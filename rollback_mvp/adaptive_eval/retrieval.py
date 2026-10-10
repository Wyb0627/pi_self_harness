"""Independent lexical BM25 and semantic retrieval result streams."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass
from typing import Mapping, Sequence

from .catalogue import TOKEN_PATTERN
from .embedding_client import EmbeddingClient, embedding_cache_key
from .schemas import (
    CatalogueManifest,
    ValidationError,
    canonical_json_bytes,
    sha256_bytes,
)


@dataclass(frozen=True, slots=True)
class RetrievalHit:
    instance_id: str
    source: str
    rank: int
    score: float
    evidence: tuple[str, ...]


def tokenize_query(query: str) -> tuple[str, ...]:
    if not isinstance(query, str) or not query.strip():
        raise ValidationError("Retrieval query must be a non-empty string")
    return tuple(match.group(0).lower() for match in TOKEN_PATTERN.finditer(query))


class LexicalIndex:
    """Small pure-Python Okapi BM25 index over public task-card text."""

    def __init__(self, catalogue: CatalogueManifest, *, k1: float = 1.2, b: float = 0.75):
        if k1 <= 0 or not 0 <= b <= 1:
            raise ValidationError("BM25 requires k1 > 0 and b in [0, 1]")
        self.catalogue = catalogue
        self.k1 = k1
        self.b = b
        self._tokens: dict[str, tuple[str, ...]] = {}
        self._frequencies: dict[str, Counter[str]] = {}
        document_frequency: Counter[str] = Counter()
        for card in catalogue.cards:
            tokens = tuple(match.group(0).lower() for match in TOKEN_PATTERN.finditer(card.task_text))
            self._tokens[card.instance_id] = tokens
            frequencies = Counter(tokens)
            self._frequencies[card.instance_id] = frequencies
            document_frequency.update(frequencies.keys())
        self._document_frequency = document_frequency
        self._average_length = sum(map(len, self._tokens.values())) / len(self._tokens)

    def search(
        self,
        query: str,
        *,
        filters: Mapping[str, str] | None,
        limit: int,
    ) -> tuple[RetrievalHit, ...]:
        if limit <= 0:
            raise ValidationError("Lexical search limit must be positive")
        query_terms = tokenize_query(query)
        if not query_terms:
            raise ValidationError("Lexical query contains no indexable tokens")
        supported_filters = {"repo", "project"}
        filters = filters or {}
        unknown_filters = set(filters) - supported_filters
        if unknown_filters:
            raise ValidationError(f"Unknown lexical filters: {sorted(unknown_filters)}")
        count = len(self.catalogue.cards)
        scored: list[tuple[float, str, tuple[str, ...]]] = []
        for card in self.catalogue.cards:
            tags = set(card.structured_tags)
            if "repo" in filters and card.repo != filters["repo"]:
                continue
            if "project" in filters and f"project:{filters['project']}" not in tags:
                continue
            frequencies = self._frequencies[card.instance_id]
            document_length = len(self._tokens[card.instance_id])
            score = 0.0
            matched: list[str] = []
            for term in query_terms:
                frequency = frequencies.get(term, 0)
                if not frequency:
                    continue
                matched.append(term)
                df = self._document_frequency[term]
                inverse_document_frequency = math.log(1 + (count - df + 0.5) / (df + 0.5))
                denominator = frequency + self.k1 * (
                    1 - self.b + self.b * document_length / self._average_length
                )
                score += inverse_document_frequency * frequency * (self.k1 + 1) / denominator
            if score > 0:
                scored.append((score, card.instance_id, tuple(dict.fromkeys(matched))))
        scored.sort(key=lambda item: (-item[0], item[1]))
        return tuple(
            RetrievalHit(
                instance_id=instance_id,
                source="lexical_bm25",
                rank=rank,
                score=score,
                evidence=matched,
            )
            for rank, (score, instance_id, matched) in enumerate(scored[:limit], start=1)
        )


def cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right) or not left:
        raise ValidationError("Cosine vectors must have equal non-zero dimensions")
    return sum(a * b for a, b in zip(left, right))


class SemanticIndex:
    def __init__(
        self,
        catalogue: CatalogueManifest,
        vectors: Mapping[str, Sequence[float]],
        client: EmbeddingClient,
    ) -> None:
        missing = set(catalogue.task_ids) - set(vectors)
        extra = set(vectors) - set(catalogue.task_ids)
        if missing or extra:
            raise ValidationError(
                f"Semantic vector IDs mismatch: missing={sorted(missing)}, extra={sorted(extra)}"
            )
        self.catalogue = catalogue
        self.vectors = {}
        for card in catalogue.cards:
            vector = tuple(float(value) for value in vectors[card.instance_id])
            if len(vector) != client.spec.dimension:
                raise ValidationError(
                    f"Task vector has wrong dimension: {card.instance_id}"
                )
            if not all(math.isfinite(value) for value in vector):
                raise ValidationError(f"Task vector is non-finite: {card.instance_id}")
            norm = math.sqrt(sum(value * value for value in vector))
            if not math.isclose(norm, 1.0, rel_tol=0.0, abs_tol=1e-5):
                raise ValidationError(f"Task vector is not normalized: {card.instance_id}")
            actual_hash = sha256_bytes(canonical_json_bytes(vector))
            if card.embedding_vector_hash and actual_hash != card.embedding_vector_hash:
                raise ValidationError(
                    f"Task vector hash mismatch: {card.instance_id}"
                )
            self.vectors[card.instance_id] = vector
        self.client = client

    def search(self, query: str, *, limit: int) -> tuple[RetrievalHit, ...]:
        if limit <= 0:
            raise ValidationError("Semantic search limit must be positive")
        if not query.strip():
            raise ValidationError("Semantic query must be non-empty")
        batch = self.client.embed([query], role="query")
        query_vector = batch.vectors[0]
        scored = [
            (cosine_similarity(query_vector, vector), instance_id)
            for instance_id, vector in self.vectors.items()
        ]
        scored.sort(key=lambda item: (-item[0], item[1]))
        return tuple(
            RetrievalHit(
                instance_id=instance_id,
                source="semantic_cosine",
                rank=rank,
                score=score,
                evidence=(
                    f"cache_key:{embedding_cache_key(query, 'query', self.client.spec)}",
                    f"response_hash:{batch.response_hash}",
                    f"vector_hash:{batch.vector_hashes[0]}",
                ),
            )
            for rank, (score, instance_id) in enumerate(scored[:limit], start=1)
        )
