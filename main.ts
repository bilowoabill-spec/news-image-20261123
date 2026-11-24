// main.ts — copy entry.png byte-identically to the output path.
//
// Usage:
//   MAKEFUN_OUTPUT_DIR=out node main.ts
//   node main.ts                       (defaults to /output/entry.png)
//
// Node 22, standard library only. The output is a byte-for-byte copy of
// the entry.png that sits next to this file (or in the working directory).

import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const PNG_MAGIC = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

// The bounty gate accepts at most 1 MiB per image.
const MAX_BYTES = 1_048_576;

function findEntryPng(): string {
  const candidates = [
    join(dirname(resolve(process.argv[1] ?? "main.ts")), "entry.png"),
    join(process.cwd(), "entry.png"),
  ];
  for (const candidate of candidates) {
    if (existsSync(candidate)) {
      return candidate;
    }
  }
  throw new Error(
    "entry.png not found next to main.ts or in the working directory",
  );
}

function main(): void {
  const src = findEntryPng();
  const data = readFileSync(src);
  if (data.length === 0) {
    throw new Error(`entry.png is empty: ${src}`);
  }
  if (!data.subarray(0, 8).equals(PNG_MAGIC)) {
    throw new Error(`entry.png is not a PNG file: ${src}`);
  }
  if (data.length > MAX_BYTES) {
    throw new Error(
      `entry.png is ${data.length} bytes, over the ${MAX_BYTES} byte limit: ${src}`,
    );
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const outPath = join(outDir, "entry.png");
  mkdirSync(outDir, { recursive: true });
  writeFileSync(outPath, data);

  // Read the copy back and confirm it matches the source byte for byte.
  const written = readFileSync(outPath);
  if (!written.equals(data)) {
    throw new Error(`written file does not match the source: ${outPath}`);
  }

  const sha = createHash("sha256").update(data).digest("hex");
  console.log(
    `Copied ${src} -> ${outPath} (${data.length} bytes, sha256 ${sha})`,
  );
}

main();
