"""Run and aggregate the frozen DGM 200-task Pi benchmark."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import shutil
import socket
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


EXPECTED_MANIFEST_NAME = "dgm-swebench-verified-200"
EXPECTED_ORDER_HASH = (
    "421c950302366954005dab020cdc89ca0d6ae1f0423e2b662637f7790a31d0d7"
)
PAID_CONFIRMATION = "I_APPROVE_DGM200_API_SPEND"
BOOTSTRAP_SEED = 20260925
DGM_REFERENCE = {
    "best_200_resolved": 100,
    "best_200_total": 200,
    "best_200_solve_rate": 0.5,
    "initial_reported_solve_rate": 0.2,
    "evolution_duration": "approximately two weeks",
    "evolution_cost_usd": "approximately 22000",
    "baseline_cost_usd": "approximately 10000",
    "reported_60_task_claude_eval_cost_usd": "approximately 350",
    "input_tokens": None,
    "output_tokens": None,
    "token_note": "DGM paper does not report input/output token counts.",
}


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def sha256_ids(instance_ids: list[str]) -> str:
    return sha256_bytes("".join(f"{instance_id}\n" for instance_id in instance_ids).encode())


def atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as file:
        temporary = Path(file.name)
        file.write(content)
        file.flush()
        os.fsync(file.fileno())
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_write(
        path,
        json.dumps(value, ensure_ascii=False, indent=2).encode() + b"\n",
    )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def load_manifest(path: Path) -> tuple[dict[str, Any], str]:
    manifest_content = path.read_bytes()
    manifest_hash = sha256_bytes(manifest_content)
    sidecar = path.with_suffix(f"{path.suffix}.sha256")
    if sidecar.exists():
        expected_hash = sidecar.read_text().split()[0]
        if manifest_hash != expected_hash:
            raise ValueError(
                f"Manifest hash mismatch: expected {expected_hash}, found {manifest_hash}"
            )
    manifest = json.loads(manifest_content)
    if manifest.get("name") != EXPECTED_MANIFEST_NAME:
        raise ValueError(f"Unexpected manifest name: {manifest.get('name')}")
    records = manifest.get("records")
    if not isinstance(records, list) or len(records) != 200:
        raise ValueError("Manifest must contain exactly 200 records.")
    ids = []
    for ordinal, entry in enumerate(records):
        if entry.get("ordinal") != ordinal:
            raise ValueError(f"Manifest ordinal mismatch at position {ordinal}.")
        row = entry.get("record")
        if not isinstance(row, dict):
            raise ValueError(f"Manifest row {ordinal} is invalid.")
        row_hash = sha256_bytes(canonical_json(row))
        if row_hash != entry.get("source_row_sha256"):
            raise ValueError(f"Manifest row hash mismatch for {row.get('instance_id')}.")
        ids.append(row["instance_id"])
    order_hash = sha256_ids(ids)
    if order_hash != EXPECTED_ORDER_HASH:
        raise ValueError(
            f"Manifest order hash mismatch: expected {EXPECTED_ORDER_HASH}, "
            f"found {order_hash}"
        )
    if manifest["ordering"].get("instance_ids_sha256") != order_hash:
        raise ValueError("Manifest top-level order hash is inconsistent.")
    return manifest, manifest_hash


def materialize_inputs(
    manifest: dict[str, Any],
    output_root: Path,
) -> tuple[Path, Path]:
    dataset_path = output_root / "frozen_swebench_dataset.json"
    task_path = output_root / "agent_tasks.json"
    dataset_rows = [entry["record"] for entry in manifest["records"]]
    agent_tasks = []
    for entry in manifest["records"]:
        row = entry["record"]
        task = {
            key: row[key]
            for key in ("instance_id", "repo", "base_commit", "problem_statement")
        }
        task["forbidden_paths"] = parse_patch_paths(row["test_patch"])
        agent_tasks.append(task)
    atomic_json(dataset_path, dataset_rows)
    atomic_json(task_path, agent_tasks)
    return dataset_path, task_path


def command_environment(
    docker_host: str | None,
    swebench_source: Path | None = None,
) -> dict[str, str]:
    environment = os.environ.copy()
    if docker_host:
        environment["DOCKER_HOST"] = docker_host
    if swebench_source:
        existing = environment.get("PYTHONPATH")
        environment["PYTHONPATH"] = (
            f"{swebench_source}{os.pathsep}{existing}" if existing else str(swebench_source)
        )
    if (
        "ROLLBACK_ENDPOINT_API_KEY" in environment
        and "ROLLBACK_LLM_API_KEY" not in environment
    ):
        environment["ROLLBACK_LLM_API_KEY"] = environment[
            "ROLLBACK_ENDPOINT_API_KEY"
        ]
    return environment


def run_logged(
    command: list[str],
    log_path: Path,
    *,
    cwd: Path,
    environment: dict[str, str],
    timeout: int | None = None,
) -> int:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as log:
        log.write(f"$ {subprocess.list2cmdline(command)}\n")
        log.flush()
        try:
            completed = subprocess.run(
                command,
                cwd=cwd,
                env=environment,
                stdout=log,
                stderr=subprocess.STDOUT,
                timeout=timeout,
                check=False,
                text=True,
            )
        except subprocess.TimeoutExpired:
            log.write(f"\nTimed out after {timeout} seconds.\n")
            return 124
    return completed.returncode


def docker_capture(
    args: list[str],
    *,
    docker_host: str | None,
    check: bool = True,
) -> str:
    result = subprocess.run(
        ["docker", *args],
        env=command_environment(docker_host),
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"docker {' '.join(args)} failed: {result.stderr or result.stdout}"
        )
    return result.stdout.strip()


def docker_image_exists(image: str, docker_host: str | None) -> bool:
    result = subprocess.run(
        ["docker", "image", "inspect", image],
        env=command_environment(docker_host),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def ensure_instance_image(
    args: argparse.Namespace,
    dataset_path: Path,
    task_dir: Path,
    instance_id: str,
) -> str:
    image_record_path = task_dir / "image.json"
    if image_record_path.exists():
        image_record = load_json(image_record_path)
        image = image_record["images"][0]["instance_image"]
        if docker_image_exists(image, args.docker_host):
            return image

    image_log_dir = task_dir / "image_logs"
    command = [
        args.swebench_python,
        str(args.image_builder),
        "--dataset",
        str(dataset_path),
        "--instance-id",
        instance_id,
        "--log-dir",
        str(image_log_dir),
        "--output",
        str(image_record_path),
        "--build-missing-env",
    ]
    if args.build_wheelhouse:
        command.extend(["--wheelhouse", str(args.build_wheelhouse)])
    for attempt in range(args.image_build_retries + 1):
        return_code = run_logged(
            command,
            task_dir / "build_image.log",
            cwd=args.repo_root,
            environment=command_environment(
                args.docker_host,
                args.swebench_source,
            ),
            timeout=args.image_build_timeout_seconds,
        )
        if return_code == 0 and image_record_path.exists():
            image_record = load_json(image_record_path)
            image = image_record["images"][0]["instance_image"]
            if docker_image_exists(image, args.docker_host):
                return image
        if attempt < args.image_build_retries:
            print(
                f"[image-retry] {instance_id} attempt "
                f"{attempt + 1}/{args.image_build_retries + 1}",
                flush=True,
            )
            time.sleep(args.image_build_retry_delay_seconds)
    raise RuntimeError(f"Failed to build evaluator image for {instance_id}.")


def create_solver_workspace(
    row: dict[str, Any],
    image: str,
    workspace: Path,
    docker_host: str | None,
    baseline_patch: str = "",
) -> None:
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=workspace.parent) as temporary:
        source = Path(temporary) / "source"
        source.mkdir()
        container = docker_capture(
            ["create", image, "true"],
            docker_host=docker_host,
        )
        try:
            docker_capture(
                ["cp", f"{container}:/testbed/.", str(source)],
                docker_host=docker_host,
            )
        finally:
            docker_capture(
                ["rm", "--force", container],
                docker_host=docker_host,
                check=False,
            )
        subprocess.run(
            [
                "git",
                "clone",
                "--quiet",
                "--depth",
                "1",
                f"file://{source}",
                str(workspace),
            ],
            check=True,
        )
    subprocess.run(
        ["git", "remote", "remove", "origin"],
        cwd=workspace,
        check=True,
    )
    actual_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=workspace,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if actual_commit != row["base_commit"]:
        raise ValueError(
            f"Expected {row['base_commit']} for {row['instance_id']}, "
            f"found {actual_commit}"
        )
    history_count = subprocess.run(
        ["git", "rev-list", "--all", "--count"],
        cwd=workspace,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if history_count != "1":
        raise ValueError(
            f"Solver workspace for {row['instance_id']} has {history_count} commits."
        )
    if baseline_patch:
        completed = subprocess.run(
            ["git", "apply", "--allow-empty", "-"],
            cwd=workspace,
            input=baseline_patch,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(
                f"Could not restore baseline patch for {row['instance_id']}: "
                f"{completed.stderr}"
            )


def run_original_pi(
    args: argparse.Namespace,
    task_path: Path,
    task_dir: Path,
    row: dict[str, Any],
    image: str,
) -> dict[str, Any]:
    original_dir = task_dir / "original"
    result_path = original_dir / "result.json"
    if result_path.exists():
        return load_json(result_path)
    workspace = task_dir / "workspace"
    create_solver_workspace(row, image, workspace, args.docker_host)
    original_dir.mkdir(parents=True, exist_ok=True)
    command = [
        args.node,
        str(args.pi_runner),
        "--agent-dir",
        str(args.agent_dir),
        "--instance-id",
        row["instance_id"],
        "--output",
        str(result_path),
        "--task-file",
        str(task_path),
        "--trace",
        str(original_dir / "trace.jsonl"),
        "--workspace",
        str(workspace),
        "--sandbox-image",
        image,
        "--max-output-tokens",
        str(args.max_output_tokens),
        "--max-total-tokens",
        str(args.max_task_tokens),
        "--timeout-seconds",
        str(args.agent_timeout_seconds),
        "--model-provider",
        args.model_provider,
        "--model-id",
        args.model_id,
    ]
    if args.docker_host:
        command.extend(["--docker-host", args.docker_host])
    return_code = run_logged(
        command,
        original_dir / "runner.log",
        cwd=args.repo_root,
        environment=command_environment(args.docker_host),
        timeout=args.agent_timeout_seconds + 120,
    )
    if not result_path.exists():
        raise RuntimeError(
            f"Pi runner failed without a result for {row['instance_id']} "
            f"(exit {return_code})."
        )
    result = load_json(result_path)
    result["runnerExitCode"] = return_code
    atomic_json(result_path, result)
    return result


def evaluation_identity(
    protocol: str,
    manifest_hash: str,
    evaluator_revision: str,
    model_id: str,
    instance_id: str,
    patch: str,
) -> str:
    payload = {
        "protocol": protocol,
        "manifest_sha256": manifest_hash,
        "evaluator_revision": evaluator_revision,
        "model_id": model_id,
        "instance_id": instance_id,
        "patch_sha256": sha256_bytes(patch.encode()),
    }
    return sha256_bytes(canonical_json(payload))


def inert_feedback_probe_patch(instance_id: str) -> str:
    content = f"feedback probe for {instance_id}\n"
    blob = f"blob {len(content.encode())}\0".encode() + content.encode()
    digest = hashlib.sha1(blob).hexdigest()[:7]
    return (
        "diff --git a/.rf_clm_feedback_probe b/.rf_clm_feedback_probe\n"
        "new file mode 100644\n"
        f"index 0000000..{digest}\n"
        "--- /dev/null\n"
        "+++ b/.rf_clm_feedback_probe\n"
        "@@ -0,0 +1 @@\n"
        f"+{content}"
    )


def evaluate_patch(
    args: argparse.Namespace,
    dataset_path: Path,
    output_root: Path,
    task_dir: Path,
    instance_id: str,
    protocol: str,
    model_label: str,
    patch: str,
    manifest_hash: str,
    *,
    allow_inert_probe: bool = False,
) -> dict[str, Any]:
    phase_dir = task_dir / protocol
    metadata_path = phase_dir / "evaluation.json"
    phase_dir.mkdir(parents=True, exist_ok=True)
    submitted_patch = patch
    used_inert_probe = False
    if not submitted_patch:
        if not allow_inert_probe:
            if metadata_path.exists():
                existing = load_json(metadata_path)
                if existing.get("status") == "empty_patch":
                    return existing
                raise ValueError(f"Stale evaluation metadata: {metadata_path}")
            metadata = {
                "status": "empty_patch",
                "resolved": False,
                "protocol": protocol,
                "officialEvaluatorRun": False,
            }
            atomic_json(metadata_path, metadata)
            return metadata
        submitted_patch = inert_feedback_probe_patch(instance_id)
        used_inert_probe = True

    identity = evaluation_identity(
        protocol,
        manifest_hash,
        args.swebench_revision,
        args.model_id,
        instance_id,
        submitted_patch,
    )
    if metadata_path.exists():
        existing = load_json(metadata_path)
        if (
            existing.get("identitySha256") == identity
            and existing.get("status") != "evaluator_error"
        ):
            return existing
        if existing.get("identitySha256") != identity:
            raise ValueError(f"Stale evaluation metadata: {metadata_path}")
        metadata_path.unlink()
    run_id = f"dgm200-{protocol[:18]}-{identity[:16]}"
    evaluator_model = f"{model_label}-{identity[:12]}"
    prediction = [
        {
            "instance_id": instance_id,
            "model_name_or_path": evaluator_model,
            "model_patch": submitted_patch,
        }
    ]
    prediction_path = phase_dir / "prediction.json"
    atomic_json(prediction_path, prediction)
    report_path = (
        output_root
        / "logs"
        / "run_evaluation"
        / run_id
        / evaluator_model.replace("/", "__")
        / instance_id
        / "report.json"
    )
    test_output_path = report_path.with_name("test_output.txt")
    started = time.monotonic()
    command = [
        args.swebench_python,
        "-m",
        "swebench.harness.run_evaluation",
        "--dataset_name",
        str(dataset_path),
        "--split",
        "test",
        "--instance_ids",
        instance_id,
        "--predictions_path",
        str(prediction_path),
        "--max_workers",
        "1",
        "--force_rebuild",
        "false",
        "--cache_level",
        "instance",
        "--clean",
        "false",
        "--run_id",
        run_id,
        "--timeout",
        str(args.evaluator_timeout_seconds),
    ]
    return_code = run_logged(
        command,
        phase_dir / "evaluator.log",
        cwd=output_root,
        environment=command_environment(
            args.docker_host,
            args.swebench_source,
        ),
        timeout=args.evaluator_timeout_seconds + 600,
    )
    report = load_json(report_path) if report_path.exists() else None
    resolved = bool(report and report.get(instance_id, {}).get("resolved"))
    metadata = {
        "status": "completed" if report else "evaluator_error",
        "resolved": resolved,
        "protocol": protocol,
        "officialEvaluatorRun": True,
        "usedInertFeedbackProbe": used_inert_probe,
        "identitySha256": identity,
        "submittedPatchSha256": sha256_bytes(submitted_patch.encode()),
        "runId": run_id,
        "modelNameOrPath": evaluator_model,
        "returnCode": return_code,
        "durationSeconds": round(time.monotonic() - started, 3),
        "reportPath": str(report_path),
        "testOutputPath": str(test_output_path),
    }
    atomic_json(metadata_path, metadata)
    return metadata


def parse_patch_paths(patch: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"^diff --git a/(.+?) b/", patch, re.MULTILINE)))


def recovery_candidate_paths(
    result: dict[str, Any],
    trace_path: Path,
    workspace: Path,
    maximum: int = 3,
) -> list[str]:
    candidates = parse_patch_paths(result.get("patch", ""))
    seen = set(candidates)
    trace_candidates: list[str] = []
    if trace_path.exists():
        for line in trace_path.read_text(errors="replace").splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") != "tool_execution_start":
                continue
            path = event.get("args", {}).get("path")
            if not isinstance(path, str):
                continue
            candidate = Path(path)
            if not candidate.is_absolute():
                candidate = workspace / candidate
            try:
                relative_path = candidate.resolve().relative_to(workspace.resolve())
            except ValueError:
                continue
            relative_string = relative_path.as_posix()
            if (
                relative_string.startswith(("tests/", "test/", "testing/"))
                or relative_string in seen
            ):
                continue
            local_path = workspace / relative_path
            if local_path.is_file():
                trace_candidates.append(relative_string)
                seen.add(relative_string)
    candidates.extend(reversed(trace_candidates))
    return list(dict.fromkeys(candidates))[:maximum]


def write_failure_evidence(
    evaluation: dict[str, Any],
    path: Path,
    instance_id: str,
) -> None:
    report_path = Path(evaluation["reportPath"])
    test_output_path = Path(evaluation["testOutputPath"])
    report = report_path.read_text(errors="replace") if report_path.exists() else ""
    test_output = (
        test_output_path.read_text(errors="replace") if test_output_path.exists() else ""
    )
    report = report[-40_000:]
    test_output = test_output[-80_000:]
    content = (
        "# Official SWE-bench Evaluator Feedback\n\n"
        "This is hidden evaluator information from the rejected original Pi "
        "submission. The resulting repair is feedback-assisted and is not a "
        "standard one-submission SWE-bench prediction.\n\n"
        f"Instance: `{instance_id}`\n\n"
        "## Report\n\n"
        f"```json\n{report}\n```\n\n"
        "## Test Output Tail\n\n"
        f"```text\n{test_output}\n```\n"
    )
    atomic_write(path, content.encode())


def run_recovery(
    args: argparse.Namespace,
    dataset_path: Path,
    task_path: Path,
    output_root: Path,
    task_dir: Path,
    row: dict[str, Any],
    image: str,
    original: dict[str, Any],
    original_evaluation: dict[str, Any],
    manifest_hash: str,
) -> dict[str, Any]:
    recovery_dir = task_dir / "recovery"
    result_path = recovery_dir / "result.json"
    if original_evaluation.get("resolved"):
        metadata = {"status": "not_needed", "resolved": True}
        atomic_json(recovery_dir / "status.json", metadata)
        return metadata
    if original.get("policyViolations"):
        metadata = {
            "status": "ineligible_policy_violation",
            "resolved": False,
        }
        atomic_json(recovery_dir / "status.json", metadata)
        return metadata

    feedback_evaluation = original_evaluation
    if not feedback_evaluation.get("officialEvaluatorRun"):
        feedback_evaluation = evaluate_patch(
            args,
            dataset_path,
            output_root,
            task_dir,
            row["instance_id"],
            "feedback_probe",
            "pi-rf-clm-feedback-probe",
            original.get("patch", ""),
            manifest_hash,
            allow_inert_probe=True,
        )
    if feedback_evaluation.get("status") != "completed":
        raise RuntimeError(
            f"Official feedback evaluation failed for {row['instance_id']}."
        )

    workspace = task_dir / "workspace"
    create_solver_workspace(
        row,
        image,
        workspace,
        args.docker_host,
        original.get("patch", ""),
    )
    candidates = recovery_candidate_paths(
        original,
        task_dir / "original" / "trace.jsonl",
        workspace,
    )
    if not candidates:
        metadata = {
            "status": "ineligible_no_source_slice",
            "resolved": False,
        }
        atomic_json(recovery_dir / "status.json", metadata)
        return metadata

    recovery_dir.mkdir(parents=True, exist_ok=True)
    failure_path = recovery_dir / "failure_evidence.md"
    write_failure_evidence(feedback_evaluation, failure_path, row["instance_id"])
    if not result_path.exists():
        command = [
            args.repair_python,
            str(args.repair_runner),
            "--baseline-result",
            str(task_dir / "original" / "result.json"),
            "--failure-file",
            str(failure_path),
            "--instance-id",
            row["instance_id"],
            "--output",
            str(result_path),
            "--task-file",
            str(task_path),
            "--workspace",
            str(workspace),
        ]
        for candidate in candidates:
            command.extend(["--candidate-path", candidate])
        return_code = run_logged(
            command,
            recovery_dir / "runner.log",
            cwd=args.repo_root,
            environment=command_environment(args.docker_host),
            timeout=args.repair_timeout_seconds,
        )
        if not result_path.exists():
            metadata = {
                "status": "repair_error",
                "resolved": False,
                "returnCode": return_code,
                "candidatePaths": candidates,
            }
            atomic_json(recovery_dir / "status.json", metadata)
            return metadata
    repair = load_json(result_path)
    if repair.get("status") == "repair_error":
        metadata = {
            "status": "repair_error",
            "resolved": False,
            "candidatePaths": candidates,
            "feedbackEvaluation": feedback_evaluation,
            "applicationError": repair.get("applicationError"),
        }
        atomic_json(recovery_dir / "status.json", metadata)
        return metadata
    recovery_evaluation = evaluate_patch(
        args,
        dataset_path,
        output_root,
        task_dir,
        row["instance_id"],
        "recovery",
        "pi-rf-clm-feedback-1",
        repair.get("patch", ""),
        manifest_hash,
    )
    if recovery_evaluation.get("status") != "completed":
        metadata = {
            "status": "evaluation_error",
            "resolved": False,
            "candidatePaths": candidates,
            "feedbackEvaluation": feedback_evaluation,
            "evaluation": recovery_evaluation,
        }
        atomic_json(recovery_dir / "status.json", metadata)
        return metadata
    metadata = {
        "status": "completed",
        "resolved": recovery_evaluation.get("resolved", False),
        "candidatePaths": candidates,
        "feedbackEvaluation": feedback_evaluation,
        "evaluation": recovery_evaluation,
    }
    atomic_json(recovery_dir / "status.json", metadata)
    return metadata


def total_reported_tokens(result: dict[str, Any]) -> int:
    return sum(
        int(result.get(key, 0) or 0)
        for key in (
            "inputTokens",
            "outputTokens",
            "cacheReadTokens",
            "cacheWriteTokens",
        )
    )


def budget_counted_tokens(result: dict[str, Any]) -> int:
    return total_reported_tokens(result) + int(
        result.get("conservativeTokenCharge", 0) or 0
    )


def existing_budget_tokens(output_root: Path) -> int:
    total = 0
    for path in output_root.glob("tasks/*/original/result.json"):
        total += budget_counted_tokens(load_json(path))
    for path in output_root.glob("tasks/*/recovery/result.json"):
        total += budget_counted_tokens(load_json(path))
    return total


def update_task_state(
    task_dir: Path,
    instance_id: str,
    status: str,
    **extra: Any,
) -> None:
    atomic_json(
        task_dir / "state.json",
        {
            "schemaVersion": 1,
            "instanceId": instance_id,
            "status": status,
            "updatedAtUnix": time.time(),
            **extra,
        },
    )


def run_task(
    args: argparse.Namespace,
    dataset_path: Path,
    task_path: Path,
    output_root: Path,
    entry: dict[str, Any],
    manifest_hash: str,
) -> bool:
    row = entry["record"]
    instance_id = row["instance_id"]
    task_dir = output_root / "tasks" / instance_id
    state_path = task_dir / "state.json"
    if state_path.exists() and load_json(state_path).get("status") == "completed":
        print(f"[skip] {instance_id}", flush=True)
        return False
    update_task_state(task_dir, instance_id, "building_image")
    image = ensure_instance_image(args, dataset_path, task_dir, instance_id)
    update_task_state(task_dir, instance_id, "running_original", image=image)
    original = run_original_pi(args, task_path, task_dir, row, image)
    update_task_state(task_dir, instance_id, "evaluating_original", image=image)
    if original.get("policyViolations"):
        original_evaluation = {
            "status": "policy_violation",
            "resolved": False,
            "protocol": "original",
            "officialEvaluatorRun": False,
        }
        atomic_json(
            task_dir / "original" / "evaluation.json",
            original_evaluation,
        )
    else:
        original_evaluation = evaluate_patch(
            args,
            dataset_path,
            output_root,
            task_dir,
            instance_id,
            "original",
            "original-pi-one-shot",
            original.get("patch", ""),
            manifest_hash,
        )
    if original_evaluation.get("status") == "evaluator_error":
        raise RuntimeError(f"Official evaluation failed for {instance_id}.")
    recovery = None
    if args.protocol == "original_and_feedback":
        update_task_state(task_dir, instance_id, "running_recovery", image=image)
        recovery = run_recovery(
            args,
            dataset_path,
            task_path,
            output_root,
            task_dir,
            row,
            image,
            original,
            original_evaluation,
            manifest_hash,
        )
        if recovery.get("status") == "evaluation_error":
            raise RuntimeError(
                f"Feedback recovery failed for {instance_id}: "
                f"{recovery['status']}"
            )
    update_task_state(
        task_dir,
        instance_id,
        "completed",
        image=image,
        originalResolved=original_evaluation.get("resolved", False),
        recoveryResolved=recovery.get("resolved", False) if recovery else None,
    )
    if not args.keep_workspaces:
        workspace = task_dir / "workspace"
        if workspace.exists():
            shutil.rmtree(workspace)
    if not args.keep_instance_images:
        docker_capture(
            ["image", "rm", "--force", image],
            docker_host=args.docker_host,
            check=False,
        )
    return True


def percentile(values: list[float], probability: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(ordered[lower])
    weight = position - lower
    return float(ordered[lower] * (1 - weight) + ordered[upper] * weight)


def distribution(values: list[float]) -> dict[str, float | int | None]:
    q1 = percentile(values, 0.25)
    q3 = percentile(values, 0.75)
    p95 = percentile(values, 0.95)
    return {
        "count": len(values),
        "total": round(sum(values), 3),
        "mean": round(statistics.mean(values), 3) if values else None,
        "median": round(statistics.median(values), 3) if values else None,
        "q1": round(q1, 3) if q1 is not None else None,
        "q3": round(q3, 3) if q3 is not None else None,
        "p95": round(p95, 3) if p95 is not None else None,
    }


def wilson_interval(successes: int, total: int) -> list[float] | None:
    if total == 0:
        return None
    z = 1.959963984540054
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    radius = (
        z
        * math.sqrt(
            proportion * (1 - proportion) / total
            + z * z / (4 * total * total)
        )
        / denominator
    )
    return [round(max(0.0, center - radius), 6), round(min(1.0, center + radius), 6)]


def paired_bootstrap_interval(
    original: list[bool],
    recovery: list[bool],
    *,
    samples: int = 10_000,
    seed: int = BOOTSTRAP_SEED,
) -> list[float] | None:
    if not original or len(original) != len(recovery):
        return None
    random_generator = random.Random(seed)
    differences = []
    for _ in range(samples):
        indices = [
            random_generator.randrange(len(original)) for _ in range(len(original))
        ]
        differences.append(
            sum(int(recovery[index]) - int(original[index]) for index in indices)
            / len(indices)
        )
    return [
        round(percentile(differences, 0.025) or 0.0, 6),
        round(percentile(differences, 0.975) or 0.0, 6),
    ]


def exact_mcnemar_p_value(original_only: int, recovery_only: int) -> float | None:
    discordant = original_only + recovery_only
    if discordant == 0:
        return None
    tail = min(original_only, recovery_only)
    cumulative = sum(math.comb(discordant, index) for index in range(tail + 1))
    return round(min(1.0, 2 * cumulative / (2**discordant)), 8)


def summarize_result_tokens(results: list[dict[str, Any]]) -> dict[str, Any]:
    reported_results = [
        result
        for result in results
        if result.get("tokenTelemetryAvailable") is not False
    ]
    keys = (
        "inputTokens",
        "outputTokens",
        "cacheReadTokens",
        "cacheWriteTokens",
    )
    summary: dict[str, Any] = {
        key: distribution(
            [float(result.get(key, 0) or 0) for result in reported_results]
        )
        for key in keys
    }
    summary["totalReportedTokens"] = distribution(
        [float(total_reported_tokens(result)) for result in reported_results]
    )
    summary["telemetryComplete"] = len(reported_results) == len(results)
    summary["missingTelemetryResults"] = len(results) - len(reported_results)
    return summary


def experiment_elapsed_seconds(output_root: Path) -> float | None:
    state_path = output_root / "run_state.json"
    if not state_path.exists():
        return None
    state = load_json(state_path)
    started = state.get("startedAtUnix")
    if not isinstance(started, (int, float)):
        return None
    completed = state.get("completedAtUnix")
    end = completed if isinstance(completed, (int, float)) else time.time()
    return round(max(0.0, end - started), 3)


def estimate_api_cost(
    original_results: list[dict[str, Any]],
    recovery_results: list[dict[str, Any]],
    run_config: dict[str, Any],
) -> dict[str, Any]:
    rates = run_config.get("costPerMillionTokens", {})
    if not rates or all(rates.get(key) is None for key in rates):
        return {
            "available": False,
            "reason": (
                "No externally verified token prices were supplied. Zero values "
                "from the model catalog are ignored."
            ),
        }

    def result_cost(result: dict[str, Any]) -> float:
        total = 0.0
        for token_key, rate_key in (
            ("inputTokens", "input"),
            ("outputTokens", "output"),
            ("cacheReadTokens", "cacheRead"),
            ("cacheWriteTokens", "cacheWrite"),
        ):
            rate = rates.get(rate_key)
            if rate is None:
                continue
            total += float(result.get(token_key, 0) or 0) * float(rate) / 1_000_000
        return total

    original_cost = sum(result_cost(result) for result in original_results)
    recovery_cost = sum(result_cost(result) for result in recovery_results)
    return {
        "available": True,
        "currency": "USD",
        "costPerMillionTokens": rates,
        "originalPi": round(original_cost, 6),
        "feedbackRecoveryIncrement": round(recovery_cost, 6),
        "combined": round(original_cost + recovery_cost, 6),
    }


def aggregate_results(
    manifest: dict[str, Any],
    manifest_hash: str,
    output_root: Path,
) -> dict[str, Any]:
    task_rows = []
    original_results = []
    recovery_results = []
    original_evaluations = []
    recovery_evaluations = []
    feedback_evaluations = []
    image_build_seconds = []
    for entry in manifest["records"]:
        instance_id = entry["record"]["instance_id"]
        task_dir = output_root / "tasks" / instance_id
        original_result_path = task_dir / "original" / "result.json"
        original_eval_path = task_dir / "original" / "evaluation.json"
        recovery_result_path = task_dir / "recovery" / "result.json"
        recovery_status_path = task_dir / "recovery" / "status.json"
        original_result = (
            load_json(original_result_path) if original_result_path.exists() else None
        )
        original_eval = (
            load_json(original_eval_path) if original_eval_path.exists() else None
        )
        recovery_result = (
            load_json(recovery_result_path) if recovery_result_path.exists() else None
        )
        recovery_status = (
            load_json(recovery_status_path) if recovery_status_path.exists() else None
        )
        image_record_path = task_dir / "image.json"
        if original_result:
            original_results.append(original_result)
        if recovery_result:
            recovery_results.append(recovery_result)
        if original_eval and original_eval.get("officialEvaluatorRun"):
            original_evaluations.append(original_eval)
        if recovery_status:
            recovery_evaluation = recovery_status.get("evaluation")
            feedback_evaluation = recovery_status.get("feedbackEvaluation")
            if recovery_evaluation and recovery_evaluation.get("officialEvaluatorRun"):
                recovery_evaluations.append(recovery_evaluation)
            if (
                feedback_evaluation
                and feedback_evaluation.get("officialEvaluatorRun")
                and feedback_evaluation.get("protocol") == "feedback_probe"
            ):
                feedback_evaluations.append(feedback_evaluation)
        if image_record_path.exists():
            image_record = load_json(image_record_path)
            for image in image_record.get("images", []):
                if image.get("duration_seconds") is not None:
                    image_build_seconds.append(float(image["duration_seconds"]))
        original_complete = bool(
            original_eval
            and original_eval.get("status")
            in {"completed", "empty_patch", "policy_violation"}
        )
        original_resolved = bool(original_eval and original_eval.get("resolved"))
        recovery_complete = bool(
            original_resolved
            or recovery_status
            and recovery_status.get("status")
            in {
                "completed",
                "not_needed",
                "ineligible_policy_violation",
                "ineligible_no_source_slice",
                "repair_error",
            }
        )
        recovery_resolved = bool(
            original_resolved or recovery_status and recovery_status.get("resolved")
        )
        task_rows.append(
            {
                "instanceId": instance_id,
                "stage": entry["stage"],
                "originalComplete": original_complete,
                "originalResolved": original_resolved,
                "recoveryComplete": recovery_complete,
                "recoveryResolved": recovery_resolved,
                "originalEmptyPatch": bool(
                    original_eval and original_eval.get("status") == "empty_patch"
                ),
                "originalPolicyViolation": bool(
                    original_result and original_result.get("policyViolations")
                ),
                "originalProviderError": (
                    original_result.get("providerError") if original_result else None
                ),
                "recoveryStatus": (
                    recovery_status.get("status") if recovery_status else None
                ),
                "recoveryTokenTelemetryAvailable": (
                    recovery_result.get("tokenTelemetryAvailable")
                    if recovery_result
                    else None
                ),
            }
        )

    original_completed_rows = [row for row in task_rows if row["originalComplete"]]
    recovery_completed_rows = [row for row in task_rows if row["recoveryComplete"]]
    paired_rows = [
        row
        for row in task_rows
        if row["originalComplete"] and row["recoveryComplete"]
    ]
    original_outcomes = [row["originalResolved"] for row in paired_rows]
    recovery_outcomes = [row["recoveryResolved"] for row in paired_rows]
    original_only = sum(
        original and not recovery
        for original, recovery in zip(original_outcomes, recovery_outcomes)
    )
    recovery_only = sum(
        recovery and not original
        for original, recovery in zip(original_outcomes, recovery_outcomes)
    )
    original_resolved = sum(row["originalResolved"] for row in original_completed_rows)
    recovery_resolved = sum(row["recoveryResolved"] for row in recovery_completed_rows)
    repair_attempts = sum(
        row["recoveryStatus"] in {"completed", "repair_error", "evaluation_error"}
        for row in task_rows
    )
    repair_successes = sum(
        row["recoveryResolved"]
        and not row["originalResolved"]
        and row["recoveryStatus"] == "completed"
        for row in task_rows
    )
    run_config_path = output_root / "run_config.json"
    run_config = load_json(run_config_path) if run_config_path.exists() else {}
    feedback_expected = run_config.get("protocol") == "original_and_feedback"
    original_complete = len(original_completed_rows) == len(task_rows)
    feedback_complete = len(recovery_completed_rows) == len(task_rows)
    original_token_total = sum(
        total_reported_tokens(result) for result in original_results
    )
    recovery_token_total = sum(
        total_reported_tokens(result) for result in recovery_results
    )
    all_results = [*original_results, *recovery_results]
    conservative_token_charge = sum(
        int(result.get("conservativeTokenCharge", 0) or 0)
        for result in all_results
    )
    missing_token_telemetry = sum(
        result.get("tokenTelemetryAvailable") is False
        for result in all_results
    )

    summary = {
        "schemaVersion": 1,
        "manifest": {
            "name": manifest["name"],
            "sha256": manifest_hash,
            "orderedIdsSha256": manifest["ordering"]["instance_ids_sha256"],
            "frozenTasks": len(task_rows),
        },
        "complete": original_complete
        and (feedback_complete if feedback_expected else True),
        "originalComplete": original_complete,
        "feedbackComplete": feedback_complete if feedback_expected else None,
        "experimentElapsedSeconds": experiment_elapsed_seconds(output_root),
        "imageBuildSeconds": distribution(image_build_seconds),
        "tokenAccounting": {
            "reportedTokens": original_token_total + recovery_token_total,
            "conservativeUnreportedTokenCharge": conservative_token_charge,
            "budgetCountedTokens": (
                original_token_total
                + recovery_token_total
                + conservative_token_charge
            ),
            "telemetryComplete": missing_token_telemetry == 0,
            "missingTelemetryResults": missing_token_telemetry,
        },
        "originalPiOneShot": {
            "completedTasks": len(original_completed_rows),
            "resolvedTasks": original_resolved,
            "solveRateOverCompleted": (
                round(original_resolved / len(original_completed_rows), 6)
                if original_completed_rows
                else None
            ),
            "wilson95": wilson_interval(
                original_resolved,
                len(original_completed_rows),
            ),
            "tokens": summarize_result_tokens(original_results),
            "agentDurationSeconds": distribution(
                [float(result.get("durationMs", 0)) / 1000 for result in original_results]
            ),
            "evaluatorDurationSeconds": distribution(
                [
                    float(evaluation.get("durationSeconds", 0))
                    for evaluation in original_evaluations
                ]
            ),
            "officialEvaluatorRuns": len(original_evaluations),
            "toolCalls": distribution(
                [float(result.get("toolCalls", 0)) for result in original_results]
            ),
            "emptyPatches": sum(row["originalEmptyPatch"] for row in task_rows),
            "policyViolations": sum(
                row["originalPolicyViolation"] for row in task_rows
            ),
            "providerErrors": sum(
                row["originalProviderError"] is not None for row in task_rows
            ),
            "budgetAborts": sum(
                bool(result.get("budgetAborted")) for result in original_results
            ),
            "timeoutAborts": sum(
                bool(result.get("timeoutAborted")) for result in original_results
            ),
        },
        "feedbackAssistedRfClm": {
            "protocolWarning": (
                "Uses one round of hidden official evaluator feedback and is not "
                "a standard one-submission SWE-bench score."
            ),
            "completedTasks": len(recovery_completed_rows),
            "resolvedTasks": recovery_resolved,
            "solveRateOverCompleted": (
                round(recovery_resolved / len(recovery_completed_rows), 6)
                if recovery_completed_rows
                else None
            ),
            "wilson95": wilson_interval(
                recovery_resolved,
                len(recovery_completed_rows),
            ),
            "repairAttempts": repair_attempts,
            "repairSuccesses": repair_successes,
            "repairSuccessRate": (
                round(repair_successes / repair_attempts, 6)
                if repair_attempts
                else None
            ),
            "repairTokens": summarize_result_tokens(recovery_results),
            "combinedReportedTokens": original_token_total + recovery_token_total,
            "incrementalReportedTokens": recovery_token_total,
            "incrementalTokenFractionVsOriginal": (
                round(recovery_token_total / original_token_total, 6)
                if original_token_total
                else None
            ),
            "repairDurationSeconds": distribution(
                [
                    float(result["latencySeconds"])
                    for result in recovery_results
                    if isinstance(result.get("latencySeconds"), (int, float))
                ]
            ),
            "recoveryEvaluatorDurationSeconds": distribution(
                [
                    float(evaluation.get("durationSeconds", 0))
                    for evaluation in recovery_evaluations
                ]
            ),
            "feedbackProbeEvaluatorDurationSeconds": distribution(
                [
                    float(evaluation.get("durationSeconds", 0))
                    for evaluation in feedback_evaluations
                ]
            ),
            "officialRecoveryEvaluatorRuns": len(recovery_evaluations),
            "officialFeedbackProbeRuns": len(feedback_evaluations),
        },
        "pairedComparison": {
            "tasks": len(paired_rows),
            "absoluteSolveRateDifference": (
                round(
                    statistics.mean(recovery_outcomes)
                    - statistics.mean(original_outcomes),
                    6,
                )
                if paired_rows
                else None
            ),
            "pairedBootstrap95": paired_bootstrap_interval(
                original_outcomes,
                recovery_outcomes,
            ),
            "bootstrapSamples": 10_000,
            "bootstrapSeed": BOOTSTRAP_SEED,
            "originalOnly": original_only,
            "recoveryOnly": recovery_only,
            "exactMcNemarPValue": exact_mcnemar_p_value(
                original_only,
                recovery_only,
            ),
        },
        "byStage": {},
        "dgmHistoricalReference": DGM_REFERENCE,
        "estimatedApiCost": estimate_api_cost(
            original_results,
            recovery_results,
            run_config,
        ),
        "taskResults": task_rows,
    }
    for stage in ("small", "medium", "big"):
        stage_rows = [row for row in task_rows if row["stage"] == stage]
        original_stage = [row for row in stage_rows if row["originalComplete"]]
        recovery_stage = [row for row in stage_rows if row["recoveryComplete"]]
        summary["byStage"][stage] = {
            "tasks": len(stage_rows),
            "originalCompleted": len(original_stage),
            "originalResolved": sum(row["originalResolved"] for row in original_stage),
            "recoveryCompleted": len(recovery_stage),
            "recoveryResolved": sum(row["recoveryResolved"] for row in recovery_stage),
        }
    atomic_json(output_root / "summary.json", summary)
    return summary


def estimate_from_pilot(pilot_path: Path) -> dict[str, Any]:
    pilot = load_json(pilot_path)
    original = pilot["systems"]["original_pi_isolated"]
    repair = pilot["systems"]["rf_clm_recovery"]
    pilot_tasks = original["total"]
    scale = 200 / pilot_tasks
    return {
        "source": str(pilot_path),
        "pilotTasks": pilot_tasks,
        "projectedOriginalReportedTokens": round(
            original["total_reported_tokens"] * scale
        ),
        "projectedOriginalSummedAgentSeconds": round(
            original["wall_seconds"] * scale,
            3,
        ),
        "projectedOriginalSerialHours": round(
            original["wall_seconds"] * scale / 3600,
            3,
        ),
        "projectedRepairTokensAtPilotAttemptRate": round(
            repair["repair_total_reported_tokens"] * scale
        ),
        "pricingStatus": (
            "Unknown. Model catalog prices are zero placeholders and must not "
            "be interpreted as free usage."
        ),
    }


def select_entries(
    manifest: dict[str, Any],
    instance_ids: list[str],
    max_tasks: int | None,
) -> list[dict[str, Any]]:
    records = manifest["records"]
    if instance_ids:
        selected = set(instance_ids)
        unknown = selected - {
            entry["record"]["instance_id"] for entry in records
        }
        if unknown:
            raise ValueError(f"Unknown instance IDs: {sorted(unknown)}")
        records = [
            entry for entry in records if entry["record"]["instance_id"] in selected
        ]
    if max_tasks is not None:
        records = records[:max_tasks]
    return records


def check_proxy(host: str, port: int) -> None:
    try:
        with socket.create_connection((host, port), timeout=2):
            return
    except OSError as error:
        raise RuntimeError(
            f"Model SSE proxy is not reachable at {host}:{port}. Start "
            "`python3 rollback_mvp/openai_buffered_sse_proxy.py` first."
        ) from error


def validate_runtime(args: argparse.Namespace) -> None:
    if not args.agent_dir.is_dir():
        raise FileNotFoundError(f"Agent directory not found: {args.agent_dir}")
    if not args.swebench_source.is_dir():
        raise FileNotFoundError(
            f"SWE-bench source not found: {args.swebench_source}"
        )
    if not os.environ.get("ROLLBACK_ENDPOINT_API_KEY"):
        raise RuntimeError("ROLLBACK_ENDPOINT_API_KEY is required for execution.")
    docker_capture(["info"], docker_host=args.docker_host)
    check_proxy(args.proxy_host, args.proxy_port)


def run_benchmark(args: argparse.Namespace) -> None:
    manifest, manifest_hash = load_manifest(args.manifest)
    output_root = args.output.resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    dataset_path, task_path = materialize_inputs(manifest, output_root)
    entries = select_entries(manifest, args.instance_id, args.max_tasks)
    estimate = estimate_from_pilot(args.pilot_results)
    atomic_json(output_root / "budget_estimate.json", estimate)
    run_config = {
        "schemaVersion": 1,
        "manifestSha256": manifest_hash,
        "protocol": args.protocol,
        "modelProvider": args.model_provider,
        "modelId": args.model_id,
        "piRunnerSha256": sha256_file(args.pi_runner),
        "repairRunnerSha256": sha256_file(args.repair_runner),
        "imageBuilderSha256": sha256_file(args.image_builder),
        "orchestratorSha256": sha256_file(Path(__file__).resolve()),
        "agentModelsSha256": sha256_file(args.agent_dir / "models.json"),
        "piCodingAgentPackageSha256": sha256_file(
            args.repo_root
            / "pi-rollback"
            / "node_modules"
            / "@earendil-works"
            / "pi-coding-agent"
            / "package.json"
        ),
        "swebenchRevision": args.swebench_revision,
        "maxTaskTokens": args.max_task_tokens,
        "maxOutputTokens": args.max_output_tokens,
        "agentTimeoutSeconds": args.agent_timeout_seconds,
        "repairTimeoutSeconds": args.repair_timeout_seconds,
        "evaluatorTimeoutSeconds": args.evaluator_timeout_seconds,
        "imageBuildTimeoutSeconds": args.image_build_timeout_seconds,
        "imageBuildRetries": args.image_build_retries,
        "imageBuildRetryDelaySeconds": args.image_build_retry_delay_seconds,
        "buildWheelhouse": (
            str(args.build_wheelhouse) if args.build_wheelhouse else None
        ),
        "globalTokenCap": args.global_token_cap,
        "globalWallSeconds": args.global_wall_seconds,
        "interTaskDelaySeconds": args.inter_task_delay_seconds,
        "costPerMillionTokens": {
            "input": args.input_cost_per_million,
            "output": args.output_cost_per_million,
            "cacheRead": args.cache_read_cost_per_million,
            "cacheWrite": args.cache_write_cost_per_million,
        },
        "selectedInstanceIds": [
            entry["record"]["instance_id"] for entry in entries
        ],
    }
    config_path = output_root / "run_config.json"
    if config_path.exists() and load_json(config_path) != run_config:
        raise ValueError(
            f"Run configuration differs from existing state: {config_path}"
        )
    atomic_json(config_path, run_config)

    if not args.execute:
        print(json.dumps({"mode": "dry-run", "config": run_config, "estimate": estimate}, indent=2))
        aggregate_results(manifest, manifest_hash, output_root)
        return
    if args.confirm_paid_run != PAID_CONFIRMATION:
        raise ValueError(
            f"Paid execution requires --confirm-paid-run {PAID_CONFIRMATION}"
        )
    if args.global_token_cap <= 0:
        raise ValueError("--global-token-cap must be positive for execution.")
    validate_runtime(args)

    run_state_path = output_root / "run_state.json"
    if not run_state_path.exists():
        atomic_json(
            run_state_path,
            {
                "schemaVersion": 1,
                "startedAtUnix": time.time(),
                "completedAtUnix": None,
            },
        )
    consecutive_errors = 0
    for index, entry in enumerate(entries, start=1):
        run_state = load_json(run_state_path)
        elapsed = time.time() - float(run_state["startedAtUnix"])
        tokens = existing_budget_tokens(output_root)
        if elapsed >= args.global_wall_seconds:
            print("Global wall-time cap reached before next task.", flush=True)
            break
        if tokens >= args.global_token_cap:
            print("Global reported-token cap reached before next task.", flush=True)
            break
        instance_id = entry["record"]["instance_id"]
        print(
            f"[{index}/{len(entries)}] {instance_id} "
            f"tokens={tokens}/{args.global_token_cap}",
            flush=True,
        )
        task_state_path = output_root / "tasks" / instance_id / "state.json"
        task_was_complete = bool(
            task_state_path.exists()
            and load_json(task_state_path).get("status") == "completed"
        )
        try:
            run_task(
                args,
                dataset_path,
                task_path,
                output_root,
                entry,
                manifest_hash,
            )
            consecutive_errors = 0
        except Exception as error:
            consecutive_errors += 1
            task_dir = output_root / "tasks" / instance_id
            update_task_state(
                task_dir,
                instance_id,
                "infrastructure_error",
                error=f"{type(error).__name__}: {error}",
            )
            print(f"[error] {instance_id}: {error}", flush=True)
            if consecutive_errors >= args.max_consecutive_errors:
                print("Stopping after consecutive infrastructure errors.", flush=True)
                break
        aggregate_results(manifest, manifest_hash, output_root)
        if not task_was_complete and args.inter_task_delay_seconds > 0:
            time.sleep(args.inter_task_delay_seconds)
    summary = aggregate_results(manifest, manifest_hash, output_root)
    run_state = load_json(run_state_path)
    run_state["completedAtUnix"] = time.time() if summary["complete"] else None
    atomic_json(run_state_path, run_state)
    summary = aggregate_results(manifest, manifest_hash, output_root)
    print(
        json.dumps(
            {
                "complete": summary["complete"],
                "originalPiOneShot": summary["originalPiOneShot"],
                "feedbackAssistedRfClm": summary["feedbackAssistedRfClm"],
                "pairedComparison": summary["pairedComparison"],
            },
            indent=2,
        )
    )


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("validate", "estimate", "aggregate", "run"),
    )
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--pilot-results",
        type=Path,
        default=repo_root
        / "research_output"
        / "clm_budgeted_evolution_20260924_125503"
        / "endpoint_small_results.json",
    )
    parser.add_argument("--instance-id", action="append", default=[])
    parser.add_argument("--max-tasks", type=int)
    parser.add_argument(
        "--protocol",
        choices=("original_only", "original_and_feedback"),
        default="original_and_feedback",
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-paid-run")
    parser.add_argument("--global-token-cap", type=int, default=0)
    parser.add_argument("--global-wall-seconds", type=int, default=86_400)
    parser.add_argument("--max-task-tokens", type=int, default=512_000)
    parser.add_argument("--max-output-tokens", type=int, default=65_536)
    parser.add_argument("--input-cost-per-million", type=float)
    parser.add_argument("--output-cost-per-million", type=float)
    parser.add_argument("--cache-read-cost-per-million", type=float)
    parser.add_argument("--cache-write-cost-per-million", type=float)
    parser.add_argument("--agent-timeout-seconds", type=int, default=3_600)
    parser.add_argument("--repair-timeout-seconds", type=int, default=900)
    parser.add_argument("--evaluator-timeout-seconds", type=int, default=1_800)
    parser.add_argument("--image-build-timeout-seconds", type=int, default=7_200)
    parser.add_argument("--image-build-retries", type=int, default=2)
    parser.add_argument("--image-build-retry-delay-seconds", type=float, default=30)
    parser.add_argument("--inter-task-delay-seconds", type=float, default=0)
    parser.add_argument("--max-consecutive-errors", type=int, default=3)
    parser.add_argument("--keep-workspaces", action="store_true")
    parser.add_argument("--keep-instance-images", action="store_true")
    parser.add_argument("--docker-host")
    parser.add_argument("--proxy-host", default="127.0.0.1")
    parser.add_argument("--proxy-port", type=int, default=8765)
    parser.add_argument("--node", default="node")
    parser.add_argument("--swebench-python", default=sys.executable)
    parser.add_argument("--repair-python", default=sys.executable)
    parser.add_argument(
        "--agent-dir",
        type=Path,
        default=repo_root
        / "research_output"
        / "clm_budgeted_evolution_20260924_125503"
        / "pi_home"
        / "agent",
    )
    parser.add_argument(
        "--swebench-source",
        type=Path,
        default=repo_root / "datasets" / "SWE-bench",
    )
    parser.add_argument(
        "--image-builder",
        type=Path,
        default=repo_root / "rollback_mvp" / "build_local_swebench_images.py",
    )
    parser.add_argument("--build-wheelhouse", type=Path)
    parser.add_argument(
        "--pi-runner",
        type=Path,
        default=repo_root / "rollback_mvp" / "pi_swe_runner.mjs",
    )
    parser.add_argument(
        "--repair-runner",
        type=Path,
        default=repo_root / "rollback_mvp" / "repair_slice_once.py",
    )
    parser.add_argument("--model-provider", default="rollback-deepseek")
    parser.add_argument("--model-id", default="byteplus/deepseek-v4-flash-ga")
    args = parser.parse_args()
    args.repo_root = repo_root
    args.agent_dir = args.agent_dir.resolve()
    args.swebench_source = args.swebench_source.resolve()
    args.image_builder = args.image_builder.resolve()
    if args.build_wheelhouse:
        args.build_wheelhouse = args.build_wheelhouse.resolve()
    args.pi_runner = args.pi_runner.resolve()
    args.repair_runner = args.repair_runner.resolve()
    args.swebench_revision = subprocess.run(
        ["git", "-C", str(args.swebench_source), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    return args


def main() -> None:
    args = parse_args()
    manifest, manifest_hash = load_manifest(args.manifest)
    if args.command == "validate":
        dataset_path, task_path = materialize_inputs(manifest, args.output.resolve())
        print(
            json.dumps(
                {
                    "valid": True,
                    "manifestSha256": manifest_hash,
                    "records": len(manifest["records"]),
                    "datasetPath": str(dataset_path),
                    "agentTaskPath": str(task_path),
                },
                indent=2,
            )
        )
    elif args.command == "estimate":
        print(json.dumps(estimate_from_pilot(args.pilot_results), indent=2))
    elif args.command == "aggregate":
        print(
            json.dumps(
                aggregate_results(
                    manifest,
                    manifest_hash,
                    args.output.resolve(),
                ),
                indent=2,
            )
        )
    else:
        run_benchmark(args)


if __name__ == "__main__":
    main()
