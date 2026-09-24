import { createHash, randomUUID } from "node:crypto";
import { chmod, copyFile, lstat, mkdir, readdir, readFile, rename, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import type {
	ArtifactFile,
	ArtifactRoot,
	Checkpoint,
	FailureBundle,
	RollbackConfig,
	SnapshotManifest,
} from "./types.ts";

const DEFAULT_CONFIG: Omit<RollbackConfig, "artifactPaths" | "probeCommand"> = {
	probeRepeats: 1,
	timeoutMs: 300_000,
	maxSliceFraction: 0.3,
	minSliceRecall: 0.95,
	singletonBudget: 1,
	dryRun: true,
};

export class ProjectStore {
	readonly cwd: string;
	readonly rootDirectory: string;
	readonly snapshotDirectory: string;
	readonly runDirectory: string;

	constructor(cwd: string) {
		this.cwd = path.resolve(cwd);
		this.rootDirectory = path.join(this.cwd, ".pi", "rollback");
		this.snapshotDirectory = path.join(this.rootDirectory, "artifacts");
		this.runDirectory = path.join(this.rootDirectory, "runs");
	}

	async loadConfig(configPath = path.join(this.cwd, ".pi", "rollback.json")): Promise<RollbackConfig> {
		const raw = parseObject(await readFile(configPath, "utf8"), configPath);
		const artifactPaths = stringArray(raw.artifactPaths, "artifactPaths").map((entry) => normalizeArtifactPath(entry));
		assertNonOverlappingRoots(artifactPaths);
		const probeCommand = stringArray(raw.probeCommand, "probeCommand");
		const priorCommand = raw.priorCommand === undefined ? undefined : stringArray(raw.priorCommand, "priorCommand");
		const config: RollbackConfig = {
			artifactPaths,
			probeCommand,
			priorCommand,
			probeRepeats: optionalNumber(raw.probeRepeats, DEFAULT_CONFIG.probeRepeats),
			timeoutMs: optionalNumber(raw.timeoutMs, DEFAULT_CONFIG.timeoutMs),
			maxSliceFraction: optionalNumber(raw.maxSliceFraction, DEFAULT_CONFIG.maxSliceFraction),
			minSliceRecall: optionalNumber(raw.minSliceRecall, DEFAULT_CONFIG.minSliceRecall),
			singletonBudget: optionalNumber(raw.singletonBudget, DEFAULT_CONFIG.singletonBudget),
			dryRun: optionalBoolean(raw.dryRun, DEFAULT_CONFIG.dryRun),
		};
		if (config.artifactPaths.length === 0) throw new Error("artifactPaths cannot be empty.");
		if (config.probeCommand.length === 0) throw new Error("probeCommand cannot be empty.");
		if (config.probeRepeats < 1 || config.probeRepeats % 2 === 0) {
			throw new Error("probeRepeats must be a positive odd integer.");
		}
		if (!Number.isInteger(config.probeRepeats)) throw new Error("probeRepeats must be an integer.");
		if (config.timeoutMs <= 0) throw new Error("timeoutMs must be positive.");
		if (config.maxSliceFraction <= 0 || config.maxSliceFraction > 1) {
			throw new Error("maxSliceFraction must be in (0, 1].");
		}
		if (config.minSliceRecall < 0 || config.minSliceRecall > 1) {
			throw new Error("minSliceRecall must be in [0, 1].");
		}
		if (!Number.isInteger(config.singletonBudget) || config.singletonBudget < 0) {
			throw new Error("singletonBudget must be a non-negative integer.");
		}
		return config;
	}

	async loadFailureBundle(filePath: string): Promise<FailureBundle> {
		const absolutePath = path.resolve(this.cwd, filePath);
		const raw = parseObject(await readFile(absolutePath, "utf8"), absolutePath);
		if (typeof raw.id !== "string" || raw.id.trim() === "") {
			throw new Error("Failure bundle id must be a non-empty string.");
		}
		if (typeof raw.summary !== "string" || raw.summary.trim() === "") {
			throw new Error("Failure bundle summary must be a non-empty string.");
		}
		return {
			id: raw.id,
			summary: raw.summary,
			candidatePatches:
				raw.candidatePatches === undefined ? undefined : stringArray(raw.candidatePatches, "candidatePatches"),
			priorOrder: raw.priorOrder === undefined ? undefined : stringArray(raw.priorOrder, "priorOrder"),
			sliceAuditRecall:
				raw.sliceAuditRecall === undefined ? undefined : requiredNumber(raw.sliceAuditRecall, "sliceAuditRecall"),
			metadata:
				raw.metadata === undefined
					? undefined
					: (parseRecord(raw.metadata, "failure metadata") as FailureBundle["metadata"]),
		};
	}

	async createSnapshot(artifactPaths: readonly string[]): Promise<SnapshotManifest> {
		await mkdir(this.snapshotDirectory, { recursive: true });
		const tempDirectory = path.join(this.rootDirectory, `snapshot-${randomUUID()}`);
		const filesDirectory = path.join(tempDirectory, "files");
		await mkdir(filesDirectory, { recursive: true });

		const roots: ArtifactRoot[] = [];
		const files: ArtifactFile[] = [];
		try {
			for (const artifactPath of artifactPaths) {
				const source = path.join(this.cwd, artifactPath);
				const destination = path.join(filesDirectory, artifactPath);
				await assertNoSymlinkComponents(this.cwd, artifactPath);
				const stat = await lstat(source).catch((error: unknown) => {
					if (isMissingError(error)) return undefined;
					throw error;
				});
				if (!stat) {
					roots.push({ path: artifactPath, kind: "missing" });
					continue;
				}
				if (stat.isSymbolicLink()) throw new Error(`Symlink artifact roots are not supported: ${artifactPath}`);
				if (stat.isFile()) {
					roots.push({ path: artifactPath, kind: "file" });
					await copySnapshotFile(source, destination, artifactPath, stat.mode, files);
					continue;
				}
				if (!stat.isDirectory()) throw new Error(`Unsupported artifact type: ${artifactPath}`);
				roots.push({ path: artifactPath, kind: "directory" });
				await mkdir(destination, { recursive: true });
				await copySnapshotTree(source, destination, artifactPath, files);
			}

			files.sort((left, right) => left.path.localeCompare(right.path));
			const id = hashValue({ artifactPaths, roots, files });
			const manifest: SnapshotManifest = {
				id,
				createdAt: new Date().toISOString(),
				artifactPaths: [...artifactPaths],
				roots,
				files,
			};
			await writeJson(path.join(tempDirectory, "manifest.json"), manifest);
			const targetDirectory = path.join(this.snapshotDirectory, id);
			const exists = await pathExists(targetDirectory);
			if (exists) {
				await rm(tempDirectory, { recursive: true, force: true });
			} else {
				await rename(tempDirectory, targetDirectory);
			}
			return manifest;
		} catch (error) {
			await rm(tempDirectory, { recursive: true, force: true });
			throw error;
		}
	}

	async readSnapshot(id: string): Promise<SnapshotManifest> {
		const manifestPath = path.join(this.snapshotDirectory, id, "manifest.json");
		const parsed = JSON.parse(await readFile(manifestPath, "utf8")) as SnapshotManifest;
		if (parsed.id !== id || !Array.isArray(parsed.files) || !Array.isArray(parsed.roots)) {
			throw new Error(`Invalid snapshot manifest: ${manifestPath}`);
		}
		const artifactPaths = parsed.artifactPaths.map((entry) => normalizeArtifactPath(entry));
		assertNonOverlappingRoots(artifactPaths);
		if (parsed.roots.length !== artifactPaths.length) {
			throw new Error(`Snapshot roots do not match artifactPaths: ${manifestPath}`);
		}
		for (const root of parsed.roots) {
			if (!artifactPaths.includes(normalizeArtifactPath(root.path))) {
				throw new Error(`Unexpected snapshot root: ${root.path}`);
			}
		}
		for (const file of parsed.files) {
			const normalized = normalizeArtifactPath(file.path);
			if (!artifactPaths.some((root) => normalized === root || normalized.startsWith(`${root}/`))) {
				throw new Error(`Snapshot file is outside configured artifact roots: ${file.path}`);
			}
		}
		const expectedId = hashValue({
			artifactPaths: parsed.artifactPaths,
			roots: parsed.roots,
			files: parsed.files,
		});
		if (expectedId !== id) throw new Error(`Snapshot manifest hash mismatch: ${manifestPath}`);
		return parsed;
	}

	async changedFiles(parentSnapshotId: string | undefined, child: SnapshotManifest): Promise<string[]> {
		if (!parentSnapshotId) return child.files.map((file) => file.path);
		const parent = await this.readSnapshot(parentSnapshotId);
		const before = new Map(parent.files.map((file) => [file.path, file.sha256]));
		const after = new Map(child.files.map((file) => [file.path, file.sha256]));
		const changed = new Set<string>();
		for (const file of parent.files) {
			if (after.get(file.path) !== file.sha256) changed.add(file.path);
		}
		for (const file of child.files) {
			if (before.get(file.path) !== file.sha256) changed.add(file.path);
		}
		const parentRoots = new Map(parent.roots.map((root) => [root.path, root.kind]));
		for (const root of child.roots) {
			if (parentRoots.get(root.path) !== root.kind) changed.add(root.path);
		}
		return [...changed].sort();
	}

	async restoreSnapshot(snapshotId: string): Promise<void> {
		const manifest = await this.readSnapshot(snapshotId);
		await this.verifySnapshotFiles(manifest);
		const transaction = path.join(this.rootDirectory, `restore-${randomUUID()}`);
		const staged = path.join(transaction, "staged");
		const backup = path.join(transaction, "backup");
		await mkdir(staged, { recursive: true });
		await mkdir(backup, { recursive: true });

		for (const root of manifest.roots) {
			if (root.kind === "missing") continue;
			const source = path.join(this.snapshotDirectory, snapshotId, "files", root.path);
			const destination = path.join(staged, root.path);
			await copyPath(source, destination);
		}

		const moved: ArtifactRoot[] = [];
		try {
			for (const root of manifest.roots) {
				await assertNoSymlinkComponents(this.cwd, root.path);
				const target = path.join(this.cwd, root.path);
				const backupPath = path.join(backup, root.path);
				if (await pathExists(target)) {
					await mkdir(path.dirname(backupPath), { recursive: true });
					await rename(target, backupPath);
				}
				moved.push(root);
				if (root.kind !== "missing") {
					await mkdir(path.dirname(target), { recursive: true });
					await rename(path.join(staged, root.path), target);
				}
			}
		} catch (error) {
			for (const root of moved.reverse()) {
				const target = path.join(this.cwd, root.path);
				const backupPath = path.join(backup, root.path);
				await rm(target, { recursive: true, force: true });
				if (await pathExists(backupPath)) {
					await mkdir(path.dirname(target), { recursive: true });
					await rename(backupPath, target);
				}
			}
			throw error;
		} finally {
			await rm(transaction, { recursive: true, force: true });
		}
	}

	async applyCheckpointDelta(checkpoint: Checkpoint, parent: Checkpoint): Promise<void> {
		const childManifest = await this.readSnapshot(checkpoint.snapshotId);
		const parentManifest = await this.readSnapshot(parent.snapshotId);
		await this.verifySnapshotFiles(childManifest, new Set(checkpoint.changedFiles));
		const childFiles = new Map(childManifest.files.map((file) => [file.path, file]));
		const parentFiles = new Map(parentManifest.files.map((file) => [file.path, file]));

		for (const changedPath of checkpoint.changedFiles) {
			await assertNoSymlinkComponents(this.cwd, changedPath);
			const childRoot = childManifest.roots.find((root) => root.path === changedPath);
			if (childRoot) {
				const target = path.join(this.cwd, changedPath);
				if (childRoot.kind === "missing") {
					await rm(target, { recursive: true, force: true });
				} else if (childRoot.kind === "directory") {
					await mkdir(target, { recursive: true });
				}
			}

			const childFile = childFiles.get(changedPath);
			if (childFile) {
				await replaceFile(
					path.join(this.snapshotDirectory, checkpoint.snapshotId, "files", changedPath),
					path.join(this.cwd, changedPath),
					childFile.mode,
				);
			} else if (parentFiles.has(changedPath)) {
				await rm(path.join(this.cwd, changedPath), { force: true });
			}
		}
	}

	async writeRun(id: string, value: unknown): Promise<string> {
		const directory = path.join(this.runDirectory, id);
		await mkdir(directory, { recursive: true });
		const outputPath = path.join(directory, "result.json");
		await writeJson(outputPath, value);
		return outputPath;
	}

	private async verifySnapshotFiles(manifest: SnapshotManifest, selected?: ReadonlySet<string>): Promise<void> {
		for (const file of manifest.files) {
			if (selected && !selected.has(file.path)) continue;
			const filePath = path.join(this.snapshotDirectory, manifest.id, "files", file.path);
			const content = await readFile(filePath);
			const actualHash = createHash("sha256").update(content).digest("hex");
			if (actualHash !== file.sha256) {
				throw new Error(`Snapshot file hash mismatch: ${file.path}`);
			}
		}
	}
}

export function hashValue(value: unknown): string {
	return createHash("sha256").update(JSON.stringify(value)).digest("hex");
}

export function normalizeArtifactPath(input: string): string {
	if (path.isAbsolute(input)) throw new Error(`Artifact path must be relative: ${input}`);
	const normalized = path.normalize(input).split(path.sep).join("/");
	if (normalized === "." || normalized === ".." || normalized.startsWith("../")) {
		throw new Error(`Artifact path cannot escape or equal the workspace root: ${input}`);
	}
	if (normalized === ".git" || normalized.startsWith(".git/")) {
		throw new Error(`Git internals cannot be managed as rollback artifacts: ${input}`);
	}
	if (
		normalized === ".pi/rollback" ||
		normalized.startsWith(".pi/rollback/") ||
		".pi/rollback".startsWith(`${normalized}/`)
	) {
		throw new Error(`Artifact path overlaps the rollback store: ${input}`);
	}
	return normalized;
}

function assertNonOverlappingRoots(roots: readonly string[]): void {
	const uniqueRoots = new Set(roots);
	if (uniqueRoots.size !== roots.length) throw new Error("artifactPaths contains duplicates.");
	for (const root of roots) {
		for (const other of roots) {
			if (root !== other && other.startsWith(`${root}/`)) {
				throw new Error(`Artifact paths cannot overlap: ${root} and ${other}`);
			}
		}
	}
}

async function copySnapshotTree(
	source: string,
	destination: string,
	relativePath: string,
	files: ArtifactFile[],
): Promise<void> {
	const entries = await readdir(source, { withFileTypes: true });
	entries.sort((left, right) => left.name.localeCompare(right.name));
	for (const entry of entries) {
		const entrySource = path.join(source, entry.name);
		const entryDestination = path.join(destination, entry.name);
		const entryRelative = `${relativePath}/${entry.name}`;
		if (entry.isSymbolicLink()) throw new Error(`Symlinks are not supported in artifacts: ${entryRelative}`);
		if (entry.isDirectory()) {
			await mkdir(entryDestination, { recursive: true });
			await copySnapshotTree(entrySource, entryDestination, entryRelative, files);
			continue;
		}
		if (!entry.isFile()) throw new Error(`Unsupported artifact type: ${entryRelative}`);
		const stat = await lstat(entrySource);
		await copySnapshotFile(entrySource, entryDestination, entryRelative, stat.mode, files);
	}
}

async function copySnapshotFile(
	source: string,
	destination: string,
	relativePath: string,
	mode: number,
	files: ArtifactFile[],
): Promise<void> {
	await mkdir(path.dirname(destination), { recursive: true });
	await copyFile(source, destination);
	await chmod(destination, mode & 0o777);
	const content = await readFile(destination);
	files.push({
		path: relativePath,
		sha256: createHash("sha256").update(content).digest("hex"),
		size: content.byteLength,
		mode: mode & 0o777,
	});
}

async function copyPath(source: string, destination: string): Promise<void> {
	const stat = await lstat(source);
	if (stat.isFile()) {
		await mkdir(path.dirname(destination), { recursive: true });
		await copyFile(source, destination);
		await chmod(destination, stat.mode & 0o777);
		return;
	}
	if (!stat.isDirectory()) throw new Error(`Unsupported snapshot entry: ${source}`);
	await mkdir(destination, { recursive: true });
	for (const entry of await readdir(source, { withFileTypes: true })) {
		if (entry.isSymbolicLink()) throw new Error(`Snapshot contains a symlink: ${path.join(source, entry.name)}`);
		await copyPath(path.join(source, entry.name), path.join(destination, entry.name));
	}
}

async function replaceFile(source: string, target: string, mode: number): Promise<void> {
	await mkdir(path.dirname(target), { recursive: true });
	const temp = `${target}.rollback-${randomUUID()}`;
	try {
		await copyFile(source, temp);
		await chmod(temp, mode);
		await rename(temp, target);
	} finally {
		await rm(temp, { force: true });
	}
}

async function writeJson(filePath: string, value: unknown): Promise<void> {
	await mkdir(path.dirname(filePath), { recursive: true });
	const temp = `${filePath}.${randomUUID()}.tmp`;
	await writeFile(temp, `${JSON.stringify(value, null, 2)}\n`, "utf8");
	await rename(temp, filePath);
}

async function pathExists(filePath: string): Promise<boolean> {
	try {
		await lstat(filePath);
		return true;
	} catch (error) {
		if (isMissingError(error)) return false;
		throw error;
	}
}

async function assertNoSymlinkComponents(cwd: string, relativePath: string): Promise<void> {
	let current = cwd;
	for (const component of relativePath.split("/")) {
		current = path.join(current, component);
		const stat = await lstat(current).catch((error: unknown) => {
			if (isMissingError(error)) return undefined;
			throw error;
		});
		if (!stat) return;
		if (stat.isSymbolicLink()) {
			throw new Error(`Artifact path traverses a symlink: ${relativePath}`);
		}
	}
}

function parseObject(content: string, source: string): Record<string, unknown> {
	let parsed: unknown;
	try {
		parsed = JSON.parse(content);
	} catch (error) {
		throw new Error(`Invalid JSON in ${source}: ${error instanceof Error ? error.message : String(error)}`);
	}
	return parseRecord(parsed, source);
}

function parseRecord(value: unknown, field: string): Record<string, unknown> {
	if (typeof value !== "object" || value === null || Array.isArray(value)) {
		throw new Error(`${field} must be a JSON object.`);
	}
	return value as Record<string, unknown>;
}

function stringArray(value: unknown, field: string): string[] {
	if (!Array.isArray(value) || !value.every((entry) => typeof entry === "string")) {
		throw new Error(`${field} must be a string array.`);
	}
	return value;
}

function requiredNumber(value: unknown, field: string): number {
	if (typeof value !== "number" || !Number.isFinite(value)) {
		throw new Error(`${field} must be a finite number.`);
	}
	return value;
}

function optionalNumber(value: unknown, fallback: number): number {
	return value === undefined ? fallback : requiredNumber(value, "numeric config value");
}

function optionalBoolean(value: unknown, fallback: boolean): boolean {
	if (value === undefined) return fallback;
	if (typeof value !== "boolean") throw new Error("Boolean config value expected.");
	return value;
}

function isMissingError(error: unknown): boolean {
	return error instanceof Error && "code" in error && error.code === "ENOENT";
}
