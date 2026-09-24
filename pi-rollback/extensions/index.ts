import { randomUUID } from "node:crypto";
import path from "node:path";
import type { ExtensionAPI, ExtensionCommandContext, ExtensionContext } from "@earendil-works/pi-coding-agent";
import { diagnoseLineage, resolveCheckpointRefs } from "../src/diagnosis.ts";
import { ExternalReplayRunner } from "../src/replay.ts";
import { hashValue, ProjectStore } from "../src/state.ts";
import type {
	ApplyRecord,
	Checkpoint,
	DiagnosisRecord,
	PriorCommandResult,
	RollbackEntry,
	RollbackPlan,
} from "../src/types.ts";

const ENTRY_TYPE = "pi-causal-rollback";

export default function rollbackExtension(pi: ExtensionAPI) {
	pi.registerCommand("rollback", {
		description: "Checkpoint, diagnose, inspect, or apply a causal rollback",
		handler: async (args, ctx) => {
			try {
				const tokens = tokenize(args);
				const action = tokens.shift();
				switch (action) {
					case "checkpoint":
						await checkpoint(pi, ctx, tokens);
						return;
					case "diagnose":
						await diagnose(pi, ctx, tokens);
						return;
					case "apply":
						await apply(pi, ctx, tokens);
						return;
					case "status":
						status(ctx);
						return;
					default:
						ctx.ui.notify(
							"Usage: /rollback checkpoint [label] [--depends id,id] | diagnose <failure.json> | apply [diagnosis-id] [--execute] | status",
							"info",
						);
				}
			} catch (error) {
				ctx.ui.notify(error instanceof Error ? error.message : String(error), "error");
			}
		},
	});
}

async function checkpoint(pi: ExtensionAPI, ctx: ExtensionCommandContext, tokens: string[]): Promise<void> {
	const parsed = parseFlags(tokens);
	const label = parsed.positionals.join(" ").trim() || `checkpoint-${Date.now()}`;
	const checkpoints = branchCheckpoints(ctx);
	if (checkpoints.some((item) => item.label === label)) {
		throw new Error(`Checkpoint label already exists on this branch: ${label}`);
	}

	const store = new ProjectStore(ctx.cwd);
	const config = await store.loadConfig();
	const parent = checkpoints.at(-1);
	const dependencyRefs = parsed.flags.get("depends")?.split(",").filter(Boolean) ?? [];
	const dependsOn = resolveCheckpointRefs(dependencyRefs, checkpoints);
	const snapshot = await store.createSnapshot(config.artifactPaths);
	const changedFiles = await store.changedFiles(parent?.snapshotId, snapshot);
	if (parent && changedFiles.length === 0) {
		throw new Error("No managed artifact changed since the previous checkpoint.");
	}

	const checkpointValue: Checkpoint = {
		id: `cp-${Date.now()}-${snapshot.id.slice(0, 8)}`,
		label,
		parentId: parent?.id,
		sessionEntryId: ctx.sessionManager.getLeafId() ?? undefined,
		snapshotId: snapshot.id,
		createdAt: new Date().toISOString(),
		changedFiles,
		dependsOn,
	};
	pi.appendEntry<RollbackEntry>(ENTRY_TYPE, { kind: "checkpoint", checkpoint: checkpointValue });
	await store.writeRun(checkpointValue.id, checkpointValue);
	ctx.ui.notify(
		`Checkpoint ${label} (${checkpointValue.id}); ${changedFiles.length} changed artifact path(s).`,
		"info",
	);
}

async function diagnose(pi: ExtensionAPI, ctx: ExtensionCommandContext, tokens: string[]): Promise<void> {
	const parsed = parseFlags(tokens);
	const failurePath = parsed.positionals[0];
	if (!failurePath) throw new Error("Usage: /rollback diagnose <failure-bundle.json>");

	const checkpoints = branchCheckpoints(ctx);
	const store = new ProjectStore(ctx.cwd);
	const config = await store.loadConfig();
	const failure = await store.loadFailureBundle(failurePath);
	const diagnosisId = `diag-${Date.now()}-${randomUUID().slice(0, 8)}`;
	const runDirectory = path.join(store.runDirectory, diagnosisId);
	const runner = new ExternalReplayRunner({
		config,
		cwd: ctx.cwd,
		runDirectory,
		failure,
		checkpoints,
		snapshotDirectory: store.snapshotDirectory,
		execute: (command, args, options) => pi.exec(command, args, options),
	});

	let priorTelemetry: PriorCommandResult | undefined;
	try {
		priorTelemetry = await runner.prior();
	} catch (error) {
		ctx.ui.notify(
			`Prior command failed; continuing with manifest order: ${error instanceof Error ? error.message : String(error)}`,
			"warning",
		);
	}
	const priorRefs = priorTelemetry?.order ?? failure.priorOrder ?? [];
	const priorOrder = resolveCheckpointRefs(priorRefs, checkpoints.slice(1));
	const gitHashResult = await pi.exec("git", ["rev-parse", "HEAD"], {
		cwd: ctx.cwd,
		timeout: 10_000,
	});
	const gitHash = gitHashResult.code === 0 ? gitHashResult.stdout.trim() : undefined;
	const result = await diagnoseLineage({
		diagnosisId,
		config,
		failure,
		checkpoints,
		priorOrder,
		priorTelemetry,
		probe: (activePatchIds) => runner.probe(activePatchIds),
		configHash: hashValue(config),
		failureHash: hashValue(failure),
		gitHash,
	});
	pi.appendEntry<RollbackEntry>(ENTRY_TYPE, { kind: "diagnosis", diagnosis: result });
	const outputPath = await store.writeRun(result.id, result);
	ctx.ui.notify(formatDiagnosis(result, outputPath), result.method === "abstain" ? "warning" : "info");
}

