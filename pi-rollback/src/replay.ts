import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import type {
	Checkpoint,
	CheckpointId,
	FailureBundle,
	PriorCommandResult,
	ProbeCommandResult,
	ProbeObservation,
	ProbeRequest,
	ProbeSummary,
	RollbackConfig,
	RollbackPlan,
	SkippedPatch,
} from "./types.ts";

export interface CommandResult {
	stdout: string;
	stderr: string;
	code: number;
	killed: boolean;
}

export type CommandExecutor = (
	command: string,
	args: string[],
	options: { cwd: string; timeout: number },
) => Promise<CommandResult>;

export class ExternalReplayRunner {
	private config: RollbackConfig;
	private cwd: string;
	private runDirectory: string;
	private failure: FailureBundle;
	private checkpoints: Checkpoint[];
	private snapshotDirectory: string;
	private execute: CommandExecutor;
	private requestSequence = 0;

	constructor(options: {
		config: RollbackConfig;
		cwd: string;
		runDirectory: string;
		failure: FailureBundle;
		checkpoints: Checkpoint[];
		snapshotDirectory: string;
		execute: CommandExecutor;
	}) {
		this.config = options.config;
		this.cwd = options.cwd;
		this.runDirectory = options.runDirectory;
		this.failure = options.failure;
		this.checkpoints = options.checkpoints;
		this.snapshotDirectory = options.snapshotDirectory;
		this.execute = options.execute;
	}

	async probe(activePatchIds: CheckpointId[]): Promise<ProbeSummary> {
		const observations: ProbeObservation[] = [];
		for (let repeat = 0; repeat < this.config.probeRepeats; repeat++) {
			observations.push(await this.runProbe(activePatchIds, repeat));
		}
		const votes = observations.filter((observation) => observation.failed).length;
		return {
			activePatchIds: [...activePatchIds],
			failed: votes > observations.length / 2,
			votes,
			repeats: observations.length,
			durationMs: observations.reduce((sum, observation) => sum + observation.durationMs, 0),
			cost: observations.reduce((sum, observation) => sum + (observation.cost ?? 0), 0),
			inputTokens: observations.reduce((sum, observation) => sum + (observation.inputTokens ?? 0), 0),
			outputTokens: observations.reduce((sum, observation) => sum + (observation.outputTokens ?? 0), 0),
			retries: observations.reduce((sum, observation) => sum + (observation.retries ?? 0), 0),
			observations,
		};
	}

	async prior(): Promise<PriorCommandResult | undefined> {
		if (!this.config.priorCommand) return undefined;
		const requestPath = await this.writeRequest("prior", {
			schemaVersion: 1,
			failure: this.failure,
			workspace: this.cwd,
			checkpoints: this.checkpoints.map((checkpoint) => this.toProbeCheckpoint(checkpoint)),
		});
		const result = await this.runCommand(this.config.priorCommand, requestPath);
		if (result.code !== 0 || result.killed) {
			throw new Error(formatCommandFailure("Prior command", result));
		}
		const parsed = parseJsonObject(result.stdout, "prior command");
		if (!Array.isArray(parsed.order) || !parsed.order.every((item) => typeof item === "string")) {
			throw new Error("Prior command must return a JSON object with a string[] order field.");
		}
		return {
			order: parsed.order,
			model: optionalString(parsed.model),
			inputTokens: optionalNumber(parsed.inputTokens),
			outputTokens: optionalNumber(parsed.outputTokens),
			cost: optionalNumber(parsed.cost),
			retries: optionalNumber(parsed.retries),
			rawResponse: optionalString(parsed.rawResponse) ?? result.stdout,
		};
	}

	private async runProbe(activePatchIds: CheckpointId[], repeat: number): Promise<ProbeObservation> {
		const request: ProbeRequest = {
			schemaVersion: 1,
			failure: this.failure,
			workspace: this.cwd,
			activePatchIds,
			checkpoints: this.checkpoints.map((checkpoint) => this.toProbeCheckpoint(checkpoint)),
		};
		const requestPath = await this.writeRequest(`probe-${repeat}`, request);
		const started = performance.now();
		const result = await this.runCommand(this.config.probeCommand, requestPath);
		const durationMs = Math.round(performance.now() - started);
		if (result.code !== 0 || result.killed) {
			throw new Error(formatCommandFailure("Probe command", result));
		}
		const parsed = parseProbeResult(result.stdout);
		return {
			...parsed,
			activePatchIds: [...activePatchIds],
			durationMs,
			exitCode: result.code,
			stdout: result.stdout,
			stderr: result.stderr,
			requestPath,
		};
	}

	private async runCommand(command: string[], requestPath: string): Promise<CommandResult> {
		const executable = command[0];
		if (!executable) throw new Error("External command cannot be empty.");
		return this.execute(executable, [...command.slice(1), requestPath], {
			cwd: this.cwd,
			timeout: this.config.timeoutMs,
		});
	}

