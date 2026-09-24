import { execFileSync, spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { parseArgs } from "node:util";
import { Type } from "typebox";
import {
	createAgentSession,
	DefaultResourceLoader,
	defineTool,
	ModelRuntime,
	SessionManager,
	SettingsManager,
} from "../pi-rollback/node_modules/@earendil-works/pi-coding-agent/dist/index.js";

const { values } = parseArgs({
	options: {
		"agent-dir": { type: "string" },
		"exclude-prefix": {
			type: "string",
			multiple: true,
			default: ["tests/", "repro.py", ".pycompat/", ".scratch/", ".venv/", "venv/", "node_modules/"],
		},
		"instance-id": { type: "string" },
		"max-output-tokens": { type: "string", default: "65536" },
		"max-total-tokens": { type: "string", default: "512000" },
		"model-id": { type: "string", default: "byteplus/deepseek-v4-flash-ga" },
		"model-provider": { type: "string", default: "rollback-deepseek" },
		"no-shell": { type: "boolean", default: false },
		"output": { type: "string" },
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

const agentDir = resolve(values["agent-dir"]);
const workspace = resolve(values.workspace);
const outputPath = resolve(values.output);
const tracePath = resolve(values.trace);
const maxOutputTokens = Number.parseInt(values["max-output-tokens"], 10);
const maxTotalTokens = Number.parseInt(values["max-total-tokens"], 10);
const timeoutMs = Number.parseInt(values["timeout-seconds"], 10) * 1000;
const tasks = JSON.parse(readFileSync(resolve(values["task-file"]), "utf8"));
const task = tasks.find((candidate) => candidate.instance_id === values["instance-id"]);
if (!task) throw new Error(`Unknown instance ID: ${values["instance-id"]}`);
const problem = task.problem_statement;
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
const restrictedBash = defineTool({
	name: "sandbox_bash",
	label: "Sandbox Bash",
	description: "Run local commands in the task repository. Network, package installation, and Git history are blocked.",
	promptSnippet: "Run local repository commands and tests without network or Git history access",
	parameters: Type.Object({
		command: Type.String(),
		timeout: Type.Optional(Type.Number({ minimum: 1, maximum: 900 })),
	}),
	execute: async (_toolCallId, params, signal, onUpdate) => {
		const rejected = rejectCommand(params.command, workspace);
		if (rejected) {
			return {
				content: [{ type: "text", text: `Command rejected: ${rejected}` }],
				details: { command: params.command, rejected },
			};
		}
		return runCommand(params.command, workspace, Math.min(params.timeout ?? 120, 900), signal, onUpdate);
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
	customTools: values["no-shell"] ? [] : [restrictedBash],
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
const patchPathspec = [".", ...values["exclude-prefix"].map((prefix) => `:(exclude)${prefix}**`)];
const evaluationPatch = execFileSync("git", ["diff", "--binary", "HEAD", "--", ...patchPathspec], {
	cwd: workspace,
	encoding: "utf8",
	maxBuffer: 64 * 1024 * 1024,
});
const completedAt = new Date();
const result = {
	schemaVersion: 1,
	instanceId: values["instance-id"],
	modelProvider: values["model-provider"],
	modelId: values["model-id"],
	strategyHash: createHash("sha256").update(strategy).digest("hex"),
	noShell: values["no-shell"],
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

function runCommand(command, cwd, timeoutSeconds, signal, onUpdate) {
	return new Promise((resolvePromise) => {
		const child = spawn("/bin/bash", ["-lc", command], {
			cwd,
			env: {
				...process.env,
				ALL_PROXY: "http://127.0.0.1:9",
				HTTP_PROXY: "http://127.0.0.1:9",
				HTTPS_PROXY: "http://127.0.0.1:9",
				NO_PROXY: "",
			},
		});
		let output = "";
		let timedOut = false;
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
		signal?.addEventListener("abort", () => child.kill("SIGTERM"), { once: true });
		child.on("close", (code, childSignal) => {
			clearTimeout(timer);
			const suffix = timedOut ? `\nCommand timed out after ${timeoutSeconds}s.` : "";
			resolvePromise({
				content: [{ type: "text", text: `${output}${suffix}` || "(no output)" }],
				details: { command, exitCode: code, signal: childSignal, timedOut },
			});
		});
	});
}
