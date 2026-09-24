import { randomUUID } from "node:crypto";
import { buildRollbackPlan } from "./replay.ts";
import type { CheckpointId, DiagnosisOptions, DiagnosisRecord, DiagnosisTelemetry, ProbeSummary } from "./types.ts";

export async function ddmin<T>(
	items: readonly T[],
	reproduces: (candidate: readonly T[]) => Promise<boolean>,
): Promise<T[]> {
	let current = [...items];
	if (current.length === 0 || !(await reproduces(current))) return [];

	let granularity = 2;
	while (current.length >= 2) {
		const chunks = partition(current, granularity);
		let reduced = false;

		for (const chunk of chunks) {
			if (await reproduces(chunk)) {
				current = chunk;
				granularity = Math.max(granularity - 1, 2);
				reduced = true;
				break;
			}
		}
		if (reduced) continue;

		for (const chunk of chunks) {
			const removed = new Set(chunk);
			const complement = current.filter((item) => !removed.has(item));
			if (complement.length > 0 && (await reproduces(complement))) {
				current = complement;
				granularity = Math.max(granularity - 1, 2);
				reduced = true;
				break;
			}
		}
		if (reduced) continue;

		if (granularity >= current.length) break;
		granularity = Math.min(current.length, granularity * 2);
	}

	let index = 0;
	while (index < current.length) {
		const candidate = current.slice(0, index).concat(current.slice(index + 1));
		if (candidate.length > 0 && (await reproduces(candidate))) {
			current = candidate;
		} else {
			index += 1;
		}
	}
	return current;
}

export async function diagnoseLineage(options: DiagnosisOptions): Promise<DiagnosisRecord> {
	const startedAt = new Date();
	const started = performance.now();
	const probes: ProbeSummary[] = [];
	const probeCache = new Map<string, ProbeSummary>();
	const patches = options.checkpoints.slice(1);
	const allPatchIds = patches.map((checkpoint) => checkpoint.id);
	const patchSet = new Set(allPatchIds);

	const probe = async (activePatchIds: readonly CheckpointId[]): Promise<ProbeSummary> => {
		const normalized = allPatchIds.filter((id) => activePatchIds.includes(id));
		const key = normalized.join("\0");
		const cached = probeCache.get(key);
		if (cached) return cached;
		const summary = await options.probe(normalized);
		probeCache.set(key, summary);
		probes.push(summary);
		return summary;
	};

	const abstain = (reason: string): DiagnosisRecord =>
		makeRecord({
			options,
			started,
			startedAt,
			probes,
			method: "abstain",
			candidates: [],
			priorOrder: [],
			causalPatchIds: [],
			removedPatchIds: [],
			usedFallback: false,
			abstainReason: reason,
		});

	if (options.checkpoints.length < 2) {
		return abstain("At least a baseline and one changed checkpoint are required.");
	}

	assertLinearLineage(options.checkpoints);
	const current = await probe(allPatchIds);
	if (!current.failed) {
		return abstain("The configured probe does not reproduce the failure at the current checkpoint.");
	}
	const baseline = await probe([]);
	if (baseline.failed) {
		return abstain("The failure reproduces at the baseline, before every tracked patch.");
	}

	const requestedCandidates = resolveCheckpointRefs(options.failure.candidatePatches ?? [], patches);
	const candidates = requestedCandidates.length > 0 ? requestedCandidates : allPatchIds;
	const priorOrder = unique([
		...options.priorOrder.filter((id) => patchSet.has(id) && candidates.includes(id)),
		...candidates,
	]);
	const sliceFraction = candidates.length / allPatchIds.length;
	const sliceAllowed =
		requestedCandidates.length > 0 &&
		sliceFraction <= options.config.maxSliceFraction &&
		(options.failure.sliceAuditRecall ?? 0) >= options.config.minSliceRecall;

	let usedFallback = false;
	let method: DiagnosisRecord["method"] = sliceAllowed ? "sliced-repair-ddmin" : "full-repair-ddmin";
	let searchSpace = sliceAllowed ? priorOrder : orderByPrior(allPatchIds, options.priorOrder);
	const repairs = async (removedPatchIds: readonly CheckpointId[]): Promise<boolean> => {
		return !(await probe(without(allPatchIds, removedPatchIds))).failed;
	};

	if (sliceAllowed && !(await repairs(searchSpace))) {
		searchSpace = orderByPrior(allPatchIds, options.priorOrder);
		method = "full-repair-ddmin";
		usedFallback = true;
	}

	let removedPatchIds: CheckpointId[] = [];
	for (const id of searchSpace.slice(0, options.config.singletonBudget)) {
		if (await repairs([id])) {
			removedPatchIds = [id];
			method = "singleton-removal";
			break;
		}
	}
	if (removedPatchIds.length === 0) {
		removedPatchIds = await ddmin(searchSpace, repairs);
	}
	if (removedPatchIds.length === 0) {
		return makeRecord({
			options,
			started,
			startedAt,
			probes,
			method: "abstain",
			candidates,
			priorOrder,
			causalPatchIds: [],
			removedPatchIds: [],
			usedFallback,
			abstainReason: "No sufficient patch-removal set was found.",
		});
	}

	if (!(await repairs(removedPatchIds))) {
		return makeRecord({
			options,
			started,
			startedAt,
			probes,
			method: "abstain",
			candidates,
			priorOrder,
			causalPatchIds: removedPatchIds,
			removedPatchIds,
			usedFallback,
			abstainReason: "The proposed removal set did not clear the failure.",
		});
	}

	const causalPatchIds = removedPatchIds;
	const plan = buildRollbackPlan(options.checkpoints, causalPatchIds, removedPatchIds);
	const skippedPatchIds = plan.skippedPatches.map((patch) => patch.id);
	if ((await probe(without(allPatchIds, skippedPatchIds))).failed) {
		return makeRecord({
			options,
			started,
			startedAt,
			probes,
			method: "abstain",
			candidates,
			priorOrder,
			causalPatchIds,
			removedPatchIds,
			usedFallback,
			abstainReason: "The dependency-safe replay plan did not clear the failure.",
		});
	}
	return makeRecord({
		options,
		started,
		startedAt,
		probes,
		method,
		candidates,
		priorOrder,
		causalPatchIds,
		removedPatchIds,
		usedFallback,
		plan,
	});
}

