"""Build SWE-bench instance images from exact, shallow local checkouts."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
import time
from pathlib import Path

from swebench.harness.test_spec import TestSpec, make_test_spec  # type: ignore[import-not-found]
from swebench.harness.utils import load_swebench_dataset  # type: ignore[import-not-found]


REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
FROM_PATTERN = re.compile(r"^(FROM(?:\s+--platform=\S+)?\s+)(\S+)", re.MULTILINE)


def run(command: list[str], *, cwd: Path | None = None) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def image_exists(image: str) -> bool:
    result = subprocess.run(
        ["docker", "image", "inspect", image],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def docker_platform(spec: TestSpec) -> str:
    return "linux/amd64" if spec.arch == "x86_64" else spec.platform


def expected_architecture(spec: TestSpec) -> str:
    return "amd64" if spec.arch == "x86_64" else spec.arch


def image_architecture(image: str) -> str | None:
    result = subprocess.run(
        ["docker", "image", "inspect", "--format", "{{.Architecture}}", image],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def normalize_dockerfile_platform(dockerfile: str) -> str:
    return dockerfile.replace("linux/x86_64", "linux/amd64")


def pin_dockerfile_source(dockerfile: str, spec: TestSpec) -> str:
    dockerfile = normalize_dockerfile_platform(dockerfile)
    match = FROM_PATTERN.search(dockerfile)
    if match is None:
        raise ValueError("Dockerfile has no FROM instruction.")
    source = match.group(2)
    if image_architecture(source) == expected_architecture(spec):
        return dockerfile

    safe_source = re.sub(r"[^a-z0-9_.-]+", "-", source.lower()).strip("-")
    alias = f"sweb.source.{expected_architecture(spec)}.{safe_source}"
    if image_architecture(alias) != expected_architecture(spec):
        container_id = run(
            [
                "docker",
                "create",
                "--platform",
                docker_platform(spec),
                source,
                "true",
            ]
        )
        try:
            run(["docker", "commit", container_id, alias])
        finally:
            run(["docker", "rm", "--force", container_id])
    return dockerfile[: match.start(2)] + alias + dockerfile[match.end(2) :]


def build_docker_context(
    image: str,
    platform_name: str,
    context: Path,
    log_path: Path,
) -> None:
    with log_path.open("w") as log:
        process = subprocess.Popen(
            [
                "docker",
                "build",
                "--platform",
                platform_name,
                "--tag",
                image,
                ".",
            ],
            cwd=context,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if process.stdout is None:
            raise RuntimeError("Docker build did not expose stdout.")
        for line in process.stdout:
            print(line, end="", flush=True)
            log.write(line)
            log.flush()
        return_code = process.wait()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, process.args)


def ensure_environment_images(
    spec: TestSpec,
    log_dir: Path,
) -> list[dict[str, object]]:
    images = [
        (spec.base_image_key, spec.base_dockerfile, {}),
        (
            spec.env_image_key,
            spec.env_dockerfile,
            {"setup_env.sh": spec.setup_env_script},
        ),
    ]
    results = []
    for image, dockerfile, files in images:
        architecture = image_architecture(image)
        if architecture == expected_architecture(spec):
            results.append(
                {
                    "image": image,
                    "architecture": architecture,
                    "status": "reused",
                }
            )
            continue
        if architecture is not None:
            run(["docker", "image", "rm", "--force", image])
        started = time.monotonic()
        log_path = log_dir / f"{image.replace(':', '__')}.build.log"
        with tempfile.TemporaryDirectory(prefix="sweb-prerequisite-") as tmp:
            context = Path(tmp)
            (context / "Dockerfile").write_text(
                pin_dockerfile_source(dockerfile, spec)
            )
            for filename, contents in files.items():
                (context / filename).write_text(contents)
            build_docker_context(
                image,
                docker_platform(spec),
                context,
                log_path,
            )
        architecture = image_architecture(image)
        if architecture != expected_architecture(spec):
            raise ValueError(
                f"Expected {image} architecture {expected_architecture(spec)}, "
                f"found {architecture}"
            )
        results.append(
            {
                "image": image,
                "architecture": architecture,
                "status": "built",
                "duration_seconds": round(time.monotonic() - started, 3),
                "log": str(log_path),
            }
        )
    return results


def checkout_exact_commit(spec: TestSpec, base_commit: str, destination: Path) -> None:
    if not REPO_PATTERN.fullmatch(spec.repo):
        raise ValueError(f"Invalid GitHub repository name: {spec.repo}")
    run(["git", "init", "--quiet", str(destination)])
    run(
        ["git", "remote", "add", "origin", f"https://github.com/{spec.repo}.git"],
        cwd=destination,
    )
    run(
        ["git", "fetch", "--depth", "2", "--no-tags", "origin", base_commit],
        cwd=destination,
    )
    run(["git", "checkout", "--quiet", "--detach", "FETCH_HEAD"], cwd=destination)
    run(["git", "remote", "remove", "origin"], cwd=destination)
    actual_commit = run(["git", "rev-parse", "HEAD"], cwd=destination)
    if actual_commit != base_commit:
        raise ValueError(
            f"Expected {base_commit} for {spec.instance_id}, found {actual_commit}"
        )


def local_setup_script(spec: TestSpec, base_commit: str) -> str:
    try:
        remote_remove_index = spec.repo_script_list.index("git remote remove origin")
    except ValueError as error:
        raise ValueError(
            f"Unexpected official repository setup for {spec.instance_id}"
        ) from error
    remaining_commands = spec.repo_script_list[remote_remove_index + 1 :]
    commands = [
        "#!/bin/bash",
        "set -euxo pipefail",
        f'test "$(git -C /testbed rev-parse HEAD)" = "{base_commit}"',
        'test -z "$(git -C /testbed remote)"',
        "chmod -R 777 /testbed",
        "cd /testbed",
        f"git reset --hard {base_commit}",
        *remaining_commands,
    ]
    return "\n".join(commands) + "\n"


def local_dockerfile(spec: TestSpec) -> str:
    return (
        f"FROM --platform={docker_platform(spec)} {spec.env_image_key}\n\n"
        "COPY ./repo /testbed\n"
        "COPY ./setup_local_repo.sh /root/\n"
        "RUN /bin/bash /root/setup_local_repo.sh\n\n"
        "WORKDIR /testbed/\n"
    )


def build_image(
    row: dict[str, object],
    spec: TestSpec,
    log_dir: Path,
    force: bool,
) -> dict[str, object]:
    base_commit = str(row["base_commit"])
    image = spec.instance_image_key
    architecture = image_architecture(image)
    if architecture == expected_architecture(spec) and not force:
        return {
            "instance_id": spec.instance_id,
            "base_commit": base_commit,
            "env_image": spec.env_image_key,
            "instance_image": image,
            "architecture": architecture,
            "history_depth": 2,
            "status": "reused",
        }
    if architecture is not None and architecture != expected_architecture(spec):
        run(["docker", "image", "rm", "--force", image])
    env_architecture = image_architecture(spec.env_image_key)
    if env_architecture is None:
        raise ValueError(
            f"Missing environment image {spec.env_image_key} for {spec.instance_id}"
        )
    if env_architecture != expected_architecture(spec):
        raise ValueError(
            f"Expected {spec.env_image_key} architecture "
            f"{expected_architecture(spec)}, found {env_architecture}"
        )
    if force and image_exists(image):
        run(["docker", "image", "rm", "--force", image])

    started = time.monotonic()
    log_path = log_dir / f"{spec.instance_id}.build.log"
    with tempfile.TemporaryDirectory(prefix=f"sweb-local-{spec.instance_id}-") as tmp:
        context = Path(tmp)
        repo = context / "repo"
        checkout_exact_commit(spec, base_commit, repo)
        (context / "setup_local_repo.sh").write_text(
            local_setup_script(spec, base_commit)
        )
        (context / "Dockerfile").write_text(local_dockerfile(spec))
        build_docker_context(
            image,
            docker_platform(spec),
            context,
            log_path,
        )
    architecture = image_architecture(image)
    if architecture != expected_architecture(spec):
        raise ValueError(
            f"Expected {image} architecture {expected_architecture(spec)}, "
            f"found {architecture}"
        )

    return {
        "instance_id": spec.instance_id,
        "base_commit": base_commit,
        "env_image": spec.env_image_key,
        "instance_image": image,
        "architecture": architecture,
        "history_depth": 2,
        "status": "built",
        "duration_seconds": round(time.monotonic() - started, 3),
        "log": str(log_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset", default="princeton-nlp/SWE-bench_Verified"
    )
    parser.add_argument("--build-missing-env", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--instance-id", action="append", required=True)
    parser.add_argument("--log-dir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--split", default="test")
    args = parser.parse_args()

    log_dir = Path(args.log_dir).resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    rows = load_swebench_dataset(
        args.dataset,
        args.split,
        args.instance_id,
    )
    rows_by_id = {str(row["instance_id"]): row for row in rows}
    specs_by_id = {
        instance_id: make_test_spec(rows_by_id[instance_id])
        for instance_id in args.instance_id
    }
    prerequisites = []
    if args.build_missing_env:
        seen = set()
        for spec in specs_by_id.values():
            if spec.env_image_key in seen:
                continue
            prerequisites.extend(ensure_environment_images(spec, log_dir))
            seen.add(spec.env_image_key)
    results = []
    for instance_id in args.instance_id:
        row = rows_by_id[instance_id]
        spec = specs_by_id[instance_id]
        print(f"Building {spec.instance_image_key} from {row['base_commit']}")
        results.append(build_image(row, spec, log_dir, args.force))

    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "prerequisite_images": prerequisites,
                "images": results,
            },
            indent=2,
        )
        + "\n"
    )


if __name__ == "__main__":
    main()
