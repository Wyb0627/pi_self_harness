import {
	createAgentSession,
	DefaultResourceLoader,
	ModelRuntime,
	SessionManager,
	SettingsManager,
} from "../pi-rollback/node_modules/@earendil-works/pi-coding-agent/dist/index.js";

const agentDir = new URL(
	"../research_output/clm_budgeted_evolution_20260924_125503/pi_home/agent/",
	import.meta.url,
).pathname;
const apiKey = process.env.ROLLBACK_ENDPOINT_API_KEY;
if (!apiKey) throw new Error("ROLLBACK_ENDPOINT_API_KEY is required.");

const modelRuntime = await ModelRuntime.create({
	authPath: `${agentDir}/auth.json`,
	modelsPath: `${agentDir}/models.json`,
	modelsStorePath: `${agentDir}/models-store.json`,
});
await modelRuntime.setRuntimeApiKey("rollback-deepseek", apiKey);
const configuredModel = modelRuntime.getModel("rollback-deepseek", "byteplus/deepseek-v4-flash-ga");
if (!configuredModel) throw new Error("DeepSeek endpoint model is unavailable.");
const model = { ...configuredModel, maxTokens: 128 };

const settingsManager = SettingsManager.inMemory({
	compaction: { enabled: false },
	retry: { enabled: false },
});
const resourceLoader = new DefaultResourceLoader({
	cwd: "/tmp",
	agentDir,
	settingsManager,
	systemPromptOverride: () => "You are concise.",
});
await resourceLoader.reload();

const { session } = await createAgentSession({
	cwd: "/tmp",
	agentDir,
	model,
	thinkingLevel: "off",
	modelRuntime,
	tools: [],
	resourceLoader,
	sessionManager: SessionManager.inMemory(),
	settingsManager,
});

session.subscribe((event) => {
	process.stdout.write(`${JSON.stringify(event)}\n`);
});
await session.prompt("Reply exactly OK.");
session.dispose();
