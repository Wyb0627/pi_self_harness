"""CLI for matched held-out DGM/P2 strategy-and-tool evolution."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rollback_mvp.dgm_evolve.experiment import (
    DgmPiExperiment,
    ExperimentConfig,
    RuntimePaths,
    require_paid_confirmation,
)


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("prepare", "preflight", "search", "endpoint"),
    )
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--import-p0-from",
        type=Path,
        help="Explicitly import an audited P0 panel during prepare only.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=repo_root
        / "research_output"
        / "clm_budgeted_evolution_20260924_125503"
        / "dgm_swebench_verified_200.v1.json",
    )
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
    parser.add_argument(
        "--pi-runner",
        type=Path,
        default=repo_root / "rollback_mvp" / "pi_swe_runner.mjs",
    )
    parser.add_argument(
        "--mutation-runner",
        type=Path,
        default=repo_root / "rollback_mvp" / "pi_strategy_mutator.mjs",
    )
    parser.add_argument(
        "--build-wheelhouse",
        type=Path,
        default=repo_root
        / "research_output"
        / "clm_budgeted_evolution_20260924_125503"
        / "dgm200_run"
        / "wheelhouse",
    )
    parser.add_argument(
        "--swebench-python",
        default="/tmp/pi-swebench-runtime/bin/python",
    )
    parser.add_argument("--node", default="node")
    parser.add_argument("--docker-host")
    parser.add_argument("--seed", type=int, default=20261014)
    parser.add_argument("--proposal-slots", type=int, default=10)
    parser.add_argument("--proposals-per-wave", type=int, default=2)
    parser.add_argument(
        "--search-token-cap",
        type=int,
        help="Optional search-wide token stop; omitted in the matched pilot.",
    )
    parser.add_argument("--search-active-seconds-cap", type=int, default=108_000)
    parser.add_argument("--endpoint-token-cap", type=int, default=80_000_000)
    parser.add_argument("--reference-token-cap", type=int, default=80_000_000)
    parser.add_argument("--endpoint-active-seconds-cap", type=int, default=108_000)
    parser.add_argument("--per-task-token-cap", type=int, default=512_000)
    parser.add_argument("--per-task-output-token-cap", type=int, default=65_536)
    parser.add_argument("--mutation-token-cap", type=int, default=64_000)
    parser.add_argument("--mutation-output-token-cap", type=int, default=32_768)
    parser.add_argument("--agent-timeout-seconds", type=int, default=3_600)
    parser.add_argument("--mutation-timeout-seconds", type=int, default=900)
    parser.add_argument("--evaluator-timeout-seconds", type=int, default=1_800)
    parser.add_argument("--inter-task-delay-seconds", type=float, default=90.0)
    parser.add_argument("--model-provider", default="rollback-deepseek")
    parser.add_argument("--model-id", default="byteplus/deepseek-v4-flash-ga")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--enable-rf-clm", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--confirm-paid-run")
    args = parser.parse_args()
    args.repo_root = repo_root
    return args


def build_config(args: argparse.Namespace) -> ExperimentConfig:
    if args.smoke:
        return ExperimentConfig(
            run_id=args.run_id,
            experiment_seed=args.seed,
            arm="p2" if args.enable_rf_clm else "dgm",
            model_provider=args.model_provider,
            model_id=args.model_id,
            proposal_slots=2,
            proposals_per_wave=2,
            search_token_cap=500_000,
            search_active_seconds_cap=7_200,
            final_endpoint_token_cap=250_000,
            reference_endpoint_token_cap=250_000,
            endpoint_active_seconds_cap=7_200,
            per_task_token_cap=64_000,
            per_task_output_token_cap=16_384,
            mutation_token_cap=32_000,
            mutation_output_token_cap=8_192,
            agent_timeout_seconds=900,
            mutation_timeout_seconds=600,
            evaluator_timeout_seconds=1_200,
            image_build_timeout_seconds=7_200,
            image_build_retries=2,
            image_build_retry_delay_seconds=30,
            inter_task_delay_seconds=0,
            smoke=True,
            smoke_small_tasks=1,
            smoke_medium_tasks=0,
            smoke_endpoint_tasks=2,
        )
    return ExperimentConfig(
        run_id=args.run_id,
        experiment_seed=args.seed,
        arm="p2" if args.enable_rf_clm else "dgm",
        model_provider=args.model_provider,
        model_id=args.model_id,
        proposal_slots=args.proposal_slots,
        proposals_per_wave=args.proposals_per_wave,
        search_token_cap=args.search_token_cap,
        search_active_seconds_cap=args.search_active_seconds_cap,
        final_endpoint_token_cap=args.endpoint_token_cap,
        reference_endpoint_token_cap=args.reference_token_cap,
        endpoint_active_seconds_cap=args.endpoint_active_seconds_cap,
        per_task_token_cap=args.per_task_token_cap,
        per_task_output_token_cap=args.per_task_output_token_cap,
        mutation_token_cap=args.mutation_token_cap,
        mutation_output_token_cap=args.mutation_output_token_cap,
        agent_timeout_seconds=args.agent_timeout_seconds,
        mutation_timeout_seconds=args.mutation_timeout_seconds,
        evaluator_timeout_seconds=args.evaluator_timeout_seconds,
        image_build_timeout_seconds=7_200,
        image_build_retries=2,
        image_build_retry_delay_seconds=30,
        inter_task_delay_seconds=args.inter_task_delay_seconds,
    )


def build_paths(args: argparse.Namespace) -> RuntimePaths:
    wheelhouse = args.build_wheelhouse.resolve()
    return RuntimePaths(
        repo_root=args.repo_root,
        full_manifest=args.manifest.resolve(),
        output_root=args.output.resolve(),
        agent_dir=args.agent_dir.resolve(),
        swebench_source=args.swebench_source.resolve(),
        image_builder=args.image_builder.resolve(),
        pi_runner=args.pi_runner.resolve(),
        mutation_runner=args.mutation_runner.resolve(),
        swebench_python=args.swebench_python,
        node=args.node,
        docker_host=args.docker_host,
        build_wheelhouse=wheelhouse if wheelhouse.is_dir() else None,
    )


def main() -> int:
    args = parse_args()
    experiment = DgmPiExperiment(build_config(args), build_paths(args))
    if args.command == "prepare":
        print(
            json.dumps(
                experiment.prepare(import_p0_from=args.import_p0_from),
                indent=2,
            )
        )
        return 0
    if args.import_p0_from is not None:
        raise SystemExit("--import-p0-from is valid only with prepare")
    protocol_lock = args.output.resolve() / "protocol-lock.json"
    if not protocol_lock.is_file():
        raise SystemExit(
            "Run prepare in a separate process before preflight/search/endpoint."
        )
    if args.command == "preflight":
        print(
            json.dumps(
                experiment.preflight(require_paid_runtime=args.execute),
                indent=2,
            )
        )
        return 0

    if not args.execute:
        raise SystemExit("search/endpoint require --execute")
    require_paid_confirmation(args.confirm_paid_run)
    with experiment.execution_lease(args.command):
        experiment.preflight(require_paid_runtime=True)
        if args.command == "search":
            print(json.dumps(experiment.run_search(), indent=2))
            return 0
        if args.command == "endpoint":
            print(json.dumps(experiment.run_endpoint(), indent=2))
            return 0
    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
