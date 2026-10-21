import assert from "node:assert/strict";
import {
	mkdtemp,
	mkdir,
	readFile,
	realpath,
	rm,
	writeFile,
} from "node:fs/promises";
import path from "node:path";
import test from "node:test";

import {
	buildCandidateToolDockerArgs,
	loadCandidateToolDefinitions,
	runCandidateTool,
	validateCandidateToolManifest,
} from "./candidate_tool_runtime.mjs";

const parameters = {
	type: "object",
	properties: {
		path: { type: "string" },
	},
	required: ["path"],
	additionalProperties: false,
};

test("candidate tool manifest is strict and rejects handler traversal", () => {
	const valid = {
		schema_version: 1,
		tools: [
			{
				name: "inspect_text",
				label: "Inspect Text",
				description: "Inspect repository text.",
				parameters,
				handler: "handlers/inspect_text.py",
				timeout_seconds: 30,
			},
		],
	};
	assert.equal(validateCandidateToolManifest(valid), valid);
	assert.throws(
		() =>
			validateCandidateToolManifest({
				...valid,
				tools: [{ ...valid.tools[0], handler: "../../host.py" }],
			}),
		/handler contract/,
	);
});

test("candidate handler container has no network or host write mount", () => {
	const args = buildCandidateToolDockerArgs({
		taskWorkspace: "/tasks/workspace",
		image: "swe-image",
		containerName: "candidate-test",
		handler: "/artifacts/candidate/handlers/inspect_text.py",
	});
	const joined = args.join(" ");
	assert.match(joined, /--network none/);
	assert.match(joined, /--read-only/);
	assert.match(
		joined,
		/\/artifacts\/candidate\/handlers\/inspect_text\.py:\/candidate\/handler\.py:ro/,
	);
	assert.match(joined, /\/tasks\/workspace:\/testbed:rw/);
	assert.match(joined, /\/testbed\/\.git:rw,nosuid,size=1m/);
	assert.doesNotMatch(joined, /docker\.sock|\/Users|:\/host/);
	assert.deepEqual(args.slice(-3), [
		"/usr/bin/env",
		"python3",
		"/candidate/handler.py",
	]);
});

test(
	"candidate handler can write only the task workspace and has no network",
	{ skip: !process.env.CANDIDATE_TOOL_TEST_IMAGE },
	async () => {
		const root = await mkdtemp(
			path.join(process.cwd(), ".candidate-tool-runtime-"),
		);
		const artifact = path.join(root, "artifact");
		const workspace = path.join(root, "workspace");
		try {
			await mkdir(path.join(artifact, "handlers"), { recursive: true });
			await mkdir(path.join(workspace, ".git"), { recursive: true });
			await writeFile(path.join(workspace, ".git", "HEAD"), "sensitive-history\n");
			const handler = path.join(artifact, "handlers", "inspect_text.py");
			await writeFile(
				handler,
				[
					"import json",
					"import pathlib",
					"import socket",
					"import sys",
					"request = json.load(sys.stdin)",
					"network_blocked = False",
					"try:",
					"    socket.create_connection(('1.1.1.1', 53), timeout=0.2)",
					"except OSError:",
					"    network_blocked = True",
					"artifact_read_only = False",
					"try:",
					"    pathlib.Path('/candidate/blocked.txt').write_text('bad')",
					"except OSError:",
					"    artifact_read_only = True",
					"pathlib.Path('/testbed/tool-result.txt').write_text(request['value'])",
					"host_absent = not pathlib.Path('/Users').exists()",
					"git_hidden = not pathlib.Path('/testbed/.git/HEAD').exists()",
					"print(json.dumps({'content': json.dumps({",
					"    'network_blocked': network_blocked,",
					"    'artifact_read_only': artifact_read_only,",
					"    'host_absent': host_absent,",
					"    'git_hidden': git_hidden,",
					"})}))",
				].join("\n"),
			);
			await writeFile(
				path.join(artifact, "tools.json"),
				JSON.stringify({
					schema_version: 1,
					tools: [
						{
							name: "inspect_text",
							label: "Inspect Text",
							description: "Inspect repository text.",
							parameters,
							handler: "handlers/inspect_text.py",
							timeout_seconds: 10,
						},
					],
				}),
			);
			const definitions = loadCandidateToolDefinitions({
				artifactPath: artifact,
				workspace,
				image: process.env.CANDIDATE_TOOL_TEST_IMAGE,
				instanceId: "runtime-isolation",
			});
			assert.deepEqual(
				definitions.map((definition) => definition.name),
				["inspect_text"],
			);
			const result = await runCandidateTool({
				taskWorkspace: await realpath(workspace),
				image: process.env.CANDIDATE_TOOL_TEST_IMAGE,
				instanceId: "runtime-isolation",
				toolCallId: "call-1",
				tool: {
					name: "inspect_text",
					timeout_seconds: 10,
				},
				handler: await realpath(handler),
				params: { value: "workspace-write-ok" },
			});
			assert.equal(
				result.details.exitCode,
				undefined,
				result.content[0].text,
			);
			const observed = JSON.parse(result.content[0].text);
			assert.deepEqual(observed, {
				network_blocked: true,
				artifact_read_only: true,
				host_absent: true,
				git_hidden: true,
			});
			assert.equal(
				await readFile(path.join(workspace, "tool-result.txt"), "utf8"),
				"workspace-write-ok",
			);
		} finally {
			await rm(root, { recursive: true, force: true });
		}
	},
);
