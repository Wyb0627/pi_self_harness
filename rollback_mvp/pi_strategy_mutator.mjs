import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { parseArgs } from "node:util";
import {
	createAgentSession,
	DefaultResourceLoader,
	ModelRuntime,
	SessionManager,
	SettingsManager,
} from "../pi-rollback/node_modules/@earendil-works/pi-coding-agent/dist/index.js";

const { values } = parseArgs({
	options: {
		"agent-dir": { type: "string" },
		"evidence-file": { type: "string" },
		"max-output-tokens": { type: "string", default: "32768" },
		"max-total-tokens": { type: "string", default: "64000" },
		"model-id": { type: "string", default: "byteplus/deepseek-v4-flash-ga" },
		"model-provider": { type: "string", default: "rollback-deepseek" },
		output: { type: "string" },
		"timeout-seconds": { type: "string", default: "900" },
		trace: { type: "string" },
	},
	strict: true,
});

for (const name of ["agent-dir", "evidence-file", "output", "trace"]) {
	if (!values[name]) throw new Error(`--${name} is required.`);
}
const apiKey = process.env.ROLLBACK_ENDPOINT_API_KEY;
if (!apiKey) throw new Error("ROLLBACK_ENDPOINT_API_KEY is required.");

const agentDir = resolve(values["agent-dir"]);
const evidencePath = resolve(values["evidence-file"]);
const outputPath = resolve(values.output);
const tracePath = resolve(values.trace);
const maxOutputTokens = Number.parseInt(values["max-output-tokens"], 10);
const maxTotalTokens = Number.parseInt(values["max-total-tokens"], 10);
const timeoutMs = Number.parseInt(values["timeout-seconds"], 10) * 1000;
const evidenceText = readFileSync(evidencePath, "utf8");
const evidence = JSON.parse(evidenceText);
mkdirSync(dirname(outputPath), { recursive: true });
mkdirSync(dirname(tracePath), { recursive: true });
writeFileSync(tracePath, "");

const modelRuntime = await ModelRuntime.create({
	authPath: `${agentDir}/auth.json`,
	modelsPath: `${agentDir}/models.json`,
	modelsStorePath: `${agentDir}/models-store.json`,
});
await modelRuntime.setRuntimeApiKey(values["model-provider"], apiKey);
const configuredModel = modelRuntime.getModel(values["model-provider"], values["model-id"]);
if (!configuredModel) {
	throw new Error(`Model unavailable: ${values["model-provider"]}/${values["model-id"]}`);
}
const model = { ...configuredModel, maxTokens: maxOutputTokens };
const settingsManager = SettingsManager.inMemory({
	compaction: { enabled: false },
	retry: {
		enabled: true,
		maxRetries: 5,
		baseDelayMs: 5000,
		maxAgentDelayMs: 60000,
	},
});
const resourceLoader = new DefaultResourceLoader({
	cwd: dirname(evidencePath),
	agentDir,
	settingsManager,
	noExtensions: true,
	noSkills: true,
	noPromptTemplates: true,
	noThemes: true,
	noContextFiles: true,
	systemPromptOverride: () =>
		[
			"You evolve a general-purpose coding-agent harness using one failed entry task as mutation evidence.",
			"Propose one project-reusable behavioral change: a strategy section, one human-readable tool, or both.",
			"A tool must be a genuine coding aid, not a task answer. Its Python handler reads one JSON object from stdin and writes exactly one JSON object with content and optional details.",
			"The handler runs inside a network-disabled, read-only container except for /testbed. It must not use network, subprocesses, shells, package installation, Git history, lifecycle hooks, or host paths.",
			"Python os is allowed for non-process filesystem inspection such as os.walk, os.listdir, os.stat, and os.path. Process, shell, signal, dynamic attribute, and sys.modules access are rejected.",
			"Do not mention benchmark names, task IDs, gold patches, evaluator internals, hidden tests, or specific issue solutions in generated artifact content.",
			"Return exactly one JSON object with exactly these fields:",
			'{"mutation_summary":"short description","strategy_patch":"reusable strategy section or empty string","tool":null,"depends_on":[],"probe_task_ids":[]}',
			"If tool is non-null it must have exactly: name, label, description, parameters, handler_code, timeout_seconds.",
			"parameters must be a strict JSON object schema with exactly type, properties, required, additionalProperties; only string, number, integer, and boolean leaf types are allowed.",
			"depends_on may name earlier mutation IDs from the supplied parent lineage only.",
			"probe_task_ids selects up to four supplied same-repository candidate tasks for the adaptive gate, in priority order, and must include entry_task.instance_id. IDs are selector output only and must not appear in strategy or tool content.",
		].join("\n"),
});
await resourceLoader.reload();

const { session } = await createAgentSession({
	cwd: dirname(evidencePath),
	agentDir,
	model,
	thinkingLevel: "off",
	modelRuntime,
	tools: [],
	resourceLoader,
	sessionManager: SessionManager.inMemory(dirname(evidencePath)),
	settingsManager,
});

let inputTokens = 0;
let outputTokens = 0;
let cacheReadTokens = 0;
let cacheWriteTokens = 0;
let providerError;
let rawResponse = "";
let budgetAborted = false;
let timeoutAborted = false;
const startedAt = new Date();
const started = performance.now();

