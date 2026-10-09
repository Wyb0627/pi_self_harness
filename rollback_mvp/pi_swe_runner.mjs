import { execFileSync, spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { constants, mkdirSync, readFileSync, realpathSync, writeFileSync } from "node:fs";
import {
	access,
	lstat,
	mkdir,
	readFile,
	readdir,
	realpath,
	stat,
	writeFile,
} from "node:fs/promises";
import { dirname, relative, resolve, sep } from "node:path";
import { parseArgs } from "node:util";
import { Type } from "typebox";
import {
	createAgentSession,
	DefaultResourceLoader,
	defineTool,
	ModelRuntime,
	SessionManager,
	SettingsManager,
	createEditToolDefinition,
	createFindToolDefinition,
	createGrepToolDefinition,
	createLsToolDefinition,
	createReadToolDefinition,
	createWriteToolDefinition,
} from "../pi-rollback/node_modules/@earendil-works/pi-coding-agent/dist/index.js";

const { values } = parseArgs({
	options: {
		"agent-dir": { type: "string" },
		"docker-host": { type: "string" },
		"exclude-prefix": {
			type: "string",
			multiple: true,
			default: [
				"tests/",
				"test/",
				"testing/",
				"repro.py",
				".pycompat/",
				".scratch/",
				".venv/",
				"venv/",
				"node_modules/",
			],
		},
		"instance-id": { type: "string" },
		"max-output-tokens": { type: "string", default: "65536" },
		"max-total-tokens": { type: "string", default: "512000" },
		"model-id": { type: "string", default: "byteplus/deepseek-v4-flash-ga" },
		"model-provider": { type: "string", default: "rollback-deepseek" },
		"no-shell": { type: "boolean", default: false },
		"output": { type: "string" },
		"sandbox-image": { type: "string" },
		"strategy-file": { type: "string", multiple: true, default: [] },
		"task-file": { type: "string" },
		"timeout-seconds": { type: "string", default: "3600" },
		"trace": { type: "string" },
		workspace: { type: "string" },
	},
	strict: true,
});

const required = ["agent-dir", "instance-id", "output", "task-file", "trace", "workspace"];
for (const name of required) {
	if (!values[name]) throw new Error(`--${name} is required.`);
}
const apiKey = process.env.ROLLBACK_ENDPOINT_API_KEY;
if (!apiKey) throw new Error("ROLLBACK_ENDPOINT_API_KEY is required.");
if (!values["no-shell"] && !values["sandbox-image"]) {
	throw new Error("--sandbox-image is required unless --no-shell is set.");
}

const agentDir = resolve(values["agent-dir"]);
const workspace = realpathSync(resolve(values.workspace));
const outputPath = resolve(values.output);
const tracePath = resolve(values.trace);
const maxOutputTokens = Number.parseInt(values["max-output-tokens"], 10);
const maxTotalTokens = Number.parseInt(values["max-total-tokens"], 10);
const timeoutMs = Number.parseInt(values["timeout-seconds"], 10) * 1000;
const tasks = JSON.parse(readFileSync(resolve(values["task-file"]), "utf8"));
const task = tasks.find((candidate) => candidate.instance_id === values["instance-id"]);
if (!task) throw new Error(`Unknown instance ID: ${values["instance-id"]}`);
const problem = task.problem_statement;
const taskForbiddenPaths = Array.isArray(task.forbidden_paths) ? task.forbidden_paths : [];
const strategy = values["strategy-file"]
	.map((path) => readFileSync(resolve(path), "utf8").trim())
	.filter(Boolean)
	.join("\n\n");
mkdirSync(dirname(outputPath), { recursive: true });
mkdirSync(dirname(tracePath), { recursive: true });
writeFileSync(tracePath, "");

const modelRuntime = await ModelRuntime.create({
	authPath: `${agentDir}/auth.json`,
	modelsPath: `${agentDir}/models.json`,
	modelsStorePath: `${agentDir}/models-store.json`,
});
await modelRuntime.setRuntimeApiKey(values["model-provider"], apiKey);
const model = modelRuntime.getModel(values["model-provider"], values["model-id"]);
if (!model) throw new Error(`Model unavailable: ${values["model-provider"]}/${values["model-id"]}`);

const settingsManager = SettingsManager.inMemory({
	compaction: { enabled: true },
	retry: { enabled: true, maxRetries: 2 },
});
const confinedReadOperations = {
	readFile: async (path) => readFile(await assertWorkspacePath(path, workspace)),
	access: async (path) => access(await assertWorkspacePath(path, workspace), constants.R_OK),
};
const confinedEditOperations = {
	readFile: async (path) => readFile(await assertWorkspacePath(path, workspace)),
	writeFile: async (path, content) => {
		await assertWorkspacePath(path, workspace, { allowMissing: true });
		await writeFile(path, content, "utf8");
	},
	access: async (path) =>
		access(await assertWorkspacePath(path, workspace), constants.R_OK | constants.W_OK),
};
const confinedWriteOperations = {
	writeFile: async (path, content) => {
		await assertWorkspacePath(path, workspace, { allowMissing: true });
		await writeFile(path, content, "utf8");
	},
	mkdir: async (path) => {
		await assertWorkspacePath(path, workspace, { allowMissing: true });
		await mkdir(path, { recursive: true });
	},
};
const confinedGrepOperations = {
	isDirectory: async (path) => (await stat(await assertWorkspacePath(path, workspace))).isDirectory(),
	readFile: async (path) => readFile(await assertWorkspacePath(path, workspace), "utf8"),
};
const confinedFindOperations = {
	exists: async (path) => {
		try {
			await assertWorkspacePath(path, workspace);
			return true;
		} catch (error) {
			if (error instanceof Error && error.message.startsWith("Path not found:")) return false;
			throw error;
		}
	},
	glob: async (pattern, path, options) => findWorkspaceFiles(pattern, path, workspace, options.limit),
};
const confinedLsOperations = {
	exists: confinedFindOperations.exists,
	stat: async (path) => stat(await assertWorkspacePath(path, workspace)),
	readdir: async (path) => readdir(await assertWorkspacePath(path, workspace)),
};
const confinedFileTools = [
	createReadToolDefinition(workspace, { operations: confinedReadOperations }),
	createEditToolDefinition(workspace, { operations: confinedEditOperations }),
	createWriteToolDefinition(workspace, { operations: confinedWriteOperations }),
	createGrepToolDefinition(workspace, { operations: confinedGrepOperations }),
	createFindToolDefinition(workspace, { operations: confinedFindOperations }),
	createLsToolDefinition(workspace, { operations: confinedLsOperations }),
];
const restrictedBash = defineTool({
	name: "sandbox_bash",
	label: "Sandbox Bash",
	description: "Run local commands in the task repository. Network, package installation, and Git history are blocked.",
	promptSnippet: "Run local repository commands and tests without network or Git history access",
	parameters: Type.Object({
		command: Type.String(),
		timeout: Type.Optional(Type.Number({ minimum: 1, maximum: 900 })),
	}),
	execute: async (toolCallId, params, signal, onUpdate) => {
		const rejected = rejectCommand(params.command, workspace);
		if (rejected) {
			return {
				content: [{ type: "text", text: `Command rejected: ${rejected}` }],
				details: { command: params.command, rejected },
			};
		}
		const sandboxCommand = params.command.split(workspace).join("/testbed");
		return runCommand(
			sandboxCommand,
			workspace,
			values["sandbox-image"],
			values["docker-host"],
			`${values["instance-id"]}-${toolCallId}`,
			Math.min(params.timeout ?? 120, 900),
			signal,
			onUpdate,
		);
	},
});
const resourceLoader = new DefaultResourceLoader({
	cwd: workspace,
	agentDir,
	settingsManager,
	noExtensions: true,
	noSkills: true,
	noPromptTemplates: true,
	noThemes: true,
	noContextFiles: true,
	appendSystemPrompt: [
		"Benchmark isolation: do not use network access, Git history, later releases, or external files. Do not modify tests. Work only from the task statement and current repository snapshot.",
		...(strategy ? [strategy] : []),
	],
});
await resourceLoader.reload();

const { session } = await createAgentSession({
	cwd: workspace,
	agentDir,
	model,
	thinkingLevel: "off",
	modelRuntime,
	tools: values["no-shell"]
		? ["read", "edit", "write", "grep", "find", "ls"]
		: ["read", "edit", "write", "grep", "find", "ls", "sandbox_bash"],
	customTools: values["no-shell"] ? confinedFileTools : [...confinedFileTools, restrictedBash],
	resourceLoader,
	sessionManager: SessionManager.inMemory(workspace),
	settingsManager,
});

let inputTokens = 0;
let outputTokens = 0;
let cacheReadTokens = 0;
let cacheWriteTokens = 0;
let toolCalls = 0;
let budgetAborted = false;
let timeoutAborted = false;
let providerError;
const startedAt = new Date();
const started = performance.now();

const unsubscribe = session.subscribe((event) => {
	writeFileSync(tracePath, `${JSON.stringify(event)}\n`, { flag: "a" });
	if (event.type === "tool_execution_end") toolCalls += 1;
	if (event.type !== "message_end" || event.message.role !== "assistant") return;
	if (event.message.stopReason === "error") {
		providerError = event.message.errorMessage ?? "Unknown provider error.";
	}
	inputTokens += event.message.usage.input;
	outputTokens += event.message.usage.output;
	cacheReadTokens += event.message.usage.cacheRead;
	cacheWriteTokens += event.message.usage.cacheWrite;
	const totalTokens = inputTokens + outputTokens + cacheReadTokens + cacheWriteTokens;
	if ((outputTokens > maxOutputTokens || totalTokens > maxTotalTokens) && !budgetAborted) {
		budgetAborted = true;
		void session.abort();
	}
});

const timeout = setTimeout(() => {
	timeoutAborted = true;
	void session.abort();
}, timeoutMs);

let error;
try {
	await session.prompt(
		`Work directly in the current repository and solve this issue.\n\n${problem}\n\n` +
			"Inspect the relevant code and implement the smallest correct fix. " +
			"Do not use Git history, network access, package downloads, or external files. " +
			"Do not add or modify tests. Run focused tests only when their dependencies are already available; " +
			"if dependencies are missing, reason from the code and finish without installing them. " +
			"Do not only describe a solution. Do not commit changes.",
	);
} catch (caught) {
	error = caught instanceof Error ? caught.stack ?? caught.message : String(caught);
} finally {
	clearTimeout(timeout);
	unsubscribe();
	session.dispose();
}

execFileSync("git", ["add", "-N", "--all"], { cwd: workspace, stdio: "ignore" });
const patch = execFileSync("git", ["diff", "--binary", "HEAD"], {
	cwd: workspace,
	encoding: "utf8",
	maxBuffer: 64 * 1024 * 1024,
});
const changedPaths = execFileSync("git", ["diff", "--name-only", "-z", "HEAD"], {
	cwd: workspace,
	encoding: "utf8",
	maxBuffer: 16 * 1024 * 1024,
})
	.split("\0")
	.filter(Boolean);
const forbiddenPaths = changedPaths.filter((path) =>
	isForbiddenEvaluationPath(path, values["exclude-prefix"], taskForbiddenPaths),
);
const allowedPaths = changedPaths.filter((path) => !forbiddenPaths.includes(path));
const evaluationPatch =
	allowedPaths.length > 0
		? execFileSync("git", ["diff", "--binary", "HEAD", "--", ...allowedPaths], {
				cwd: workspace,
				encoding: "utf8",
				maxBuffer: 64 * 1024 * 1024,
			})
		: "";
const forbiddenPatch =
	forbiddenPaths.length > 0
		? execFileSync("git", ["diff", "--binary", "HEAD", "--", ...forbiddenPaths], {
				cwd: workspace,
				encoding: "utf8",
				maxBuffer: 64 * 1024 * 1024,
			})
		: "";
const completedAt = new Date();
const result = {
	schemaVersion: 1,
	instanceId: values["instance-id"],
	modelProvider: values["model-provider"],
	modelId: values["model-id"],
	strategyHash: createHash("sha256").update(strategy).digest("hex"),
	noShell: values["no-shell"],
	sandboxImage: values["sandbox-image"] ?? null,
	startedAt: startedAt.toISOString(),
	completedAt: completedAt.toISOString(),
	durationMs: Math.round(performance.now() - started),
	inputTokens,
	outputTokens,
	cacheReadTokens,
	cacheWriteTokens,
	toolCalls,
	maxOutputTokens,
	maxTotalTokens,
	budgetAborted,
	timeoutAborted,
	providerError,
	error,
	policyViolations: forbiddenPatch
		? [
				{
					type: "forbidden-path-modification",
					patch: forbiddenPatch,
				},
			]
		: [],
	patch: evaluationPatch,
	fullPatch: patch,
};
writeFileSync(outputPath, `${JSON.stringify(result, null, 2)}\n`);
if (error || providerError) process.exitCode = 1;

function rejectCommand(command, cwd) {
	const withoutWorkspace = command.split(cwd).join("");
	const rules = [
		[/https?:\/\//i, "network URLs are disabled"],
		[/\b(curl|wget|ssh|scp|rsync)\b/i, "network commands are disabled"],
		[/\b(pip|pip3|npm|pnpm|yarn|brew|apt|apt-get|conda)\s+(install|download|add|view)\b/i, "package changes are disabled"],
		[/\bgit\s+(log|show|fetch|pull|clone|remote|branch|checkout|switch|reset|restore)\b/i, "Git history and state-changing commands are disabled"],
		[/\b(env\s+-u|unset)\b.*proxy/i, "proxy overrides are disabled"],
		[/\/tmp\//, "paths outside the task workspace are disabled"],
		[/\/(Users|private|opt|usr\/local)\//, "paths outside the task workspace are disabled"],
	];
	for (const [pattern, reason] of rules) {
		if (pattern.test(withoutWorkspace)) return reason;
	}
}

function isForbiddenEvaluationPath(path, excludedPrefixes, exactForbiddenPaths) {
	if (exactForbiddenPaths.includes(path)) return true;
	if (excludedPrefixes.some((prefix) => path === prefix.replace(/\/$/, "") || path.startsWith(prefix))) {
		return true;
	}
	const segments = path.split("/");
	const basename = segments.at(-1) ?? "";
	return (
		segments.some((segment) => segment === "test" || segment === "tests" || segment === "testing") ||
		basename === "conftest.py" ||
		basename.startsWith("test_") ||
		basename.endsWith("_test.py")
	);
}

function runCommand(command, cwd, image, dockerHost, executionId, timeoutSeconds, signal, onUpdate) {
	return new Promise((resolvePromise) => {
		const containerName = `pi-swe-${safeDockerName(executionId)}`;
		const dockerEnvironment = {
			...process.env,
			...(dockerHost ? { DOCKER_HOST: dockerHost } : {}),
		};
		const child = spawn("docker", [
			"run",
			"--rm",
			"--name",
			containerName,
			"--network",
			"none",
			"--cap-drop",
			"ALL",
			"--security-opt",
			"no-new-privileges",
			"--pids-limit",
			"512",
			"--read-only",
			"--tmpfs",
			"/tmp:rw,exec,nosuid,size=2g",
			"--tmpfs",
			"/root/.cache:rw,nosuid,size=1g",
			"--volume",
			`${cwd}:/testbed:rw`,
			"--workdir",
			"/testbed",
			"--env",
			"HOME=/tmp",
			"--env",
			"PIP_NO_INDEX=1",
			image,
			"/bin/bash",
			"-lc",
			command,
		], {
			env: dockerEnvironment,
		});
		let output = "";
		let timedOut = false;
		let aborted = false;
		const append = (chunk) => {
			output += chunk.toString();
			if (output.length > 100_000) output = output.slice(-100_000);
			onUpdate?.({ content: [{ type: "text", text: output }], details: { command } });
		};
		child.stdout.on("data", append);
		child.stderr.on("data", append);
		const timer = setTimeout(() => {
			timedOut = true;
			child.kill("SIGTERM");
		}, timeoutSeconds * 1000);
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
			if (timedOut || aborted) {
				try {
					execFileSync("docker", ["rm", "--force", containerName], {
						env: dockerEnvironment,
						stdio: "ignore",
					});
				} catch {}
			}
			const suffix = timedOut ? `\nCommand timed out after ${timeoutSeconds}s.` : "";
			resolvePromise({
				content: [{ type: "text", text: `${output}${suffix}` || "(no output)" }],
				details: { command, exitCode: code, signal: childSignal, timedOut },
			});
		});
	});
}

async function assertWorkspacePath(path, cwd, options = {}) {
	const absolutePath = resolve(path);
	const pathFromWorkspace = relative(cwd, absolutePath);
	if (pathFromWorkspace === ".." || pathFromWorkspace.startsWith(`..${sep}`) || resolve(cwd, pathFromWorkspace) !== absolutePath) {
		throw new Error(`Path outside task workspace: ${path}`);
	}

	const components = pathFromWorkspace.split(sep).filter(Boolean);
	let current = cwd;
	for (const component of components) {
		current = resolve(current, component);
		try {
			const info = await lstat(current);
			if (info.isSymbolicLink()) throw new Error(`Symbolic links are disabled: ${current}`);
		} catch (error) {
			if (error instanceof Error && "code" in error && error.code === "ENOENT") {
				if (options.allowMissing) return absolutePath;
				throw new Error(`Path not found: ${absolutePath}`);
			}
			throw error;
		}
	}
	const canonical = await realpath(absolutePath);
	const canonicalRelative = relative(cwd, canonical);
	if (canonicalRelative === ".." || canonicalRelative.startsWith(`..${sep}`)) {
		throw new Error(`Path outside task workspace: ${path}`);
	}
	return canonical;
}

async function findWorkspaceFiles(pattern, searchPath, workspacePath, limit) {
	const root = await assertWorkspacePath(searchPath, workspacePath);
	const matcher = globMatcher(pattern);
	const matches = [];
	const visit = async (directory, prefix) => {
		if (matches.length >= limit) return;
		const entries = await readdir(directory, { withFileTypes: true });
		entries.sort((left, right) => left.name.localeCompare(right.name));
		for (const entry of entries) {
			if (matches.length >= limit) return;
			if (entry.name === ".git" || entry.name === "node_modules") continue;
			const entryPath = resolve(directory, entry.name);
			const relativePath = prefix ? `${prefix}/${entry.name}` : entry.name;
			if (entry.isSymbolicLink()) continue;
			if (entry.isDirectory()) {
				await visit(entryPath, relativePath);
			} else if (entry.isFile() && matcher(relativePath, entry.name)) {
				matches.push(entryPath);
			}
		}
	};
	await visit(root, "");
	return matches;
}

function globMatcher(pattern) {
	const useFullPath = pattern.includes("/");
	let expression = "^";
	for (let index = 0; index < pattern.length; index += 1) {
		const character = pattern[index];
		if (character === "*" && pattern[index + 1] === "*") {
			if (pattern[index + 2] === "/") {
				expression += "(?:.*/)?";
				index += 2;
			} else {
				expression += ".*";
				index += 1;
			}
		} else if (character === "*") {
			expression += "[^/]*";
		} else if (character === "?") {
			expression += "[^/]";
		} else {
			expression += character.replace(/[|\\{}()[\]^$+?.]/g, "\\$&");
		}
	}
	expression += "$";
	const regex = new RegExp(expression);
	return (relativePath, basename) => regex.test(useFullPath ? relativePath : basename);
}

function safeDockerName(value) {
	const normalized = value.toLowerCase().replace(/[^a-z0-9_.-]+/g, "-").replace(/^[^a-z0-9]+/, "");
	const suffix = createHash("sha256").update(value).digest("hex").slice(0, 10);
	return `${normalized.slice(0, 45) || "task"}-${suffix}`;
}