	private async writeRequest(kind: string, request: unknown): Promise<string> {
		const requestsDirectory = path.join(this.runDirectory, "requests");
		await mkdir(requestsDirectory, { recursive: true });
		this.requestSequence += 1;
		const requestPath = path.join(requestsDirectory, `${String(this.requestSequence).padStart(4, "0")}-${kind}.json`);
		await writeFile(requestPath, `${JSON.stringify(request, null, 2)}\n`, "utf8");
		return requestPath;
	}

	private toProbeCheckpoint(checkpoint: Checkpoint) {
		return {
			id: checkpoint.id,
			label: checkpoint.label,
			parentId: checkpoint.parentId,
			snapshotDir: path.join(this.snapshotDirectory, checkpoint.snapshotId, "files"),
			changedFiles: checkpoint.changedFiles,
			dependsOn: checkpoint.dependsOn,
		};
	}
}

export function buildRollbackPlan(
	checkpoints: readonly Checkpoint[],
	causalPatchIds: readonly CheckpointId[],
	removedPatchIds: readonly CheckpointId[],
): RollbackPlan {
	const removed = new Set(removedPatchIds);
	const causal = new Set(causalPatchIds);
	const earliestRemovedIndex = checkpoints.findIndex((checkpoint) => removed.has(checkpoint.id));
	if (earliestRemovedIndex <= 0) {
		throw new Error("A rollback plan requires a removable patch after the baseline.");
	}

	const rollbackCheckpoint = checkpoints[earliestRemovedIndex - 1];
	if (!rollbackCheckpoint) throw new Error("Rollback checkpoint is missing.");
	const blockedIds = new Set<CheckpointId>(removed);
	const blockedFiles = new Set<string>();
	for (const checkpoint of checkpoints) {
		if (removed.has(checkpoint.id)) {
			for (const file of checkpoint.changedFiles) blockedFiles.add(file);
		}
	}

	const replayPatchIds: CheckpointId[] = [];
	const skippedPatches: SkippedPatch[] = [];
	for (const checkpoint of checkpoints.slice(earliestRemovedIndex)) {
		if (removed.has(checkpoint.id)) {
			skippedPatches.push({ id: checkpoint.id, reason: "causal" });
			continue;
		}
		if (checkpoint.dependsOn.some((id) => blockedIds.has(id))) {
			skippedPatches.push({ id: checkpoint.id, reason: "dependency" });
			blockedIds.add(checkpoint.id);
			for (const file of checkpoint.changedFiles) blockedFiles.add(file);
			continue;
		}
		if (checkpoint.changedFiles.some((file) => blockedFiles.has(file))) {
			skippedPatches.push({ id: checkpoint.id, reason: "overlapping-files" });
			blockedIds.add(checkpoint.id);
			for (const file of checkpoint.changedFiles) blockedFiles.add(file);
			continue;
		}
		replayPatchIds.push(checkpoint.id);
	}

	return {
		rollbackCheckpointId: rollbackCheckpoint.id,
		rollbackSessionEntryId: rollbackCheckpoint.sessionEntryId,
		causalPatchIds: checkpoints.filter((checkpoint) => causal.has(checkpoint.id)).map((checkpoint) => checkpoint.id),
		removedPatchIds: checkpoints.filter((checkpoint) => removed.has(checkpoint.id)).map((checkpoint) => checkpoint.id),
		replayPatchIds,
		skippedPatches,
	};
}

function parseProbeResult(stdout: string): ProbeCommandResult {
	const parsed = parseJsonObject(stdout, "probe command");
	if (typeof parsed.failed !== "boolean") {
		throw new Error("Probe command must return a JSON object with a boolean failed field.");
	}
	return {
		failed: parsed.failed,
		cost: optionalNumber(parsed.cost),
		inputTokens: optionalNumber(parsed.inputTokens),
		outputTokens: optionalNumber(parsed.outputTokens),
		model: optionalString(parsed.model),
		retries: optionalNumber(parsed.retries),
	};
}

function parseJsonObject(stdout: string, source: string): Record<string, unknown> {
	let parsed: unknown;
	try {
		parsed = JSON.parse(stdout);
	} catch (error) {
		throw new Error(`${source} returned invalid JSON: ${error instanceof Error ? error.message : String(error)}`);
	}
	if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
		throw new Error(`${source} must return a JSON object.`);
	}
	return parsed as Record<string, unknown>;
}

function optionalString(value: unknown): string | undefined {
	return typeof value === "string" ? value : undefined;
}

function optionalNumber(value: unknown): number | undefined {
	return typeof value === "number" && Number.isFinite(value) ? value : undefined;
}

function formatCommandFailure(label: string, result: CommandResult): string {
	const reason = result.killed ? "timed out or was aborted" : `exited with code ${result.code}`;
	const stderr = result.stderr.trim();
	return `${label} ${reason}${stderr ? `: ${stderr}` : ""}`;
}