const unsubscribe = session.subscribe((event) => {
	writeFileSync(tracePath, `${JSON.stringify(event)}\n`, { flag: "a" });
	if (event.type !== "message_end" || event.message.role !== "assistant") return;
	inputTokens += event.message.usage.input;
	outputTokens += event.message.usage.output;
	cacheReadTokens += event.message.usage.cacheRead;
	cacheWriteTokens += event.message.usage.cacheWrite;
	rawResponse = messageText(event.message.content);
	providerError =
		event.message.stopReason === "error"
			? (event.message.errorMessage ?? "Unknown provider error.")
			: undefined;
	const totalTokens = inputTokens + outputTokens + cacheReadTokens + cacheWriteTokens;
	if ((totalTokens > maxTotalTokens || outputTokens > maxOutputTokens) && !budgetAborted) {
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
		"Use the following frozen parent evidence to produce the next harness strategy.\n\n" +
			evidenceText,
	);
} catch (caught) {
	error = caught instanceof Error ? caught.stack ?? caught.message : String(caught);
} finally {
	clearTimeout(timeout);
	unsubscribe();
	session.dispose();
}

let parsed;
let parseError;
try {
	parsed = parseStrictMutation(rawResponse);
} catch (caught) {
	parseError = caught instanceof Error ? caught.message : String(caught);
}
const valid = !error && !providerError && !budgetAborted && !timeoutAborted && !parseError;
const result = {
	schemaVersion: 1,
	parentArtifactHash: evidence.parent_artifact_hash,
	modelProvider: values["model-provider"],
	modelId: values["model-id"],
	startedAt: startedAt.toISOString(),
	completedAt: new Date().toISOString(),
	durationMs: Math.round(performance.now() - started),
	inputTokens,
	outputTokens,
	cacheReadTokens,
	cacheWriteTokens,
	maxOutputTokens,
	maxTotalTokens,
	budgetAborted,
	timeoutAborted,
	providerError,
	error,
	parseError,
	tokenTelemetryAvailable: true,
	rawResponse,
	rawResponseSha256: createHash("sha256").update(rawResponse).digest("hex"),
	valid,
	mutationSummary: valid ? parsed.mutation_summary : null,
	strategyPatch: valid ? parsed.strategy_patch : null,
	tool: valid ? parsed.tool : null,
	dependsOn: valid ? parsed.depends_on : null,
	probeTaskIds: valid ? parsed.probe_task_ids : null,
};
const temporaryOutputPath = `${outputPath}.tmp-${process.pid}`;
writeFileSync(temporaryOutputPath, `${JSON.stringify(result, null, 2)}\n`);
renameSync(temporaryOutputPath, outputPath);
if (!valid) process.exitCode = 1;

function messageText(content) {
	if (typeof content === "string") return content;
	if (!Array.isArray(content)) return "";
	return content
		.filter((block) => block && block.type === "text" && typeof block.text === "string")
		.map((block) => block.text)
		.join("\n");
}

function parseStrictMutation(text) {
	let candidate = text.trim();
	if (candidate.startsWith("```")) {
		const firstNewline = candidate.indexOf("\n");
		const lastFence = candidate.lastIndexOf("```");
		if (firstNewline < 0 || lastFence <= firstNewline) {
			throw new Error("Malformed fenced JSON response.");
		}
		candidate = candidate.slice(firstNewline + 1, lastFence).trim();
	}
	const value = JSON.parse(candidate);
	if (!value || typeof value !== "object" || Array.isArray(value)) {
		throw new Error("Mutation response must be a JSON object.");
	}
	const keys = Object.keys(value).sort();
	if (
		keys.join("\0") !==
		"depends_on\0mutation_summary\0probe_task_ids\0strategy_patch\0tool"
	) {
		throw new Error(
			"Mutation response fields must be exactly mutation_summary, strategy_patch, tool, depends_on, and probe_task_ids.",
		);
	}
	if (typeof value.mutation_summary !== "string" || !value.mutation_summary.trim()) {
		throw new Error("mutation_summary must be a non-empty string.");
	}
	if (typeof value.strategy_patch !== "string") {
		throw new Error("strategy_patch must be a string.");
	}
	if (
		!Array.isArray(value.depends_on) ||
		!value.depends_on.every((item) => typeof item === "string") ||
		new Set(value.depends_on).size !== value.depends_on.length
	) {
		throw new Error("depends_on must be an array of unique strings.");
	}
	if (
		!Array.isArray(value.probe_task_ids) ||
		value.probe_task_ids.length > 4 ||
		!value.probe_task_ids.every((item) => typeof item === "string") ||
		new Set(value.probe_task_ids).size !== value.probe_task_ids.length
	) {
		throw new Error("probe_task_ids must contain at most four unique strings.");
	}
	if (value.tool !== null) {
		if (!value.tool || typeof value.tool !== "object" || Array.isArray(value.tool)) {
			throw new Error("tool must be null or an object.");
		}
		const toolKeys = Object.keys(value.tool).sort();
		if (
			toolKeys.join("\0") !==
			"description\0handler_code\0label\0name\0parameters\0timeout_seconds"
		) {
			throw new Error("tool has invalid fields.");
		}
	}
	if (!value.strategy_patch.trim() && value.tool === null) {
		throw new Error("Mutation must change strategy or define one tool.");
	}
	return value;
}
