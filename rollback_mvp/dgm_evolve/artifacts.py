"""Validated strategy-and-tool artifacts for matched Pi evolution."""

from __future__ import annotations

import ast
import dataclasses
import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from rollback_mvp.adaptive_eval.schemas import hash_json


MAX_STRATEGY_PATCH_CHARS = 8_000
MAX_STRATEGY_CHARS = 32_000
MAX_HANDLER_CHARS = 16_000
MAX_TOOLS = 4
TASK_ID_PATTERN = re.compile(r"\b[a-zA-Z0-9_.-]+__[a-zA-Z0-9_.-]+-\d+\b")
TOOL_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]{2,31}$")
PARAMETER_NAME_PATTERN = re.compile(r"^[a-z][a-zA-Z0-9_]{0,31}$")
RESERVED_TOOL_NAMES = {
    "bash",
    "edit",
    "find",
    "grep",
    "ls",
    "read",
    "sandbox_bash",
    "write",
}
PROHIBITED_ARTIFACT_TEXT = (
    "swe-bench",
    "gold patch",
    "official evaluator",
    "test_patch",
    "pass_to_pass",
    "fail_to_pass",
)
ALLOWED_HANDLER_IMPORTS = {
    "ast",
    "collections",
    "difflib",
    "fnmatch",
    "hashlib",
    "json",
    "math",
    "os",
    "pathlib",
    "re",
    "statistics",
    "sys",
    "textwrap",
}
PROHIBITED_HANDLER_CALLS = {
    "__import__",
    "breakpoint",
    "compile",
    "delattr",
    "eval",
    "exec",
    "getattr",
    "globals",
    "locals",
    "setattr",
    "vars",
}
PROHIBITED_HANDLER_ATTRIBUTES = {
    "_getframe",
    "abort",
    "execl",
    "execle",
    "execlp",
    "execlpe",
    "execv",
    "execve",
    "execvp",
    "execvpe",
    "fork",
    "forkpty",
    "kill",
    "killpg",
    "modules",
    "popen",
    "posix_spawn",
    "posix_spawnp",
    "spawnl",
    "spawnle",
    "spawnlp",
    "spawnlpe",
    "spawnv",
    "spawnve",
    "spawnvp",
    "spawnvpe",
    "startfile",
    "system",
}


class ArtifactValidationError(ValueError):
    """A generated artifact violates the frozen mutable-surface contract."""


@dataclass(frozen=True, slots=True)
class CandidateTool:
    name: str
    label: str
    description: str
    parameters: dict[str, Any]
    handler_code: str
    timeout_seconds: int = 120

    @property
    def handler_path(self) -> str:
        return f"handlers/{self.name}.py"

    @property
    def manifest_entry(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "label": self.label,
            "description": self.description,
            "parameters": self.parameters,
            "handler": self.handler_path,
            "timeout_seconds": self.timeout_seconds,
        }


@dataclass(frozen=True, slots=True)
class MutationDelta:
    mutation_id: str
    repo: str
    entry_task_id: str
    mutation_summary: str
    strategy_patch: str
    tool: CandidateTool | None
    depends_on: tuple[str, ...] = ()

    @property
    def changed_paths(self) -> tuple[str, ...]:
        paths = []
        if self.strategy_patch:
            paths.append(f"strategy-sections/{self.mutation_id}.md")
        if self.tool is not None:
            paths.append(f"tools/{self.tool.name}")
        return tuple(paths)


@dataclass(frozen=True, slots=True)
class ArtifactContent:
    strategy: str
    tools: tuple[CandidateTool, ...]

    @property
    def tools_manifest(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "tools": [tool.manifest_entry for tool in self.tools],
        }

    @property
    def content_hash(self) -> str:
        return artifact_hash(self.strategy, self.tools)