async function apply(pi: ExtensionAPI, ctx: ExtensionCommandContext, tokens: string[]): Promise<void> {
	const parsed = parseFlags(tokens);
	const diagnosisId = parsed.positionals[0];
	const diagnosis = findDiagnosis(ctx, diagnosisId);
	if (!diagnosis) {
		throw new Error(diagnosisId ? `Diagnosis not found: ${diagnosisId}` : "No diagnosis is available.");
	}
	if (!diagnosis.plan) throw new Error(`Diagnosis ${diagnosis.id} has no applicable rollback plan.`);

	const store = new ProjectStore(ctx.cwd);
	const config = await store.loadConfig();
	const execute = parsed.flags.has("execute");
	if (config.dryRun || !execute) {
		ctx.ui.notify(`${formatPlan(diagnosis.plan)}\nDry run only. Use --execute and set dryRun=false to apply.`, "info");
		return;
	}
	if (!ctx.hasUI) throw new Error("Applying a rollback requires an interactive confirmation.");
	const confirmed = await ctx.ui.confirm(
		"Apply causal rollback?",
		`${formatPlan(diagnosis.plan)}\nOnly configured artifact paths will be changed.`,
	);
	if (!confirmed) return;

	const checkpoints = branchCheckpoints(ctx);
	const byId = new Map(checkpoints.map((checkpoint) => [checkpoint.id, checkpoint]));
	const rollbackCheckpoint = requiredCheckpoint(byId, diagnosis.plan.rollbackCheckpointId);
	const safetySnapshot = await store.createSnapshot(config.artifactPaths);
	let navigated = false;
	try {
		await store.restoreSnapshot(rollbackCheckpoint.snapshotId);
		for (const replayId of diagnosis.plan.replayPatchIds) {
			const replayCheckpoint = requiredCheckpoint(byId, replayId);
			if (!replayCheckpoint.parentId) throw new Error(`Replay checkpoint has no parent: ${replayId}`);
			const parent = requiredCheckpoint(byId, replayCheckpoint.parentId);
			await store.applyCheckpointDelta(replayCheckpoint, parent);
		}
		const replayedSnapshot =
			diagnosis.plan.replayPatchIds.length > 0 ? await store.createSnapshot(config.artifactPaths) : undefined;
		const replayedChanges = replayedSnapshot
			? await store.changedFiles(rollbackCheckpoint.snapshotId, replayedSnapshot)
			: [];
		if (diagnosis.plan.rollbackSessionEntryId) {
			const navigation = await ctx.navigateTree(diagnosis.plan.rollbackSessionEntryId, {
				summarize: false,
				label: `rollback:${diagnosis.id}`,
			});
			if (navigation.cancelled) throw new Error("Session tree navigation was cancelled.");
			navigated = true;
		}
		if (replayedSnapshot) {
			const replayedCheckpoint: Checkpoint = {
				id: `cp-${Date.now()}-${replayedSnapshot.id.slice(0, 8)}`,
				label: `replay:${diagnosis.failure.id}`,
				parentId: rollbackCheckpoint.id,
				sessionEntryId: ctx.sessionManager.getLeafId() ?? undefined,
				snapshotId: replayedSnapshot.id,
				createdAt: new Date().toISOString(),
				changedFiles: replayedChanges,
				dependsOn: [],
				replayedFrom: diagnosis.plan.replayPatchIds,
			};
			pi.appendEntry<RollbackEntry>(ENTRY_TYPE, { kind: "checkpoint", checkpoint: replayedCheckpoint });
			await store.writeRun(replayedCheckpoint.id, replayedCheckpoint);
		}
		const applyRecord: ApplyRecord = {
			id: `apply-${Date.now()}-${randomUUID().slice(0, 8)}`,
			diagnosisId: diagnosis.id,
			appliedAt: new Date().toISOString(),
			dryRun: false,
		};
		pi.appendEntry<RollbackEntry>(ENTRY_TYPE, { kind: "apply", apply: applyRecord });
		await store.writeRun(applyRecord.id, applyRecord);
		await ctx.reload();
	} catch (error) {
		if (!navigated) await store.restoreSnapshot(safetySnapshot.id);
		throw error;
	}
}

