from __future__ import annotations

import json
import math
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

from .audit_sampler import deterministic_audit, derive_audit_seed
from .catalogue import load_frozen_catalogue
from .coverage import (
    facility_location_coverage,
    greedy_by_marginal_coverage,
    marginal_coverage,
    redundancy,
)
from .embedding_client import (
    FakeEmbeddingClient,
    HttpEmbeddingClient,
    _RejectRedirects,
    embedding_cache_key,
)
from .retrieval import LexicalIndex, SemanticIndex
from .schemas import (
    EMBEDDING_DIMENSION,
    EXPECTED_DATASET_MANIFEST_SHA256,
    EXPECTED_ORDERED_IDS_SHA256,
    EmbeddingSpec,
    InfrastructureError,
    ValidationError,
)
from .trajectory import load_public_trajectory


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = (
    ROOT
    / "research_output"
    / "clm_budgeted_evolution_20260924_125503"
    / "dgm_swebench_verified_200.v1.json"
)
HASH_A = "a" * 64
HASH_B = "b" * 64


def axis(index: int = 0) -> list[float]:
    vector = [0.0] * EMBEDDING_DIMENSION
    vector[index] = 1.0
    return vector


class CatalogueTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalogue = load_frozen_catalogue(MANIFEST)

    def test_frozen_manifest_hash_order_and_distribution(self) -> None:
        self.assertEqual(
            self.catalogue.dataset_manifest_hash, EXPECTED_DATASET_MANIFEST_SHA256
        )
        self.assertEqual(self.catalogue.ordered_ids_hash, EXPECTED_ORDERED_IDS_SHA256)
        self.assertEqual(len(self.catalogue.cards), 200)
        self.assertEqual(self.catalogue.task_ids, tuple(sorted(self.catalogue.task_ids)))
        first = self.catalogue.cards[0]
        self.assertNotIn("test_patch", first.task_text)
        self.assertNotIn("patch", first.task_text.lower().split())

    def test_changed_manifest_fails_before_catalogue_construction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            changed = Path(temporary) / "manifest.json"
            changed.write_bytes(MANIFEST.read_bytes() + b" ")
            with self.assertRaisesRegex(ValidationError, "hash mismatch"):
                load_frozen_catalogue(changed)

    def test_lexical_bm25_and_filters_are_deterministic(self) -> None:
        index = LexicalIndex(self.catalogue)
        self.assertLessEqual(max(index._document_frequency.values()), 200)
        first = index.search("separability matrix", filters={"project": "astropy"}, limit=5)
        second = index.search("separability matrix", filters={"project": "astropy"}, limit=5)
        self.assertEqual(first, second)
        self.assertEqual(first[0].source, "lexical_bm25")
        self.assertEqual(first[0].instance_id, "astropy__astropy-12907")
        with self.assertRaises(ValidationError):
            index.search("matrix", filters={"private_tests": "yes"}, limit=1)


