import assert from "node:assert/strict";
import test from "node:test";
import { ddmin, diagnoseLineage } from "../src/diagnosis.ts";
import type { Checkpoint, DiagnosisOptions, FailureBundle, ProbeSummary, RollbackConfig } from "../src/types.ts";

const CONFIG: RollbackConfig = {
	artifactPaths: [".pi/evolving"],
	probeCommand: ["false"],
	probeRepeats: 1,
	timeoutMs: 1_000,
	maxSliceFraction: 0.5,
	minSliceRecall: 0.95,
	singletonBudget: 1,
	dryRun: true,
};

test("ddmin recovers an interacting failure core", async () => {
	const cause = new Set(["p1", "p3"]);
	const result = await ddmin(["p1", "p2", "p3", "p4"], async (active) => {
		return [...cause].every((id) => active.includes(id));
	});
	assert.deepEqual(result, ["p1", "p3"]);
});

test("diagnosis commits a verified minimal removal and replays independent gains", async () => {
	const failure: FailureBundle = {
		id: "interaction",
		summary: "p1 and p3 fail together",
		candidatePatches: ["p1", "p3"],
		priorOrder: ["p1", "p3"],
		sliceAuditRecall: 1,
	};
	const result = await diagnose(failure, (active) => active.includes("p1") && active.includes("p3"));

	assert.equal(result.method, "singleton-removal");
	assert.deepEqual(result.causalPatchIds, ["p1"]);
	assert.deepEqual(result.removedPatchIds, ["p1"]);
	assert.equal(result.plan?.rollbackCheckpointId, "base");
	assert.deepEqual(result.plan?.replayPatchIds, ["p2", "p3"]);
	assert.deepEqual(result.plan?.skippedPatches, [
		{ id: "p1", reason: "causal" },
		{ id: "p4", reason: "dependency" },
	]);
	assert.equal(result.telemetry.uniqueProbes, 5);
});

test("an incomplete candidate slice falls back to full ddmin", async () => {
	const failure: FailureBundle = {
		id: "slice-miss",
		summary: "candidate slice misses p3",
		candidatePatches: ["p1"],
		sliceAuditRecall: 1,
	};
	const result = await diagnose(failure, (active) => active.includes("p1") || active.includes("p3"));

	assert.equal(result.method, "full-repair-ddmin");
	assert.equal(result.telemetry.usedFallback, true);
	assert.deepEqual(result.causalPatchIds, ["p1", "p3"]);
	assert.deepEqual(result.removedPatchIds, ["p1", "p3"]);
});

test("a low-recall slice is not used", async () => {
	const failure: FailureBundle = {
		id: "unsafe-slice",
		summary: "slice audit is below the configured gate",
		candidatePatches: ["p2"],
		sliceAuditRecall: 0.8,
	};
	const result = await diagnose(failure, (active) => active.includes("p2"));

	assert.equal(result.method, "full-repair-ddmin");
	assert.equal(result.telemetry.usedFallback, false);
	assert.deepEqual(result.causalPatchIds, ["p2"]);
});

test("a misleading prior cannot bypass executable repair verification", async () => {
	const failure: FailureBundle = {
		id: "misleading-prior",
		summary: "p1 and p3 fail together",
		priorOrder: ["p2", "p4", "p1", "p3"],
	};
	const fails = (active: readonly string[]) => active.includes("p1") && active.includes("p3");
	const result = await diagnose(failure, fails);

	assert.equal(result.method, "full-repair-ddmin");
	assert.equal(result.removedPatchIds.length, 1);
	assert.equal(fails(["p1", "p2", "p3", "p4"].filter((id) => !result.removedPatchIds.includes(id))), false);
});

test("diagnosis abstains when dependency-safe replay invalidates the repair", async () => {
	const failure: FailureBundle = {
		id: "plan-regression",
		summary: "skipping a dependent guard reintroduces failure",
		priorOrder: ["p1"],
	};
	const result = await diagnose(
		failure,
		(active) => (active.includes("p1") && active.includes("p3")) || (active.includes("p2") && !active.includes("p4")),
	);

	assert.equal(result.method, "abstain");
	assert.match(result.telemetry.abstainReason ?? "", /dependency-safe replay plan/);
	assert.equal(result.plan, undefined);
});

test("diagnosis abstains when the baseline already fails", async () => {
	const failure: FailureBundle = {
		id: "bad-baseline",
		summary: "not introduced by the tracked lineage",
	};
	const result = await diagnose(failure, () => true);

	assert.equal(result.method, "abstain");
	assert.match(result.telemetry.abstainReason ?? "", /baseline/);
	assert.equal(result.plan, undefined);
});

async function diagnose(failure: FailureBundle, fails: (active: readonly string[]) => boolean) {
	const options: DiagnosisOptions = {
		diagnosisId: `test-${failure.id}`,
		config: CONFIG,
		failure,
		checkpoints: checkpoints(),
		priorOrder: failure.priorOrder ?? [],
		probe: async (active) => probeSummary(active, fails(active)),
		configHash: "config",
		failureHash: "failure",
		gitHash: "git",
	};
	return diagnoseLineage(options);
}

function checkpoints(): Checkpoint[] {
	return [
		checkpoint("base", undefined, [], []),
		checkpoint("p1", "base", ["a.ts"], []),
		checkpoint("p2", "p1", ["b.ts"], []),
		checkpoint("p3", "p2", ["c.ts"], []),
		checkpoint("p4", "p3", ["d.ts"], ["p1"]),
	];
}

function checkpoint(id: string, parentId: string | undefined, changedFiles: string[], dependsOn: string[]): Checkpoint {
	return {
		id,
		label: id,
		parentId,
		sessionEntryId: `entry-${id}`,
		snapshotId: `snapshot-${id}`,
		createdAt: "2026-09-24T00:00:00.000Z",
		changedFiles,
		dependsOn,
	};
}

function probeSummary(activePatchIds: string[], failed: boolean): ProbeSummary {
	return {
		activePatchIds,
		failed,
		votes: Number(failed),
		repeats: 1,
		durationMs: 1,
		cost: 0,
		inputTokens: 0,
		outputTokens: 0,
		retries: 0,
		observations: [],
	};
}
