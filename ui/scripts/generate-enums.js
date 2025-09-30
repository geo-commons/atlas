// eslint-disable-next-line @typescript-eslint/no-require-imports
const fs = require("node:fs");
// eslint-disable-next-line @typescript-eslint/no-require-imports
const path = require("node:path");

/* eslint-disable no-console */
const BASE_URL = process.env.ENUMS_BASE_URL || "http://localhost:8000/atlas/api/v1";

/** Generate TS contents given a typeName and items [{value,label}] */
function generateTs(typeName, items) {
  // Lowercase the first letter for variable names
  const lcTypeName = typeName.charAt(0).toLowerCase() + typeName.slice(1);

  // ID type (string union)
  const idType = `${typeName}Id`;
  const union = items.map((i) => JSON.stringify(i.value)).join(" | ");

  // Options array
  const optionsArray = items
    .map((i) => `  { id: ${JSON.stringify(i.value)}, label: ${JSON.stringify(i.label)} }`)
    .join(",\n");

  // Labels record (id -> label)
  const labelsRecord = items.map((i) => `  ${JSON.stringify(i.value)}: ${JSON.stringify(i.label)}`).join(",\n");

  return `/* AUTO-GENERATED FILE — do not edit, rather run npm install to get the most recent version of the types.
   * Source: ${new Date().toISOString()}
   * From: ${typeName} at build-time
   */
import { Option } from "./Option";

// ${typeName}
export type ${idType} = ${union};

export const ${lcTypeName}Options: Option<${idType}>[] = [
${optionsArray}
];

export const ${lcTypeName}Labels: Record<${idType}, string> = {
${labelsRecord}
};
`;
}

async function fetchJson(url) {
  const res = await fetch(url, { headers: { Accept: "application/json" } });
  if (!res.ok) {
    throw new Error(`${res.status} ${res.statusText} for ${url}`);
  }
  return res.json();
}

async function run() {
  const ENUM_SPECS = [
    { endpoint: "/metadatasets/topic-categories/", typeName: "TopicCategory" },
    { endpoint: "/metadatasets/role-types/", typeName: "RoleType" },
    { endpoint: "/metadatasets/update-method-types/", typeName: "UpdateMethodType" },
    { endpoint: "/metadatasets/authorization-level-types/", typeName: "AuthorizationLevelType" },
    { endpoint: "/metadatasets/status-types/", typeName: "StatusType" },
    { endpoint: "/metadatasets/access-constraints-types/", typeName: "AccessConstraintsType" },
    { endpoint: "/metadatasets/other-constraints-types/", typeName: "OtherConstraintsType" },
  ];

  console.log("▶ generating enum types from API…");

  const TYPES_DIR = path.join(process.cwd(), "src/types");

  const written = [];

  for (const spec of ENUM_SPECS) {
    const url = `${BASE_URL.replace(/\/$/, "")}${spec.endpoint}`;
    console.log(`  • ${spec.typeName} ← ${url}`);

    let data;
    try {
      data = await fetchJson(url);
    } catch (err) {
      console.error(`    ✖ failed to fetch ${url}:`, err.message);
      process.exitCode = 1;
      continue;
    }

    if (!Array.isArray(data)) {
      console.error(`    ✖ bad shape (expected array) for ${url}`);
      process.exitCode = 1;
      continue;
    }

    // validate shape minimally
    const items = data.filter((x) => x && typeof x.value === "string" && typeof x.label === "string");

    if (items.length === 0) {
      console.warn(`    ! no items for ${spec.typeName}; skipping`);
      continue;
    }

    // dedupe on value
    const seen = new Set();
    const deduped = [];
    for (const it of items) {
      if (seen.has(it.value)) continue;
      seen.add(it.value);
      deduped.push(it);
    }

    const ts = generateTs(spec.typeName, deduped);
    const outfile = path.join(TYPES_DIR, `${spec.typeName}.ts`);
    fs.writeFileSync(outfile, ts, "utf8");
    written.push(outfile);
    console.log(`    ✓ wrote ${path.relative(process.cwd(), outfile)}`);
  }

  // write index barrel
  if (written.length) {
    const index = written.map((p) => `export * from "./${path.basename(p, ".ts")}";`).join("\n") + "\n";
    fs.writeFileSync(path.join(TYPES_DIR, "index.ts"), index, "utf8");
    console.log(`  ✓ wrote types/index.ts`);
  }

  console.log("✔ done");
}

run().catch((e) => {
  console.error("unexpected error:", e);
  process.exit(1);
});