function status(ctx: ExtensionContext): void {
	const checkpoints = branchCheckpoints(ctx);
	const diagnoses = branchDiagnoses(ctx);
	const latest = diagnoses.at(-1);
	const lines = [
		`Tracked checkpoints: ${checkpoints.length}`,
		...checkpoints.map(
			(checkpoint, index) => `${index === 0 ? "baseline" : `patch ${index}`}: ${checkpoint.label} (${checkpoint.id})`,
		),
		latest
			? `Latest diagnosis: ${latest.id}, method=${latest.method}, probes=${latest.telemetry.probeInvocations}`
			: "Latest diagnosis: none",
	];
	ctx.ui.notify(lines.join("\n"), "info");
}

function branchCheckpoints(ctx: ExtensionContext): Checkpoint[] {
	return collectEntries(ctx.sessionManager.getBranch())
		.filter((entry): entry is Extract<RollbackEntry, { kind: "checkpoint" }> => entry.kind === "checkpoint")
		.map((entry) => entry.checkpoint);
}

function branchDiagnoses(ctx: ExtensionContext): DiagnosisRecord[] {
	return collectEntries(ctx.sessionManager.getBranch())
		.filter((entry): entry is Extract<RollbackEntry, { kind: "diagnosis" }> => entry.kind === "diagnosis")
		.map((entry) => entry.diagnosis);
}

function collectEntries(entries: ReturnType<ExtensionContext["sessionManager"]["getEntries"]>): RollbackEntry[] {
	const collected: RollbackEntry[] = [];
	for (const entry of entries) {
		if (entry.type !== "custom" || entry.customType !== ENTRY_TYPE || !isRollbackEntry(entry.data)) continue;
		collected.push(entry.data);
	}
	return collected;
}

function isRollbackEntry(value: unknown): value is RollbackEntry {
	if (typeof value !== "object" || value === null || !("kind" in value)) return false;
	return value.kind === "checkpoint" || value.kind === "diagnosis" || value.kind === "apply";
}

function findDiagnosis(ctx: ExtensionContext, id: string | undefined): DiagnosisRecord | undefined {
	const diagnoses = branchDiagnoses(ctx);
	return id ? diagnoses.find((diagnosis) => diagnosis.id === id) : diagnoses.at(-1);
}

function requiredCheckpoint(byId: ReadonlyMap<string, Checkpoint>, id: string): Checkpoint {
	const checkpoint = byId.get(id);
	if (!checkpoint) throw new Error(`Checkpoint not found: ${id}`);
	return checkpoint;
}

function formatDiagnosis(diagnosis: DiagnosisRecord, outputPath: string): string {
	if (diagnosis.method === "abstain") {
		return `Diagnosis abstained: ${diagnosis.telemetry.abstainReason}\nAudit: ${outputPath}`;
	}
	return [
		`Diagnosis ${diagnosis.id}: ${diagnosis.method}`,
		`Causal patches: ${diagnosis.causalPatchIds.join(", ")}`,
		`Remove: ${diagnosis.removedPatchIds.join(", ")}`,
		`Probe invocations: ${diagnosis.telemetry.probeInvocations}`,
		`Audit: ${outputPath}`,
	].join("\n");
}

function formatPlan(plan: RollbackPlan): string {
	return [
		`Rollback to: ${plan.rollbackCheckpointId}`,
		`Remove: ${plan.removedPatchIds.join(", ")}`,
		`Replay: ${plan.replayPatchIds.join(", ") || "none"}`,
		`Skip: ${plan.skippedPatches.map((item) => `${item.id} (${item.reason})`).join(", ") || "none"}`,
	].join("\n");
}

function parseFlags(tokens: readonly string[]): {
	positionals: string[];
	flags: Map<string, string>;
} {
	const positionals: string[] = [];
	const flags = new Map<string, string>();
	for (let index = 0; index < tokens.length; index++) {
		const token = tokens[index];
		if (!token) continue;
		if (!token.startsWith("--")) {
			positionals.push(token);
			continue;
		}
		const equals = token.indexOf("=");
		if (equals !== -1) {
			flags.set(token.slice(2, equals), token.slice(equals + 1));
			continue;
		}
		const name = token.slice(2);
		const next = tokens[index + 1];
		if (next && !next.startsWith("--")) {
			flags.set(name, next);
			index += 1;
		} else {
			flags.set(name, "true");
		}
	}
	return { positionals, flags };
}

function tokenize(input: string): string[] {
	const tokens: string[] = [];
	let current = "";
	let quote: "'" | '"' | undefined;
	let escaped = false;
	for (const character of input.trim()) {
		if (escaped) {
			current += character;
			escaped = false;
			continue;
		}
		if (character === "\\") {
			escaped = true;
			continue;
		}
		if (quote) {
			if (character === quote) quote = undefined;
			else current += character;
			continue;
		}
		if (character === "'" || character === '"') {
			quote = character;
			continue;
		}
		if (/\s/.test(character)) {
			if (current) {
				tokens.push(current);
				current = "";
			}
			continue;
		}
		current += character;
	}
	if (quote) throw new Error("Unterminated quote in rollback command.");
	if (escaped) current += "\\";
	if (current) tokens.push(current);
	return tokens;
}
