import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { promisify } from "node:util";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import rollbackExtension from "../extensions/index.ts";
import { buildRollbackPlan, ExternalReplayRunner } from "../src/replay.ts";
import type { Checkpoint, RollbackConfig } from "../src/types.ts";

const execFileAsync = promisify(execFile);

test("extension registers the rollback command", () => {
	let commandName: string | undefined;
	const api = {
		registerCommand(name: string) {
			commandName = name;
		},
	} as unknown as ExtensionAPI;

	rollbackExtension(api);
	assert.equal(commandName, "rollback");
});

test("external replay runner writes requests and aggregates majority telemetry", async () => {
	const cwd = await mkdtemp(path.join(os.tmpdir(), "pi-replay-"));
	try {
		let invocation = 0;
		const config: RollbackConfig = {
			artifactPaths: [".pi/evolving"],
			probeCommand: ["probe"],
			probeRepeats: 3,
			timeoutMs: 1_000,
			maxSliceFraction: 0.3,
			minSliceRecall: 0.95,
			singletonBudget: 1,
			dryRun: true,
		};
		const runner = new ExternalReplayRunner({
			config,
			cwd,
			runDirectory: path.join(cwd, "run"),
			failure: { id: "failure", summary: "failure" },
			checkpoints: [checkpoint("base"), checkpoint("p1", "base")],
			snapshotDirectory: path.join(cwd, "snapshots"),
			execute: async (_command, args) => {
				invocation += 1;
				const request = JSON.parse(await readFile(args.at(-1) ?? "", "utf8"));
				assert.deepEqual(request.activePatchIds, ["p1"]);
				return {
					stdout: `${JSON.stringify({
						failed: invocation !== 2,
						cost: 0.5,
						inputTokens: 10,
						outputTokens: 2,
						retries: 1,
					})}\n`,
					stderr: "",
					code: 0,
					killed: false,
				};
			},
		});

		const result = await runner.probe(["p1"]);
		assert.equal(result.failed, true);
		assert.equal(result.votes, 2);
		assert.equal(result.repeats, 3);
		assert.equal(result.cost, 1.5);
		assert.equal(result.inputTokens, 30);
		assert.equal(result.outputTokens, 6);
		assert.equal(result.retries, 3);
	} finally {
		await rm(cwd, { recursive: true, force: true });
	}
});

test("the packaged demo probe executes against checkpoint labels", async () => {
	const cwd = await mkdtemp(path.join(os.tmpdir(), "pi-demo-probe-"));
	try {
		const runner = new ExternalReplayRunner({
			config: {
				artifactPaths: [".pi/evolving"],
				probeCommand: ["node", path.resolve("fixtures/demo-probe.mjs")],
				probeRepeats: 1,
				timeoutMs: 1_000,
				maxSliceFraction: 0.3,
				minSliceRecall: 0.95,
				singletonBudget: 1,
				dryRun: true,
			},
			cwd,
			runDirectory: path.join(cwd, "run"),
			failure: { id: "demo", summary: "interaction" },
			checkpoints: [
				checkpoint("base"),
				{ ...checkpoint("p1", "base"), label: "cache-layer" },
				{ ...checkpoint("p2", "p1"), label: "parallel-workers" },
			],
			snapshotDirectory: path.join(cwd, "snapshots"),
			execute: async (command, args, options) => {
				const result = await execFileAsync(command, args, options);
				return { stdout: result.stdout, stderr: result.stderr, code: 0, killed: false };
			},
		});

		assert.equal((await runner.probe(["p1"])).failed, false);
		assert.equal((await runner.probe(["p1", "p2"])).failed, true);
	} finally {
		await rm(cwd, { recursive: true, force: true });
	}
});

test("rollback plan skips later patches that overlap removed files", () => {
	const checkpoints = [
		checkpoint("base"),
		{ ...checkpoint("p1", "base"), changedFiles: ["shared.ts"] },
		{ ...checkpoint("p2", "p1"), changedFiles: ["independent.ts"] },
		{ ...checkpoint("p3", "p2"), changedFiles: ["shared.ts"] },
	];
	const plan = buildRollbackPlan(checkpoints, ["p1"], ["p1"]);

	assert.deepEqual(plan.replayPatchIds, ["p2"]);
	assert.deepEqual(plan.skippedPatches, [
		{ id: "p1", reason: "causal" },
		{ id: "p3", reason: "overlapping-files" },
	]);
});

function checkpoint(id: string, parentId?: string): Checkpoint {
	return {
		id,
		label: id,
		parentId,
		snapshotId: `snapshot-${id}`,
		createdAt: "2026-09-24T00:00:00.000Z",
		changedFiles: [],
		dependsOn: [],
	};
}
