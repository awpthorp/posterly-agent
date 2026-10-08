import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
const read = (file) => readFile(file, "utf8");
const json = async (file) => JSON.parse(await read(file));
const claude = await json(".claude-plugin/plugin.json");
const cursor = await json("plugins/posterly/.cursor-plugin/plugin.json");
const gemini = await json("gemini-extension.json");
assert.equal(claude.version, cursor.version);
assert.equal(claude.version, gemini.version);
for (const file of [".claude-plugin/marketplace.json", ".cursor-plugin/marketplace.json"]) {
  assert.equal((await json(file)).metadata.version, claude.version, file);
}
const registry = await json("registry/server.json");
assert.equal(registry.version, registry.packages[0].version);
for (const file of [".mcp.json", "plugins/posterly/mcp.json", "gemini-extension.json"]) {
  const server = (await json(file)).mcpServers.posterly;
  assert.equal(server.command, "npx", file);
  assert.deepEqual(server.args, ["-y", `posterly-mcp-server@${registry.version}`], file);
}
const skill = await read("skills/posterly/SKILL.md");
assert.equal(await read("SKILL.md"), skill);
assert.equal(await read("plugins/posterly/skills/posterly/SKILL.md"), skill);
assert.equal(await read("skills/setup/SKILL.md"), await read("plugins/posterly/skills/setup/SKILL.md"));
for (const file of ["skills/posterly/SKILL.md", "skills/setup/SKILL.md", "plugins/posterly/commands/setup.md", "README.md"]) {
  const content = await read(file);
  assert(!content.includes("@latest"), `${file}: launcher must have an exact version`);
  assert(!/^allowed-tools:/m.test(content), `${file}: shell approvals belong to the user`);
}
assert(gemini.settings.some((setting) => setting.envVar === "POSTERLY_API_KEY" && setting.sensitive === true));
await read(gemini.contextFileName);
const icon = await readFile(".claude-plugin/icon.png");
assert.equal(icon.readUInt32BE(16), 512);
assert.equal(icon.readUInt32BE(20), 512);
assert(icon.length < 2 * 1024 * 1024);
console.log(`Distribution validation passed: plugin ${claude.version}, MCP ${registry.version}`);