def candidate_tool_from_json(value: object) -> CandidateTool:
    if not isinstance(value, dict):
        raise ArtifactValidationError("tool must be null or an object")
    expected = {
        "name",
        "label",
        "description",
        "parameters",
        "handler_code",
        "timeout_seconds",
    }
    if set(value) != expected:
        raise ArtifactValidationError(
            f"tool fields must be exactly {sorted(expected)}"
        )
    tool = CandidateTool(
        name=value["name"],
        label=value["label"],
        description=value["description"],
        parameters=value["parameters"],
        handler_code=value["handler_code"],
        timeout_seconds=value["timeout_seconds"],
    )
    validate_candidate_tool(tool, ())
    return tool


def mutation_delta_from_json(value: Mapping[str, Any]) -> MutationDelta:
    expected = {
        "mutation_id",
        "repo",
        "entry_task_id",
        "mutation_summary",
        "strategy_patch",
        "tool",
        "depends_on",
    }
    if set(value) != expected:
        raise ArtifactValidationError(
            f"Mutation delta fields must be exactly {sorted(expected)}"
        )
    tool_value = value["tool"]
    return MutationDelta(
        mutation_id=value["mutation_id"],
        repo=value["repo"],
        entry_task_id=value["entry_task_id"],
        mutation_summary=value["mutation_summary"],
        strategy_patch=value["strategy_patch"],
        tool=(
            None
            if tool_value is None
            else candidate_tool_from_json(tool_value)
        ),
        depends_on=tuple(value["depends_on"]),
    )


def mutation_delta_to_json(delta: MutationDelta) -> dict[str, Any]:
    return {
        **dataclasses.asdict(delta),
        "depends_on": list(delta.depends_on),
    }


def validate_strategy_text(
    strategy: str,
    evolve_task_ids: Sequence[str],
    *,
    patch: bool = False,
) -> None:
    if not isinstance(strategy, str):
        raise ArtifactValidationError("Strategy content must be a string")
    if patch and len(strategy) > MAX_STRATEGY_PATCH_CHARS:
        raise ArtifactValidationError("Strategy patch exceeds the frozen size limit")
    if not patch and len(strategy) > MAX_STRATEGY_CHARS:
        raise ArtifactValidationError("Composed strategy exceeds the frozen size limit")
    _validate_general_text(strategy, evolve_task_ids, "strategy")


def validate_candidate_tool(
    tool: CandidateTool,
    evolve_task_ids: Sequence[str],
) -> None:
    if not isinstance(tool.name, str) or not TOOL_NAME_PATTERN.fullmatch(tool.name):
        raise ArtifactValidationError("Tool name must match [a-z][a-z0-9_]{2,31}")
    if tool.name in RESERVED_TOOL_NAMES:
        raise ArtifactValidationError(f"Tool name is reserved: {tool.name}")
    for field_name in ("label", "description", "handler_code"):
        value = getattr(tool, field_name)
        if not isinstance(value, str) or not value.strip():
            raise ArtifactValidationError(f"Tool {field_name} must be non-empty")
        _validate_general_text(value, evolve_task_ids, f"tool.{field_name}")
    if len(tool.label) > 80 or len(tool.description) > 600:
        raise ArtifactValidationError("Tool label or description is too long")
    if len(tool.handler_code) > MAX_HANDLER_CHARS:
        raise ArtifactValidationError("Tool handler exceeds the frozen size limit")
    if (
        isinstance(tool.timeout_seconds, bool)
        or not isinstance(tool.timeout_seconds, int)
        or not 1 <= tool.timeout_seconds <= 120
    ):
        raise ArtifactValidationError("Tool timeout_seconds must be in [1, 120]")
    try:
        tree = ast.parse(tool.handler_code, filename=tool.handler_path)
    except SyntaxError as error:
        raise ArtifactValidationError(
            f"Tool handler is invalid Python: {error.msg}"
        ) from error
    _validate_handler_ast(tree)
    validate_parameter_schema(tool.parameters, evolve_task_ids)


