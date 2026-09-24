import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, rm, symlink, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { normalizeArtifactPath, ProjectStore } from "../src/state.ts";
import type { Checkpoint } from "../src/types.ts";

test("snapshot restore and independent delta replay preserve file contents", async () => {
	const cwd = await mkdtemp(path.join(os.tmpdir(), "pi-rollback-"));
	try {
		const artifactDirectory = path.join(cwd, ".pi", "evolving");
		await mkdir(artifactDirectory, { recursive: true });
		await writeFile(path.join(artifactDirectory, "base.txt"), "base\n");

		const store = new ProjectStore(cwd);
		const baseline = await store.createSnapshot([".pi/evolving"]);
		await writeFile(path.join(artifactDirectory, "gain.txt"), "gain\n");
		const changed = await store.createSnapshot([".pi/evolving"]);
		const changedFiles = await store.changedFiles(baseline.id, changed);
		assert.deepEqual(changedFiles, [".pi/evolving/gain.txt"]);

		await rm(artifactDirectory, { recursive: true });
		await store.restoreSnapshot(baseline.id);
		await assert.rejects(readFile(path.join(artifactDirectory, "gain.txt"), "utf8"), /ENOENT/);

		const baselineCheckpoint = makeCheckpoint("base", undefined, baseline.id, []);
		const changedCheckpoint = makeCheckpoint("gain", "base", changed.id, changedFiles);
		await store.applyCheckpointDelta(changedCheckpoint, baselineCheckpoint);
		assert.equal(await readFile(path.join(artifactDirectory, "base.txt"), "utf8"), "base\n");
		assert.equal(await readFile(path.join(artifactDirectory, "gain.txt"), "utf8"), "gain\n");
	} finally {
		await rm(cwd, { recursive: true, force: true });
	}
});

test("artifact paths cannot escape, include git internals, or overlap the store", () => {
	assert.throws(() => normalizeArtifactPath("."), /workspace root/);
	assert.throws(() => normalizeArtifactPath("../outside"), /workspace root/);
	assert.throws(() => normalizeArtifactPath(".git/objects"), /Git internals/);
	assert.throws(() => normalizeArtifactPath(".pi"), /rollback store/);
	assert.equal(normalizeArtifactPath(".pi/extensions/evolving"), ".pi/extensions/evolving");
});

test("snapshot rejects an artifact path that traverses a symlink", async () => {
	const cwd = await mkdtemp(path.join(os.tmpdir(), "pi-rollback-link-"));
	const outside = await mkdtemp(path.join(os.tmpdir(), "pi-rollback-outside-"));
	try {
		await mkdir(path.join(cwd, ".pi"), { recursive: true });
		await symlink(outside, path.join(cwd, ".pi", "linked"));
		const store = new ProjectStore(cwd);
		await assert.rejects(store.createSnapshot([".pi/linked/artifact"]), /traverses a symlink/);
	} finally {
		await rm(cwd, { recursive: true, force: true });
		await rm(outside, { recursive: true, force: true });
	}
});

test("restore rejects corrupted snapshot contents", async () => {
	const cwd = await mkdtemp(path.join(os.tmpdir(), "pi-rollback-corrupt-"));
	try {
		const artifactDirectory = path.join(cwd, ".pi", "evolving");
		await mkdir(artifactDirectory, { recursive: true });
		await writeFile(path.join(artifactDirectory, "state.txt"), "trusted\n");
		const store = new ProjectStore(cwd);
		const snapshot = await store.createSnapshot([".pi/evolving"]);
		await writeFile(
			path.join(store.snapshotDirectory, snapshot.id, "files", ".pi", "evolving", "state.txt"),
			"corrupted\n",
		);

		await assert.rejects(store.restoreSnapshot(snapshot.id), /hash mismatch/);
		assert.equal(await readFile(path.join(artifactDirectory, "state.txt"), "utf8"), "trusted\n");
	} finally {
		await rm(cwd, { recursive: true, force: true });
	}
});

function makeCheckpoint(
	id: string,
	parentId: string | undefined,
	snapshotId: string,
	changedFiles: string[],
): Checkpoint {
	return {
		id,
		label: id,
		parentId,
		snapshotId,
		createdAt: "2026-09-24T00:00:00.000Z",
		changedFiles,
		dependsOn: [],
	};
}