export function resolveCheckpointRefs(
	references: readonly string[],
	checkpoints: readonly { id: string; label: string }[],
): CheckpointId[] {
	const resolved: CheckpointId[] = [];
	for (const reference of references) {
		const matches = checkpoints.filter((checkpoint) => checkpoint.id === reference || checkpoint.label === reference);
		if (matches.length === 0) {
			throw new Error(`Unknown checkpoint reference: ${reference}`);
		}
		if (matches.length > 1) {
			throw new Error(`Ambiguous checkpoint label: ${reference}`);
		}
		const match = matches[0];
		if (!match) throw new Error(`Unknown checkpoint reference: ${reference}`);
		resolved.push(match.id);
	}
	return unique(resolved);
}

function assertLinearLineage(checkpoints: readonly { id: string; parentId?: string }[]): void {
	for (let index = 1; index < checkpoints.length; index++) {
		const checkpoint = checkpoints[index];
		const parent = checkpoints[index - 1];
		if (!checkpoint || !parent) throw new Error("Invalid checkpoint lineage.");
		if (checkpoint.parentId !== parent.id) {
			throw new Error(`Checkpoint ${checkpoint.id} is not a child of ${parent.id}.`);
		}
	}
}

function makeRecord(input: {
	options: DiagnosisOptions;
	started: number;
	startedAt: Date;
	probes: ProbeSummary[];
	method: DiagnosisRecord["method"];
	candidates: CheckpointId[];
	priorOrder: CheckpointId[];
	causalPatchIds: CheckpointId[];
	removedPatchIds: CheckpointId[];
	usedFallback: boolean;
	abstainReason?: string;
	plan?: DiagnosisRecord["plan"];
}): DiagnosisRecord {
	const prior = input.options.priorTelemetry;
	const telemetry: DiagnosisTelemetry = {
		startedAt: input.startedAt.toISOString(),
		completedAt: new Date().toISOString(),
		durationMs: Math.round(performance.now() - input.started),
		probeInvocations: input.probes.reduce((sum, probe) => sum + probe.repeats, 0),
		uniqueProbes: input.probes.length,
		probeCost: input.probes.reduce((sum, probe) => sum + probe.cost, 0) + (prior?.cost ?? 0),
		inputTokens: input.probes.reduce((sum, probe) => sum + probe.inputTokens, 0) + (prior?.inputTokens ?? 0),
		outputTokens: input.probes.reduce((sum, probe) => sum + probe.outputTokens, 0) + (prior?.outputTokens ?? 0),
		retries: input.probes.reduce((sum, probe) => sum + probe.retries, 0) + (prior?.retries ?? 0),
		model:
			prior?.model ??
			input.probes.flatMap((probe) => probe.observations).find((observation) => observation.model)?.model ??
			input.options.failure.metadata?.model,
		promptHash: input.options.failure.metadata?.promptHash,
		dataHash: input.options.failure.metadata?.dataHash,
		gitHash: input.options.gitHash ?? input.options.failure.metadata?.gitHash,
		configHash: input.options.configHash,
		failureHash: input.options.failureHash,
		usedFallback: input.usedFallback,
		abstainReason: input.abstainReason,
	};
	return {
		id: input.options.diagnosisId ?? `diag-${Date.now()}-${randomUUID().slice(0, 8)}`,
		failure: input.options.failure,
		method: input.method,
		candidatePatchIds: input.candidates,
		priorOrder: input.priorOrder,
		causalPatchIds: input.causalPatchIds,
		removedPatchIds: input.removedPatchIds,
		plan: input.plan,
		prior,
		probes: input.probes,
		telemetry,
	};
}

function without(ids: readonly CheckpointId[], removed: readonly CheckpointId[]): CheckpointId[] {
	const removedSet = new Set(removed);
	return ids.filter((id) => !removedSet.has(id));
}

function orderByPrior(ids: readonly CheckpointId[], prior: readonly CheckpointId[]): CheckpointId[] {
	return unique([...prior.filter((id) => ids.includes(id)), ...ids]);
}

function partition<T>(items: readonly T[], count: number): T[][] {
	const size = Math.ceil(items.length / count);
	const chunks: T[][] = [];
	for (let start = 0; start < items.length; start += size) {
		chunks.push(items.slice(start, start + size));
	}
	return chunks;
}

function unique<T>(items: readonly T[]): T[] {
	return [...new Set(items)];
}
