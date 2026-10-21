"""Command-line validation entry points for adaptive evaluation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .catalogue import load_frozen_catalogue
from .schemas import AdaptiveEvalError


DEFAULT_MANIFEST = (
    Path(__file__).resolve().parents[2]
    / "research_output"
    / "clm_budgeted_evolution_20260924_125503"
    / "dgm_swebench_verified_200.v1.json"
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fail-closed DGM-style Pi adaptive evaluation controller"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate-catalogue")
    validate.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    subparsers.add_parser("container-preflight")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate-catalogue":
            catalogue = load_frozen_catalogue(args.manifest)
            print(
                json.dumps(
                    {
                        "status": "valid",
                        "tasks": len(catalogue.task_ids),
                        "dataset_manifest_hash": catalogue.dataset_manifest_hash,
                        "ordered_ids_hash": catalogue.ordered_ids_hash,
                        "catalogue_hash": catalogue.catalogue_hash,
                    },
                    indent=2,
                )
            )
            return 0
        if args.command == "container-preflight":
            raise AdaptiveEvalError(
                "production container execution is blocked until a complete digest-pinned "
                "invocation can attest restricted proxy enforcement, quota-backed mounts, "
                "fresh workspaces, and timeout cleanup"
            )
        raise AssertionError(f"Unhandled command: {args.command}")
    except AdaptiveEvalError as error:
        print(json.dumps({"status": "invalid", "error": str(error)}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
