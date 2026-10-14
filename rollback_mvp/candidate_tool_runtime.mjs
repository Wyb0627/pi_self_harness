import { execFileSync, spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { lstatSync, readFileSync, realpathSync } from "node:fs";
import { relative, resolve, sep } from "node:path";
import { Type } from "typebox";
import { defineTool } from "../pi-rollback/node_modules/@earendil-works/pi-coding-agent/dist/index.js";

const TOOL_NAME = /^[a-z][a-z0-9_]{2,31}$/;
const PARAMETER_NAME = /^[a-z][a-zA-Z0-9_]{0,31}$/;
const RESERVED_NAMES = new Set([
	"bash",
	"edit",
	"find",
	"grep",
	"ls",
	"read",
	"sandbox_bash",
	"write",
]);
const MAX_TOOLS = 4;
const MAX_STDOUT = 100_000;
const MAX_STDERR = 20_000;

export function loadCandidateToolDefinitions({
	artifactPath,
	workspace,
	image,
	dockerHost,
	instanceId,
}) {
	const artifact = realpathSync(resolve(artifactPath));
	const taskWorkspace = realpathSync(resolve(workspace));
	const manifestPath = assertArtifactFile(resolve(artifact, "tools.json"), artifact);
	const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
	validateCandidateToolManifest(manifest);
	return manifest.tools.map((tool) => {
		const handler = assertArtifactFile(resolve(artifact, tool.handler), artifact);
		return defineTool({
			name: tool.name,
			label: tool.label,
			description: tool.description,
			promptSnippet: tool.description,
			parameters: Type.Unsafe(tool.parameters),
			executionMode: "sequential",
			execute: async (toolCallId, params, signal, onUpdate) =>
				runCandidateTool({
					taskWorkspace,
					image,
					dockerHost,
					instanceId,
					toolCallId,
					tool,
					handler,
					params,
					signal,
					onUpdate,
				}),
		});
	});
}

export function validateCandidateToolManifest(manifest) {
	if (
		!manifest ||
		typeof manifest !== "object" ||
		Array.isArray(manifest) ||
		Object.keys(manifest).sort().join("\0") !== "schema_version\0tools" ||
		manifest.schema_version !== 1 ||
		!Array.isArray(manifest.tools) ||
		manifest.tools.length > MAX_TOOLS
	) {
		throw new Error("Candidate tools.json has an invalid top-level schema.");
	}
	const names = new Set();
	for (const [index, tool] of manifest.tools.entries()) {
		validateTool(tool, index);
		if (names.has(tool.name)) throw new Error(`Duplicate candidate tool: ${tool.name}`);
		names.add(tool.name);
	}
	return manifest;
}

export function buildCandidateToolDockerArgs({
	taskWorkspace,
	image,
	containerName,
	handler,
}) {
	return [
		"run",
		"--rm",
		"--interactive",
		"--name",
		containerName,
		"--network",
		"none",
		"--cap-drop",
		"ALL",
		"--security-opt",
		"no-new-privileges",
		"--pids-limit",
		"128",
		"--memory",
		"2g",
		"--read-only",
		"--tmpfs",
		"/tmp:rw,nosuid,size=256m",
		"--tmpfs",
		"/testbed/.git:rw,nosuid,size=1m",
		"--volume",
		`${taskWorkspace}:/testbed:rw`,
		"--volume",
		`${handler}:/candidate/handler.py:ro`,
		"--workdir",
		"/testbed",
		"--env",
		"HOME=/tmp",
		"--env",
		"PYTHONDONTWRITEBYTECODE=1",
		"--env",
		"NO_PROXY=*",
		image,
		"/usr/bin/env",
		"python3",
		"/candidate/handler.py",
	];
}

export function runCandidateTool({
	taskWorkspace,
	image,
	dockerHost,
	instanceId,
	toolCallId,
	tool,
	handler,
	params,
	signal,
	onUpdate,
}) {
	return new Promise((resolvePromise) => {
		const containerName = safeDockerName(`pi-tool-${instanceId}-${toolCallId}`);
		const dockerEnvironment = {
			PATH: process.env.PATH,
			...(dockerHost ? { DOCKER_HOST: dockerHost } : {}),
		};
		const args = buildCandidateToolDockerArgs({
			taskWorkspace,
			image,
			containerName,
			handler,
		});
		const child = spawn("docker", args, {
			env: dockerEnvironment,
			stdio: ["pipe", "pipe", "pipe"],
		});
		let stdout = "";
		let stderr = "";
		let timedOut = false;
		let aborted = false;
		let overflow = false;
		const update = () => {
			const text = [stdout, stderr].filter(Boolean).join("\n").slice(-4_000);
			if (text) onUpdate?.({ content: [{ type: "text", text }], details: { tool: tool.name } });
		};
		child.stdout.on("data", (chunk) => {
			stdout += chunk.toString();
			if (stdout.length > MAX_STDOUT) {
				overflow = true;
				child.kill("SIGTERM");
			}
			update();
		});
		child.stderr.on("data", (chunk) => {
			stderr = `${stderr}${chunk.toString()}`.slice(-MAX_STDERR);
			update();
		});
		child.stdin.end(`${JSON.stringify(params)}\n`);
		const timer = setTimeout(() => {
			timedOut = true;
			child.kill("SIGTERM");
		}, tool.timeout_seconds * 1000);
		signal?.addEventListener(
			"abort",
			() => {
				aborted = true;
				child.kill("SIGTERM");
			},
			{ once: true },
		);
		child.on("close", (code, childSignal) => {
			clearTimeout(timer);
			if (timedOut || aborted || overflow) {
				try {
					execFileSync("docker", ["rm", "--force", containerName], {
						env: dockerEnvironment,
						stdio: "ignore",
					});
				} catch {}
			}
			const failure = timedOut
				? `Candidate tool timed out after ${tool.timeout_seconds}s.`
				: aborted
					? "Candidate tool was aborted."
					: overflow
						? "Candidate tool exceeded the output limit."
						: code !== 0
							? `Candidate tool exited with code ${code}.`
							: null;
			if (failure) {
				resolvePromise({
					content: [{ type: "text", text: `${failure}${stderr ? `\n${stderr}` : ""}` }],
					details: {
						tool: tool.name,
						exitCode: code,
						signal: childSignal,
						timedOut,
						aborted,
						overflow,
					},
				});
				return;
			}
			try {
				const parsed = parseHandlerOutput(stdout);
				resolvePromise({
					content: [{ type: "text", text: parsed.content }],
					details: { tool: tool.name, ...(parsed.details ?? {}) },
				});
			} catch (error) {
				resolvePromise({
					content: [
						{
							type: "text",
							text: `Candidate tool returned invalid output: ${
								error instanceof Error ? error.message : String(error)
							}`,
						},
					],
					details: { tool: tool.name, exitCode: code, invalidOutput: true },
				});
			}
		});
	});
}

function validateTool(tool, index) {
	const expected = [
		"description",
		"handler",
		"label",
		"name",
		"parameters",
		"timeout_seconds",
	];
	if (
		!tool ||
		typeof tool !== "object" ||
		Array.isArray(tool) ||
		Object.keys(tool).sort().join("\0") !== expected.join("\0")
	) {
		throw new Error(`Candidate tool ${index} has invalid fields.`);
	}
	if (!TOOL_NAME.test(tool.name) || RESERVED_NAMES.has(tool.name)) {
		throw new Error(`Candidate tool ${index} has an invalid or reserved name.`);
	}
	if (
		typeof tool.label !== "string" ||
		!tool.label.trim() ||
		tool.label.length > 80 ||
		typeof tool.description !== "string" ||
		!tool.description.trim() ||
		tool.description.length > 600
	) {
		throw new Error(`Candidate tool ${tool.name} has invalid human-readable metadata.`);
	}
	if (
		typeof tool.handler !== "string" ||
		tool.handler !== `handlers/${tool.name}.py` ||
		!Number.isInteger(tool.timeout_seconds) ||
		tool.timeout_seconds < 1 ||
		tool.timeout_seconds > 120
	) {
		throw new Error(`Candidate tool ${tool.name} has an invalid handler contract.`);
	}
	validateParameterSchema(tool.parameters, tool.name);
}

function validateParameterSchema(schema, toolName) {
	const expected = ["additionalProperties", "properties", "required", "type"];
	if (
		!schema ||
		typeof schema !== "object" ||
		Array.isArray(schema) ||
		Object.keys(schema).sort().join("\0") !== expected.join("\0") ||
		schema.type !== "object" ||
		schema.additionalProperties !== false ||
		!schema.properties ||
		typeof schema.properties !== "object" ||
		Array.isArray(schema.properties) ||
		Object.keys(schema.properties).length > 8 ||
		!Array.isArray(schema.required) ||
		new Set(schema.required).size !== schema.required.length
	) {
		throw new Error(`Candidate tool ${toolName} has an invalid parameter object schema.`);
	}
	for (const required of schema.required) {
		if (typeof required !== "string" || !(required in schema.properties)) {
			throw new Error(`Candidate tool ${toolName} has an invalid required parameter.`);
		}
	}
	for (const [name, definition] of Object.entries(schema.properties)) {
		if (!PARAMETER_NAME.test(name)) {
			throw new Error(`Candidate tool ${toolName} has an invalid parameter name.`);
		}
		const allowed = new Set(["description", "enum", "maximum", "minimum", "type"]);
		if (
			!definition ||
			typeof definition !== "object" ||
			Array.isArray(definition) ||
			Object.keys(definition).some((key) => !allowed.has(key)) ||
			!["string", "number", "integer", "boolean"].includes(definition.type)
		) {
			throw new Error(`Candidate tool ${toolName}.${name} has an unsupported schema.`);
		}
	}
}

function assertArtifactFile(path, artifact) {
	const resolved = resolve(path);
	const pathFromArtifact = relative(artifact, resolved);
	if (
		pathFromArtifact === ".." ||
		pathFromArtifact.startsWith(`..${sep}`) ||
		resolve(artifact, pathFromArtifact) !== resolved
	) {
		throw new Error(`Candidate artifact path escapes its root: ${path}`);
	}
	let current = artifact;
	for (const component of pathFromArtifact.split(sep).filter(Boolean)) {
		current = resolve(current, component);
		const info = lstatSync(current);
		if (info.isSymbolicLink()) throw new Error(`Candidate artifact contains a symlink: ${current}`);
	}
	const info = lstatSync(resolved);
	if (!info.isFile()) throw new Error(`Candidate artifact file is missing: ${resolved}`);
	const canonical = realpathSync(resolved);
	const canonicalRelative = relative(artifact, canonical);
	if (canonicalRelative === ".." || canonicalRelative.startsWith(`..${sep}`)) {
		throw new Error(`Candidate artifact file escapes its root: ${resolved}`);
	}
	return canonical;
}

function parseHandlerOutput(stdout) {
	const parsed = JSON.parse(stdout);
	const keys = Object.keys(parsed).sort();
	if (
		!parsed ||
		typeof parsed !== "object" ||
		Array.isArray(parsed) ||
		(keys.join("\0") !== "content" && keys.join("\0") !== "content\0details") ||
		typeof parsed.content !== "string" ||
		!parsed.content.trim() ||
		parsed.content.length > 80_000 ||
		(parsed.details !== undefined &&
			(!parsed.details || typeof parsed.details !== "object" || Array.isArray(parsed.details)))
	) {
		throw new Error("Expected {content: string, details?: object}.");
	}
	return parsed;
}

function safeDockerName(value) {
	const normalized = value.toLowerCase().replace(/[^a-z0-9_.-]+/g, "-").replace(/^[^a-z0-9]+/, "");
	const suffix = createHash("sha256").update(value).digest("hex").slice(0, 10);
	return `${normalized.slice(0, 45) || "candidate-tool"}-${suffix}`;
}
