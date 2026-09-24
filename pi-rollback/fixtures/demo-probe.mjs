import { readFile } from "node:fs/promises";

const requestPath = process.argv.at(-1);
if (!requestPath) throw new Error("Expected a request JSON path.");

const request = JSON.parse(await readFile(requestPath, "utf8"));
const labels = new Set(
	request.checkpoints
		.filter((checkpoint) => request.activePatchIds.includes(checkpoint.id))
		.map((checkpoint) => checkpoint.label),
);

const failed = labels.has("cache-layer") && labels.has("parallel-workers");
process.stdout.write(
	`${JSON.stringify({
		failed,
		cost: 0,
		inputTokens: 0,
		outputTokens: 0,
		model: "deterministic-demo",
		retries: 0,
	})}\n`,
);