class EmbeddingContractTest(unittest.TestCase):
    def setUp(self) -> None:
        self.spec = EmbeddingSpec(
            sidecar_url="http://127.0.0.1:9777/v1/embeddings",
            sidecar_manifest_hash=HASH_A,
        )

    def test_fake_traverses_contract_and_cache_key_is_role_sensitive(self) -> None:
        client = FakeEmbeddingClient(self.spec, lambda _text, _role: axis())
        batch = client.embed(["same text"], role="query")
        self.assertEqual(len(batch.vectors[0]), 1024)
        self.assertNotEqual(
            embedding_cache_key("same text", "query", self.spec),
            embedding_cache_key("same text", "task", self.spec),
        )
        self.assertTrue(str(client.requests[0]["input"][0]).startswith("Instruct:"))

    def test_wrong_revision_metadata_and_non_normalized_vectors_fail_closed(self) -> None:
        mismatch = FakeEmbeddingClient(
            self.spec,
            lambda _text, _role: axis(),
            metadata_overrides={"model_revision": "wrong"},
        )
        with self.assertRaisesRegex(InfrastructureError, "model_revision mismatch"):
            mismatch.embed(["query"], role="query")
        non_normalized = FakeEmbeddingClient(
            self.spec, lambda _text, _role: [1.0, 1.0] + [0.0] * 1022
        )
        with self.assertRaisesRegex(InfrastructureError, "not L2-normalized"):
            non_normalized.embed(["query"], role="query")

    def test_semantic_results_remain_a_distinct_stream(self) -> None:
        catalogue = load_frozen_catalogue(MANIFEST)
        task_vectors = {instance_id: axis() for instance_id in catalogue.task_ids}
        client = FakeEmbeddingClient(self.spec, lambda _text, _role: axis())
        hits = SemanticIndex(catalogue, task_vectors, client).search("query", limit=2)
        self.assertTrue(all(hit.source == "semantic_cosine" for hit in hits))
        self.assertEqual([hit.instance_id for hit in hits], sorted(catalogue.task_ids)[:2])

    def test_http_client_missing_sidecar_fails_without_lexical_fallback(self) -> None:
        client = HttpEmbeddingClient(self.spec, timeout_seconds=1)
        with patch(
            "urllib.request.urlopen",
            side_effect=urllib.error.URLError("sidecar unavailable"),
        ):
            with self.assertRaisesRegex(InfrastructureError, "sidecar request failed"):
                client.embed(["query"], role="query")

    def test_http_client_rejects_remote_endpoint_and_wrong_dimension(self) -> None:
        with self.assertRaisesRegex(ValidationError, "local HTTP endpoint"):
            HttpEmbeddingClient(
                EmbeddingSpec(
                    sidecar_url="https://example.com/v1/embeddings",
                    sidecar_manifest_hash=HASH_A,
                ),
                timeout_seconds=1,
            )
        wrong_dimension = FakeEmbeddingClient(
            self.spec, lambda _text, _role: [1.0] + [0.0] * 1022
        )
        with self.assertRaisesRegex(InfrastructureError, "wrong dimension"):
            wrong_dimension.embed(["query"], role="query")
        with self.assertRaisesRegex(InfrastructureError, "redirect is forbidden"):
            _RejectRedirects().redirect_request(
                None, None, 302, "Found", {}, "https://remote.example/v1/embeddings"
            )


class CoverageTest(unittest.TestCase):
    def setUp(self) -> None:
        root_two = math.sqrt(0.5)
        self.vectors = {
            "a": (1.0, 0.0),
            "b": (0.0, 1.0),
            "c": (root_two, root_two),
            "negative": (-1.0, 0.0),
        }
        self.universe = ("a", "b", "c", "negative")

    def test_exact_facility_location_and_marginal_formula(self) -> None:
        expected_a = (1 + 0 + math.sqrt(0.5) + 0) / 4
        self.assertAlmostEqual(
            facility_location_coverage(("a",), self.universe, self.vectors), expected_a
        )
        expected_gain_b = (0 + 1 + 0 + 0) / 4
        self.assertAlmostEqual(
            marginal_coverage("b", ("a",), self.universe, self.vectors),
            expected_gain_b,
        )
        self.assertEqual(
            facility_location_coverage((), self.universe, self.vectors), 0.0
        )

    def test_redundancy_formula_and_lexical_tie_break(self) -> None:
        report = redundancy(("a", "b", "c"), self.vectors)
        self.assertAlmostEqual(report.value, math.sqrt(0.5))
        self.assertEqual(redundancy(("a",), self.vectors).value, 0.0)
        selected = greedy_by_marginal_coverage(
            ("b", "a"), (), ("a", "b"), self.vectors, capacity=1
        )
        self.assertEqual(selected[0][0], "a")


class AuditAndTrajectoryTest(unittest.TestCase):
    def test_audit_reproduces_and_samples_only_after_selection(self) -> None:
        seed = derive_audit_seed("experiment-7", HASH_A, HASH_B, "c" * 64)
        first = deterministic_audit(
            ("a", "b", "c", "d"), ("a",), size=2, seed_derivation=seed
        )
        second = deterministic_audit(
            ("a", "b", "c", "d"), ("a",), size=2, seed_derivation=seed
        )
        self.assertEqual(first, second)
        self.assertEqual(first.candidate_ids, ("b", "c", "d"))
        self.assertNotIn("a", first.audit_ids)

    def test_malformed_trajectory_is_not_replaced_with_invented_text(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "trace.jsonl"
            path.write_text('{"type": "ok"}\nnot json\n')
            with self.assertRaisesRegex(ValidationError, "Malformed trajectory JSON"):
                load_public_trajectory(path)

    def test_private_evaluator_fields_are_rejected_from_trajectory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "trace.jsonl"
            path.write_text(json.dumps({"event": {"test_patch": "secret"}}) + "\n")
            with self.assertRaisesRegex(ValidationError, "restricted evaluator field"):
                load_public_trajectory(path)


if __name__ == "__main__":
    unittest.main()
