"""Generate one bounded repair from a failed patch and executable feedback."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from llm_client import LLMClient


def parse_patch_paths(patch: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"^diff --git a/(.+?) b/", patch, re.MULTILINE)))


def apply_edits(workspace: Path, edits: list[dict[str, str]]) -> list[str]:
    changed: list[str] = []
    for edit in edits:
        relative = edit["path"]
        path = (workspace / relative).resolve()
        if not path.is_relative_to(workspace.resolve()):
            raise ValueError(f"Edit escapes workspace: {relative}")
        old = edit["old"]
        new = edit["new"]
        text = path.read_text()
        count = text.count(old)
        if count != 1:
            raise ValueError(f"Expected one exact match in {relative}, found {count}")
        path.write_text(text.replace(old, new, 1))
        changed.append(relative)
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-result", required=True)
    parser.add_argument("--candidate-path", action="append", default=[])
    parser.add_argument("--failure-file", required=True)
    parser.add_argument("--instance-id", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--task-file", required=True)
    parser.add_argument("--workspace", required=True)
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    baseline = json.loads(Path(args.baseline_result).read_text())
    tasks = json.loads(Path(args.task_file).read_text())
    task = next(row for row in tasks if row["instance_id"] == args.instance_id)
    candidate_paths = list(dict.fromkeys(args.candidate_path + parse_patch_paths(baseline.get("patch", ""))))
    if not candidate_paths:
        raise ValueError("The failed baseline has no changed source files to slice.")

    sources = []
    for relative in candidate_paths:
        path = (workspace / relative).resolve()
        if not path.is_relative_to(workspace) or not path.is_file():
            raise ValueError(f"Invalid candidate path: {relative}")
        sources.append(f"## {relative}\n```\n{path.read_text()[:120000]}\n```")

    system = """You repair a code patch after an executable evaluator rejected it.
Use only the supplied failure evidence and source slice. Return strict JSON:
{"edits":[{"path":"relative/path","old":"exact existing text","new":"replacement"}],"explanation":"brief"}
Each old string must occur exactly once. Make the smallest source-only repair.
Do not edit tests and do not rely on release history or external sources."""
    user = f"""# Task
{task["problem_statement"]}

# Rejected candidate patch
{baseline.get("patch", "")}

# Executable failure evidence
{Path(args.failure_file).read_text()}

# Causal source slice
{chr(10).join(sources)}
"""
    result = LLMClient().complete_json_with_telemetry(system, user, max_tokens=8192)
    edits = result.data.get("edits")
    if not isinstance(edits, list) or not edits:
        raise ValueError("Model returned no edits.")
    changed = apply_edits(workspace, edits)
    patch = subprocess.run(
        ["git", "diff", "--binary", "HEAD", "--", *changed],
        cwd=workspace,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    output = {
        "schemaVersion": 1,
        "instanceId": args.instance_id,
        "method": "repair-first-causal-slice",
        "candidatePaths": candidate_paths,
        "changedPaths": changed,
        "inputTokens": result.input_tokens,
        "outputTokens": result.output_tokens,
        "latencySeconds": result.latency_seconds,
        "attempts": result.attempts,
        "failureHash": hashlib.sha256(Path(args.failure_file).read_bytes()).hexdigest(),
        "patch": patch,
        "explanation": result.data.get("explanation", ""),
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
