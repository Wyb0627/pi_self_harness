export type CheckpointId = string;

export interface ArtifactRoot {
	path: string;
	kind: "file" | "directory" | "missing";
}

export interface ArtifactFile {
	path: string;
	sha256: string;
	size: number;
	mode: number;
}

export interface SnapshotManifest {
	id: string;
	createdAt: string;
	artifactPaths: string[];
	roots: ArtifactRoot[];
	files: ArtifactFile[];
}

export interface Checkpoint {
	id: CheckpointId;
	label: string;
	parentId?: CheckpointId;
	sessionEntryId?: string;
	snapshotId: string;
	createdAt: string;
	changedFiles: string[];
	dependsOn: CheckpointId[];
	replayedFrom?: CheckpointId[];
}

export interface FailureMetadata {
	model?: string;
	promptHash?: string;
	dataHash?: string;
	gitHash?: string;
	[key: string]: string | number | boolean | undefined;
}

export interface FailureBundle {
	id: string;
	summary: string;
	candidatePatches?: string[];
	priorOrder?: string[];
	sliceAuditRecall?: number;
	metadata?: FailureMetadata;
}

export interface RollbackConfig {
	artifactPaths: string[];
	probeCommand: string[];
	priorCommand?: string[];
	probeRepeats: number;
	timeoutMs: number;
	maxSliceFraction: number;
	minSliceRecall: number;
	singletonBudget: number;
	dryRun: boolean;
}

export interface ProbeCheckpoint {
	id: CheckpointId;
	label: string;
	parentId?: CheckpointId;
	snapshotDir: string;
	changedFiles: string[];
	dependsOn: CheckpointId[];
}

export interface ProbeRequest {
	schemaVersion: 1;
	failure: FailureBundle;
	workspace: string;
	activePatchIds: CheckpointId[];
	checkpoints: ProbeCheckpoint[];
}

export interface ProbeCommandResult {
	failed: boolean;
	cost?: number;
	inputTokens?: number;
	outputTokens?: number;
	model?: string;
	retries?: number;
}

export interface ProbeObservation extends ProbeCommandResult {
	activePatchIds: CheckpointId[];
	durationMs: number;
	exitCode: number;
	stdout: string;
	stderr: string;
	requestPath: string;
}

export interface ProbeSummary {
	activePatchIds: CheckpointId[];
	failed: boolean;
	votes: number;
	repeats: number;
	durationMs: number;
	cost: number;
	inputTokens: number;
	outputTokens: number;
	retries: number;
	observations: ProbeObservation[];
}

export interface PriorCommandResult {
	order: string[];
	model?: string;
	inputTokens?: number;
	outputTokens?: number;
	cost?: number;
	retries?: number;
	rawResponse?: string;
}

export interface DiagnosisTelemetry {
	startedAt: string;
	completedAt: string;
	durationMs: number;
	probeInvocations: number;
	uniqueProbes: number;
	probeCost: number;
	inputTokens: number;
	outputTokens: number;
	retries: number;
	model?: string;
	promptHash?: string;
	dataHash?: string;
	gitHash?: string;
	configHash: string;
	failureHash: string;
	usedFallback: boolean;
	abstainReason?: string;
}

export interface SkippedPatch {
	id: CheckpointId;
	reason: "causal" | "dependency" | "overlapping-files";
}

export interface RollbackPlan {
	rollbackCheckpointId: CheckpointId;
	rollbackSessionEntryId?: string;
	causalPatchIds: CheckpointId[];
	removedPatchIds: CheckpointId[];
	replayPatchIds: CheckpointId[];
	skippedPatches: SkippedPatch[];
}

export interface DiagnosisRecord {
	id: string;
	failure: FailureBundle;
	method: "singleton-removal" | "sliced-repair-ddmin" | "full-repair-ddmin" | "abstain";
	candidatePatchIds: CheckpointId[];
	priorOrder: CheckpointId[];
	causalPatchIds: CheckpointId[];
	removedPatchIds: CheckpointId[];
	plan?: RollbackPlan;
	prior?: PriorCommandResult;
	probes: ProbeSummary[];
	telemetry: DiagnosisTelemetry;
}

export interface ApplyRecord {
	id: string;
	diagnosisId: string;
	appliedAt: string;
	dryRun: boolean;
}

export type RollbackEntry =
	| { kind: "checkpoint"; checkpoint: Checkpoint }
	| { kind: "diagnosis"; diagnosis: DiagnosisRecord }
	| { kind: "apply"; apply: ApplyRecord };

export interface DiagnosisOptions {
	diagnosisId?: string;
	config: RollbackConfig;
	failure: FailureBundle;
	checkpoints: Checkpoint[];
	priorOrder: CheckpointId[];
	priorTelemetry?: PriorCommandResult;
	probe: (activePatchIds: CheckpointId[]) => Promise<ProbeSummary>;
	configHash: string;
	failureHash: string;
	gitHash?: string;
}
