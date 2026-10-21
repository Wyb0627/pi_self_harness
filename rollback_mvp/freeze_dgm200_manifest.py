"""Freeze the exact 200-task DGM SWE-bench Verified benchmark."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DGM_COMMIT = "682eb38a3eb232f4396924cacd0a083bf1444cf8"
HF_REVISION = "c104f840cc67f8b6eec6f759ebc8b2693d585d4a"
DATASET_NAME = "princeton-nlp/SWE-bench_Verified"
DATASET_SPLIT = "test"
DATASET_ROWS = 500
FEATURES = (
    "repo",
    "instance_id",
    "base_commit",
    "patch",
    "test_patch",
    "problem_statement",
    "hints_text",
    "created_at",
    "version",
    "FAIL_TO_PASS",
    "PASS_TO_PASS",
    "environment_setup_commit",
    "difficulty",
)
SUBSET_HASHES = {
    "small": "b8909d87321bf7e9277e82baff8b2a739a3e1e76585ec512ae8ad4b6eef86591",
    "medium": "bf1cde9b2590f7813cc0cbb43a3ce0a9fccbdd163083891ff96b9abc82e4c06f",
    "big": "76a8b81f0c044a64c928ab46312b5eb69c3728ab7d39c4fe6239a790797906cd",
}
SUBSET_SIZES = {"small": 10, "medium": 50, "big": 140}
SUBSET_ORDER_IDS_SHA256 = (
    "5ee4ed8c14f82509a5c015969ee93c31302ee111e3aa28094a5548258f529cb0"
)
VERIFIED_ORDER_IDS_SHA256 = (
    "421c950302366954005dab020cdc89ca0d6ae1f0423e2b662637f7790a31d0d7"
)
PARQUET_SHA256 = (
    "a45b1fe4e2f0c8390b2b2938ac83e92ed5979000856808f3679c07812e9e6dcd"
)
ARROW_SHA256 = "0d119efe73413554335bd410a04d82fd4a586bfd312cee677ee40af5de2ac46e"


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_ids(instance_ids: list[str]) -> str:
    return sha256_bytes("".join(f"{instance_id}\n" for instance_id in instance_ids).encode())


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def fetch_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "pi-dgm200-freezer/1"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def fetch_subsets() -> tuple[dict[str, list[str]], dict[str, str]]:
    subsets: dict[str, list[str]] = {}
    source_urls: dict[str, str] = {}
    for stage in ("small", "medium", "big"):
        url = (
            "https://raw.githubusercontent.com/jennyzzt/dgm/"
            f"{DGM_COMMIT}/swe_bench/subsets/{stage}.json"
        )
        content = fetch_bytes(url)
        actual_hash = sha256_bytes(content)
        if actual_hash != SUBSET_HASHES[stage]:
            raise ValueError(
                f"{stage}.json hash mismatch: expected {SUBSET_HASHES[stage]}, "
                f"found {actual_hash}"
            )
        values = json.loads(content)
        if not isinstance(values, list) or not all(
            isinstance(value, str) for value in values
        ):
            raise ValueError(f"{stage}.json is not a string list.")
        subsets[stage] = values
        source_urls[stage] = url
    return subsets, source_urls


def fetch_dataset_rows() -> tuple[list[dict[str, Any]], tuple[str, ...]]:
    rows: list[dict[str, Any]] = []
    features: tuple[str, ...] | None = None
    page_size = 100
    for offset in range(0, DATASET_ROWS, page_size):
        query = urllib.parse.urlencode(
            {
                "dataset": DATASET_NAME,
                "config": "default",
                "split": DATASET_SPLIT,
                "offset": offset,
                "length": page_size,
                "revision": HF_REVISION,
            }
        )
        request = urllib.request.Request(
            f"https://datasets-server.huggingface.co/rows?{query}",
            headers={"User-Agent": "pi-dgm200-freezer/1"},
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            revision = response.headers.get("x-revision")
            if revision != HF_REVISION:
                raise ValueError(
                    f"Expected Hugging Face revision {HF_REVISION}, found {revision}"
                )
            payload = json.load(response)
        if payload.get("partial"):
            raise ValueError("Hugging Face returned a partial dataset page.")
        page_features = tuple(feature["name"] for feature in payload["features"])
        if features is None:
            features = page_features
        elif page_features != features:
            raise ValueError("Dataset feature order changed between pages.")
        for item in payload["rows"]:
            expected_index = len(rows)
            if item["row_idx"] != expected_index:
                raise ValueError(
                    f"Expected dataset row {expected_index}, found {item['row_idx']}"
                )
            if item.get("truncated_cells"):
                raise ValueError(f"Dataset row {expected_index} contains truncated cells.")
            rows.append(item["row"])
    if features is None:
        raise ValueError("Dataset API returned no features.")
    return rows, features


def validate_subsets(subsets: dict[str, list[str]]) -> list[str]:
    for stage, expected_size in SUBSET_SIZES.items():
        if len(subsets.get(stage, [])) != expected_size:
            raise ValueError(
                f"Expected {expected_size} {stage} tasks, found "
                f"{len(subsets.get(stage, []))}"
            )
    task_ids = [
        instance_id
        for stage in ("small", "medium", "big")
        for instance_id in subsets[stage]
    ]
    if len(set(task_ids)) != 200:
        raise ValueError("DGM small, medium, and big subsets are not disjoint.")
    actual_hash = sha256_ids(task_ids)
    if actual_hash != SUBSET_ORDER_IDS_SHA256:
        raise ValueError(
            "DGM subset-order ID hash mismatch: "
            f"expected {SUBSET_ORDER_IDS_SHA256}, found {actual_hash}"
        )
    return task_ids


def build_manifest(
    subsets: dict[str, list[str]],
    source_urls: dict[str, str],
    rows: list[dict[str, Any]],
    features: tuple[str, ...],
) -> dict[str, Any]:
    task_ids = validate_subsets(subsets)
    if len(rows) != DATASET_ROWS:
        raise ValueError(f"Expected {DATASET_ROWS} dataset rows, found {len(rows)}")
    if features != FEATURES:
        raise ValueError(f"Unexpected dataset fields: {features}")
    if any(tuple(row) != FEATURES for row in rows):
        raise ValueError("One or more dataset rows have unexpected field order.")

    stage_by_id: dict[str, tuple[str, int]] = {}
    for stage in ("small", "medium", "big"):
        for stage_index, instance_id in enumerate(subsets[stage]):
            stage_by_id[instance_id] = (stage, stage_index)
    dataset_ids = [row["instance_id"] for row in rows]
    missing = sorted(set(task_ids) - set(dataset_ids))
    if missing:
        raise ValueError(f"DGM task IDs missing from Verified: {missing}")

    records = []
    for dataset_row_index, row in enumerate(rows):
        instance_id = row["instance_id"]
        if instance_id not in stage_by_id:
            continue
        stage, stage_index = stage_by_id[instance_id]
        records.append(
            {
                "ordinal": len(records),
                "dataset_row_index": dataset_row_index,
                "stage": stage,
                "stage_index": stage_index,
                "source_row_sha256": sha256_bytes(canonical_json(row)),
                "record": row,
            }
        )
    selected_ids = [entry["record"]["instance_id"] for entry in records]
    if selected_ids != sorted(selected_ids):
        raise ValueError("Selected Verified rows are not in lexicographic instance order.")
    actual_hash = sha256_ids(selected_ids)
    if actual_hash != VERIFIED_ORDER_IDS_SHA256:
        raise ValueError(
            "Verified-order ID hash mismatch: "
            f"expected {VERIFIED_ORDER_IDS_SHA256}, found {actual_hash}"
        )

    return {
        "schema_version": 1,
        "name": "dgm-swebench-verified-200",
        "dgm": {
            "repository": "https://github.com/jennyzzt/dgm",
            "commit": DGM_COMMIT,
            "partition_semantics": "disjoint_incremental_10_plus_50_plus_140",
            "subset_order_ids_sha256": SUBSET_ORDER_IDS_SHA256,
            "subsets": {
                stage: {
                    "size": SUBSET_SIZES[stage],
                    "sha256": SUBSET_HASHES[stage],
                    "source_url": source_urls[stage],
                    "instance_ids": subsets[stage],
                }
                for stage in ("small", "medium", "big")
            },
        },
        "swebench": {
            "dataset": DATASET_NAME,
            "split": DATASET_SPLIT,
            "revision": HF_REVISION,
            "source_row_count": DATASET_ROWS,
            "features": list(FEATURES),
            "parquet_sha256": PARQUET_SHA256,
            "arrow_sha256": ARROW_SHA256,
        },
        "ordering": {
            "rule": "source Verified row order filtered by DGM subset membership",
            "instance_ids_sha256": VERIFIED_ORDER_IDS_SHA256,
            "count": len(records),
        },
        "records": records,
    }


def validate_released_order(manifest: dict[str, Any], released_result: Path) -> None:
    released = json.loads(released_result.read_text())
    expected = [
        entry["record"]["instance_id"] for entry in manifest["records"]
    ]
    if released.get("submitted_ids") != expected:
        raise ValueError(
            f"Released DGM submitted_ids do not match manifest: {released_result}"
        )


def validate_local_source(path: Path, expected_hash: str, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")
    actual_hash = sha256_bytes(path.read_bytes())
    if actual_hash != expected_hash:
        raise ValueError(
            f"{label} hash mismatch: expected {expected_hash}, found {actual_hash}"
        )


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as file:
        temporary = Path(file.name)
        file.write(content)
        file.flush()
        os.fsync(file.fileno())
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--released-result")
    parser.add_argument("--parquet")
    parser.add_argument("--arrow")
    args = parser.parse_args()

    if args.parquet:
        validate_local_source(Path(args.parquet), PARQUET_SHA256, "Verified Parquet")
    if args.arrow:
        validate_local_source(Path(args.arrow), ARROW_SHA256, "Verified Arrow")

    subsets, source_urls = fetch_subsets()
    rows, features = fetch_dataset_rows()
    manifest = build_manifest(subsets, source_urls, rows, features)
    if args.released_result:
        validate_released_order(manifest, Path(args.released_result))

    output = Path(args.output).resolve()
    content = json.dumps(manifest, ensure_ascii=False, indent=2).encode() + b"\n"
    atomic_write(output, content)
    digest = sha256_bytes(content)
    atomic_write(
        output.with_suffix(f"{output.suffix}.sha256"),
        f"{digest}  {output.name}\n".encode(),
    )
    print(
        json.dumps(
            {
                "output": str(output),
                "sha256": digest,
                "records": len(manifest["records"]),
                "instance_ids_sha256": manifest["ordering"][
                    "instance_ids_sha256"
                ],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
