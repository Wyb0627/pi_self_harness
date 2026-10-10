"""Strict HTTP contract and deterministic fake for the local embedding sidecar."""

from __future__ import annotations

import dataclasses
import json
import math
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol, Sequence

from .schemas import (
    EMBEDDING_DIMENSION,
    QUERY_TEMPLATE,
    EmbeddingSpec,
    CatalogueManifest,
    InfrastructureError,
    ValidationError,
    canonical_json_bytes,
    sha256_bytes,
    hash_json,
)
from .state import atomic_json


@dataclass(frozen=True, slots=True)
class EmbeddingBatch:
    vectors: tuple[tuple[float, ...], ...]
    vector_hashes: tuple[str, ...]
    response_hash: str


class EmbeddingClient(Protocol):
    spec: EmbeddingSpec

    def embed(self, inputs: Sequence[str], *, role: str) -> EmbeddingBatch: ...


@dataclass(frozen=True, slots=True)
class CatalogueEmbeddingIndex:
    catalogue: CatalogueManifest
    vectors: dict[str, tuple[float, ...]]
    cache_keys: dict[str, str]
    response_hash: str
    index_hash: str


def embed_catalogue(
    catalogue: CatalogueManifest, client: EmbeddingClient, evidence_dir: Path
) -> CatalogueEmbeddingIndex:
    """Bind every frozen task card to one validated sidecar vector and cache key."""
    request_evidence = {
        "schema_version": 1,
        "catalogue_hash": catalogue.catalogue_hash,
        "embedding_spec": dataclasses.asdict(client.spec),
        "task_text_hashes": {
            card.instance_id: card.task_text_hash for card in catalogue.cards
        },
        "cache_keys": {
            card.instance_id: embedding_cache_key(card.task_text, "task", client.spec)
            for card in catalogue.cards
        },
    }
    atomic_json(evidence_dir / "embedding-request.json", request_evidence)
    try:
        batch = client.embed([card.task_text for card in catalogue.cards], role="task")
    except Exception as error:
        atomic_json(
            evidence_dir / "embedding-error.json",
            {"error_type": type(error).__name__, "message": str(error)},
        )
        raise
    if len(batch.vectors) != len(catalogue.cards):
        raise InfrastructureError("Embedding batch does not cover the frozen catalogue")
    vectors: dict[str, tuple[float, ...]] = {}
    cache_keys: dict[str, str] = {}
    cards = []
    for card, vector, vector_hash in zip(
        catalogue.cards, batch.vectors, batch.vector_hashes
    ):
        cache_key = embedding_cache_key(card.task_text, "task", client.spec)
        vectors[card.instance_id] = vector
        cache_keys[card.instance_id] = cache_key
        cards.append(
            dataclasses.replace(
                card,
                embedding_id=cache_key,
                embedding_vector_hash=vector_hash,
            )
        )
    index_payload = {
        "schema_version": 1,
        "source_catalogue_hash": catalogue.catalogue_hash,
        "sidecar_manifest_hash": client.spec.sidecar_manifest_hash,
        "model_revision": client.spec.model_revision,
        "cache_keys": cache_keys,
        "vector_hashes": {
            card.instance_id: card.embedding_vector_hash for card in cards
        },
        "response_hash": batch.response_hash,
    }
    index_hash = hash_json(index_payload)
    atomic_json(
        evidence_dir / "embedding-index.json",
        index_payload | {"index_hash": index_hash},
    )
    bound_catalogue = CatalogueManifest(
        source_path=catalogue.source_path,
        dataset_manifest_hash=catalogue.dataset_manifest_hash,
        ordered_ids_hash=catalogue.ordered_ids_hash,
        catalogue_hash=hash_json(
            {
                "source_catalogue_hash": catalogue.catalogue_hash,
                "embedding_index_hash": index_hash,
                "cards": [dataclasses.asdict(card) for card in cards],
            }
        ),
        task_ids=catalogue.task_ids,
        cards=tuple(cards),
        embedding_index_hash=index_hash,
        embedding_response_hash=batch.response_hash,
    )
    return CatalogueEmbeddingIndex(
        catalogue=bound_catalogue,
        vectors=vectors,
        cache_keys=cache_keys,
        response_hash=batch.response_hash,
        index_hash=index_hash,
    )


def embedding_cache_key(text: str, role: str, spec: EmbeddingSpec) -> str:
    if role not in {"task", "query"}:
        raise ValidationError(f"Unknown embedding role: {role}")
    payload = {
        "text": text,
        "role": role,
        "template_revision": spec.query_template_revision,
        "max_length": spec.max_length,
        "model_revision": spec.model_revision,
        "sidecar_manifest_hash": spec.sidecar_manifest_hash,
    }
    return sha256_bytes(canonical_json_bytes(payload))


def format_embedding_input(text: str, role: str) -> str:
    if role == "task":
        return text
    if role == "query":
        return QUERY_TEMPLATE.format(query=text)
    raise ValidationError(f"Unknown embedding role: {role}")


