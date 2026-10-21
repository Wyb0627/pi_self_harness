import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

const label = process.argv[2];
if (!label || !/^[a-z0-9-]+$/.test(label)) {
	throw new Error("Usage: node pi-rollback/fixtures/demo-step.mjs <lowercase-label>");
}

const directory = path.join(process.cwd(), ".pi", "rollback-demo");
await mkdir(directory, { recursive: true });
await writeFile(path.join(directory, `${label}.txt`), `${label}\n`, "utf8");