def validate_mutation_delta(
    delta: MutationDelta,
    evolve_task_ids: Sequence[str],
) -> None:
    for name in ("mutation_id", "repo", "entry_task_id", "mutation_summary"):
        value = getattr(delta, name)
        if not isinstance(value, str) or not value.strip():
            raise ArtifactValidationError(f"{name} must be non-empty")
    if not re.fullmatch(r"m-\d{4}-[0-9a-f]{12}", delta.mutation_id):
        raise ArtifactValidationError("mutation_id has an invalid frozen format")
    if delta.entry_task_id not in evolve_task_ids:
        raise ArtifactValidationError("Mutation entry task is outside D_evolve")
    if not isinstance(delta.depends_on, tuple) or len(delta.depends_on) != len(
        set(delta.depends_on)
    ):
        raise ArtifactValidationError("depends_on must contain unique mutation IDs")
    _validate_general_text(
        delta.mutation_summary, evolve_task_ids, "mutation_summary"
    )
    validate_strategy_text(delta.strategy_patch, evolve_task_ids, patch=True)
    if delta.tool is not None:
        validate_candidate_tool(delta.tool, evolve_task_ids)
    if not delta.strategy_patch.strip() and delta.tool is None:
        raise ArtifactValidationError("Mutation must change strategy or one tool")


def validate_parameter_schema(
    schema: object,
    evolve_task_ids: Sequence[str] = (),
) -> None:
    if not isinstance(schema, dict):
        raise ArtifactValidationError("Tool parameters must be an object schema")
    expected = {"type", "properties", "required", "additionalProperties"}
    if set(schema) != expected:
        raise ArtifactValidationError(
            f"Tool parameter schema fields must be exactly {sorted(expected)}"
        )
    properties = schema.get("properties")
    required = schema.get("required")
    if (
        schema.get("type") != "object"
        or schema.get("additionalProperties") is not False
        or not isinstance(properties, dict)
        or len(properties) > 8
        or not isinstance(required, list)
        or not all(isinstance(item, str) for item in required)
        or len(required) != len(set(required))
        or set(required) - set(properties)
    ):
        raise ArtifactValidationError("Tool parameter object schema is invalid")
    for name, definition in properties.items():
        if not isinstance(name, str) or not PARAMETER_NAME_PATTERN.fullmatch(name):
            raise ArtifactValidationError(f"Invalid tool parameter name: {name!r}")
        _validate_parameter_definition(definition, name, evolve_task_ids)


def materialize_lineage(
    lineage: Sequence[MutationDelta],
    evolve_task_ids: Sequence[str],
) -> ArtifactContent:
    mutation_ids: set[str] = set()
    strategy_sections: list[str] = []
    tools: dict[str, CandidateTool] = {}
    for delta in lineage:
        validate_mutation_delta(delta, evolve_task_ids)
        if delta.mutation_id in mutation_ids:
            raise ArtifactValidationError(
                f"Duplicate mutation ID in lineage: {delta.mutation_id}"
            )
        missing = set(delta.depends_on) - mutation_ids
        if missing:
            raise ArtifactValidationError(
                f"Mutation depends on absent earlier mutations: {sorted(missing)}"
            )
        mutation_ids.add(delta.mutation_id)
        if delta.strategy_patch.strip():
            strategy_sections.append(delta.strategy_patch.strip())
        if delta.tool is not None:
            tools[delta.tool.name] = delta.tool
    if len(tools) > MAX_TOOLS:
        raise ArtifactValidationError(
            f"Artifact exceeds the {MAX_TOOLS}-tool frozen limit"
        )
    strategy = "\n\n".join(strategy_sections)
    validate_strategy_text(strategy, evolve_task_ids)
    ordered_tools = tuple(tools[name] for name in sorted(tools))
    return ArtifactContent(strategy=strategy, tools=ordered_tools)


def artifact_hash(
    strategy: str,
    tools: Sequence[CandidateTool] = (),
) -> str:
    return hash_json(
        {
            "strategy.md": strategy,
            "tools": [
                {
                    "manifest": tool.manifest_entry,
                    "handler_code": tool.handler_code,
                }
                for tool in sorted(tools, key=lambda item: item.name)
            ],
        }
    )


