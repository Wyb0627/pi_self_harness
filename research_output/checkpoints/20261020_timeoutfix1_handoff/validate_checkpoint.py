#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def canonical(value):
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode()


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


manifest = ROOT / "file-manifest.sha256"
for line in manifest.read_text().splitlines():
    expected, relative = line.split("  ", 1)
    path = ROOT / relative
    assert path.is_file(), f"missing: {relative}"
    assert digest(path) == expected, f"hash mismatch: {relative}"

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue
    assert path.name not in {
        ".execution.lock", "auth.json", "trace.jsonl", "runner.log", "evaluator.log"
    }, f"forbidden file: {path}"
    assert path.suffix.lower() != ".pem", f"PEM excluded: {path}"
    if path.suffix == ".json":
        json.loads(path.read_text())

dgm = ROOT / "dgm_seed20261014_v2_timeoutfix1"
ledger_path = dgm / "global-cost-ledger.jsonl"
previous = "0" * 64
for sequence, line in enumerate(ledger_path.read_text().splitlines()):
    record = json.loads(line)
    assert record["sequence"] == sequence
    assert record["previous_hash"] == previous
    unhashed = {key: value for key, value in record.items() if key != "entry_hash"}
    assert hashlib.sha256(canonical(unhashed)).hexdigest() == record["entry_hash"]
    previous = record["entry_hash"]

observations = list((dgm / "observations").rglob("observation.json"))
assert len(observations) == 190, len(observations)
for path in observations:
    observation = json.loads(path.read_text())
    unhashed = {
        key: value for key, value in observation.items() if key != "observation_hash"
    }
    assert hashlib.sha256(canonical(unhashed)).hexdigest() == observation["observation_hash"]
    identity_path = path.with_name("identity.json")
    identity = json.loads(identity_path.read_text())
    assert hashlib.sha256(canonical(identity)).hexdigest() == observation["identity_hash"]

for task_dir in {
    path.parent for path in (dgm / "observations").rglob("identity.json")
}:
    assert (task_dir / "observation.json").is_file(), f"incomplete task copied: {task_dir}"

p2 = ROOT / "p2_seed20261014_v2_timeoutfix1"
assert not list(p2.rglob("observation.json"))
assert not (dgm / "search-seal.json").exists()
assert not (dgm / "search-invalid.json").exists()
assert not list(ROOT.rglob("test-140-manifest.json"))
assert not list(ROOT.rglob("endpoint-state.json"))
print("checkpoint validation passed: 190 complete observations; D_test unconsumed")