def _validate_vector(raw: object, index: int, dimension: int) -> tuple[float, ...]:
    if not isinstance(raw, list) or len(raw) != dimension:
        found = len(raw) if isinstance(raw, list) else type(raw).__name__
        raise InfrastructureError(
            f"Embedding {index} has wrong dimension: expected {dimension}, found {found}"
        )
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in raw):
        raise InfrastructureError(f"Embedding {index} contains a non-numeric value")
    vector = tuple(float(value) for value in raw)
    if not all(math.isfinite(value) for value in vector):
        raise InfrastructureError(f"Embedding {index} contains a non-finite value")
    norm = math.sqrt(sum(value * value for value in vector))
    if not math.isclose(norm, 1.0, rel_tol=0.0, abs_tol=1e-5):
        raise InfrastructureError(f"Embedding {index} is not L2-normalized: norm={norm}")
    return vector


def validate_embedding_response(
    payload: object, expected_count: int, spec: EmbeddingSpec
) -> EmbeddingBatch:
    if not isinstance(payload, dict):
        raise InfrastructureError("Embedding sidecar response must be a JSON object")
    expected_metadata = {
        "dimension": spec.dimension,
        "normalized": True,
        "model_id": spec.model_id,
        "model_revision": spec.model_revision,
        "manifest_sha256": spec.sidecar_manifest_hash,
    }
    for field, expected in expected_metadata.items():
        if payload.get(field) != expected:
            raise InfrastructureError(
                f"Embedding sidecar {field} mismatch: expected {expected!r}, "
                f"found {payload.get(field)!r}"
            )
    data = payload.get("data")
    if not isinstance(data, list) or len(data) != expected_count:
        raise InfrastructureError(
            f"Embedding sidecar returned {len(data) if isinstance(data, list) else 'invalid'} "
            f"items for {expected_count} inputs"
        )
    vectors: list[tuple[float, ...]] = []
    hashes: list[str] = []
    for expected_index, item in enumerate(data):
        if not isinstance(item, dict) or item.get("index") != expected_index:
            raise InfrastructureError("Embedding response indices are not contiguous and ordered")
        vector = _validate_vector(item.get("embedding"), expected_index, spec.dimension)
        vectors.append(vector)
        hashes.append(sha256_bytes(canonical_json_bytes(vector)))
    return EmbeddingBatch(
        vectors=tuple(vectors),
        vector_hashes=tuple(hashes),
        response_hash=sha256_bytes(canonical_json_bytes(payload)),
    )


class HttpEmbeddingClient:
    def __init__(self, spec: EmbeddingSpec, *, timeout_seconds: float) -> None:
        if timeout_seconds <= 0:
            raise ValidationError("Embedding timeout must be positive")
        parsed = urllib.parse.urlparse(spec.sidecar_url)
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise ValidationError("sidecar_url must be a local HTTP endpoint")
        if parsed.path.rstrip("/") != "/v1/embeddings":
            raise ValidationError("sidecar_url must target /v1/embeddings")
        if parsed.query or parsed.fragment or parsed.username or parsed.password:
            raise ValidationError("sidecar_url cannot contain query, fragment, or userinfo")
        self.spec = spec
        self.timeout_seconds = timeout_seconds

    def embed(self, inputs: Sequence[str], *, role: str) -> EmbeddingBatch:
        values = tuple(inputs)
        if not values or any(not isinstance(value, str) or not value for value in values):
            raise ValidationError("Embedding inputs must be a non-empty string sequence")
        formatted = [format_embedding_input(value, role) for value in values]
        request = urllib.request.Request(
            self.spec.sidecar_url,
            data=canonical_json_bytes(
                {"input": formatted, "max_length": self.spec.max_length}
            ),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            opener = urllib.request.build_opener(_RejectRedirects())
            with opener.open(request, timeout=self.timeout_seconds) as response:
                if response.status != 200:
                    raise InfrastructureError(
                        f"Embedding sidecar returned HTTP {response.status}"
                    )
                payload = json.load(response)
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
            raise InfrastructureError(f"Embedding sidecar request failed: {error}") from error
        return validate_embedding_response(payload, len(values), self.spec)


class _RejectRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise InfrastructureError(
            f"Embedding sidecar redirect is forbidden: HTTP {code} to {newurl}"
        )


class FakeEmbeddingClient:
    """Test-only client that still traverses the production response validator."""

    def __init__(
        self,
        spec: EmbeddingSpec,
        vector_factory: Callable[[str, str], Sequence[float]],
        *,
        metadata_overrides: dict[str, object] | None = None,
    ) -> None:
        self.spec = spec
        self.vector_factory = vector_factory
        self.metadata_overrides = metadata_overrides or {}
        self.requests: list[dict[str, object]] = []

    def embed(self, inputs: Sequence[str], *, role: str) -> EmbeddingBatch:
        values = tuple(inputs)
        formatted = tuple(format_embedding_input(value, role) for value in values)
        self.requests.append(
            {
                "input": formatted,
                "role": role,
                "max_length": self.spec.max_length,
                "cache_keys": tuple(
                    embedding_cache_key(value, role, self.spec) for value in values
                ),
            }
        )
        payload: dict[str, object] = {
            "data": [
                {
                    "index": index,
                    "embedding": list(self.vector_factory(value, role)),
                }
                for index, value in enumerate(formatted)
            ],
            "dimension": EMBEDDING_DIMENSION,
            "normalized": True,
            "model_id": self.spec.model_id,
            "model_revision": self.spec.model_revision,
            "manifest_sha256": self.spec.sidecar_manifest_hash,
        }
        payload.update(self.metadata_overrides)
        return validate_embedding_response(payload, len(values), self.spec)