def _validate_parameter_definition(
    value: object,
    name: str,
    evolve_task_ids: Sequence[str],
) -> None:
    if not isinstance(value, dict):
        raise ArtifactValidationError(f"Tool parameter {name} must be an object")
    allowed = {"type", "description", "enum", "minimum", "maximum"}
    if set(value) - allowed or "type" not in value:
        raise ArtifactValidationError(f"Tool parameter {name} has unsupported fields")
    kind = value["type"]
    if kind not in {"string", "number", "integer", "boolean"}:
        raise ArtifactValidationError(
            f"Tool parameter {name} has unsupported type {kind!r}"
        )
    description = value.get("description")
    if description is not None and (
        not isinstance(description, str) or len(description) > 300
    ):
        raise ArtifactValidationError(
            f"Tool parameter {name} description is invalid"
        )
    if description is not None:
        _validate_general_text(
            description,
            evolve_task_ids,
            f"tool.parameters.{name}.description",
        )
    enum = value.get("enum")
    if enum is not None:
        if (
            not isinstance(enum, list)
            or not enum
            or len(enum) > 20
            or any(
                isinstance(item, (dict, list))
                or item is None
                or (
                    kind == "string"
                    and not isinstance(item, str)
                )
                or (
                    kind == "boolean"
                    and not isinstance(item, bool)
                )
                or (
                    kind in {"number", "integer"}
                    and (
                        isinstance(item, bool)
                        or not isinstance(item, (int, float))
                    )
                )
                for item in enum
            )
        ):
            raise ArtifactValidationError(f"Tool parameter {name} enum is invalid")
        for item in enum:
            if isinstance(item, str):
                _validate_general_text(
                    item,
                    evolve_task_ids,
                    f"tool.parameters.{name}.enum",
                )
    for bound in ("minimum", "maximum"):
        if bound in value and (
            isinstance(value[bound], bool)
            or not isinstance(value[bound], (int, float))
        ):
            raise ArtifactValidationError(
                f"Tool parameter {name} {bound} must be numeric"
            )
    if kind in {"string", "boolean"} and {
        "minimum",
        "maximum",
    } & set(value):
        raise ArtifactValidationError(
            f"Tool parameter {name} cannot use numeric bounds"
        )


def _validate_handler_ast(tree: ast.AST) -> None:
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            if any(alias.name == "*" for alias in node.names):
                raise ArtifactValidationError(
                    "Tool handler wildcard imports are not allowed"
                )
            names = (
                [alias.name for alias in node.names]
                if isinstance(node, ast.Import)
                else [node.module or ""]
            )
            for imported in names:
                root = imported.split(".", 1)[0]
                if root not in ALLOWED_HANDLER_IMPORTS:
                    raise ArtifactValidationError(
                        f"Tool handler import is not allowed: {imported}"
                    )
            if (
                isinstance(node, ast.ImportFrom)
                and (node.module or "").split(".", 1)[0] == "os"
            ):
                for alias in node.names:
                    if alias.name in PROHIBITED_HANDLER_ATTRIBUTES:
                        raise ArtifactValidationError(
                            "Tool handler os process import is not allowed: "
                            f"{alias.name}"
                        )
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in PROHIBITED_HANDLER_CALLS:
                raise ArtifactValidationError(
                    f"Tool handler call is not allowed: {node.func.id}"
                )
        if isinstance(node, ast.Name) and node.id in PROHIBITED_HANDLER_CALLS:
            raise ArtifactValidationError(
                f"Tool handler dynamic name is not allowed: {node.id}"
            )
        if isinstance(node, ast.Attribute):
            if node.attr.startswith("__"):
                raise ArtifactValidationError(
                    f"Tool handler dunder access is not allowed: {node.attr}"
                )
            if node.attr in PROHIBITED_HANDLER_ATTRIBUTES:
                raise ArtifactValidationError(
                    f"Tool handler process access is not allowed: {node.attr}"
                )


def _validate_general_text(
    value: str,
    evolve_task_ids: Sequence[str],
    field_name: str,
) -> None:
    lowered = value.lower()
    if any(term in lowered for term in PROHIBITED_ARTIFACT_TEXT):
        raise ArtifactValidationError(
            f"{field_name} contains benchmark-specific text"
        )
    if TASK_ID_PATTERN.search(value) or any(
        instance_id in value for instance_id in evolve_task_ids
    ):
        raise ArtifactValidationError(f"{field_name} contains an explicit task ID")
