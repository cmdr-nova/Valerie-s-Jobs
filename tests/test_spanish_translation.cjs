const assert = require("node:assert/strict");
const test = require("node:test");
const fs = require("node:fs");
const path = require("node:path");
const { execFileSync } = require("node:child_process");
const { Package } = require("@s4tk/models");
const { validateTranslation, SPANISH_INSTANCE, CREDIT_INSTANCE } = require("../tools/spanish_translation");
const root = path.resolve(__dirname, "..");
function pack() { return Package.from(fs.readFileSync(path.join(root, "localization/es/BRODA_TS4.package"))); }
function table(pkg) { return pkg.entries.find(entry => entry.key.instance === SPANISH_INSTANCE); }
const originalKeys = [0x042dc034, 0xe3ac5520, 0xe1e13b87, 0xa61a9f2f, 0xa58982e0, 0xb0a5f214, 0x4925ed61, 0xf4eea8b8, 0x1e923aed];
const additions = JSON.parse(execFileSync("python3", [path.join(root, "tools/export_strings.py")], { encoding: "utf8" }));
const reference = [...originalKeys.map(key => ({ key, value: "Original tuning string without tokens" })), ...additions];

test("Spanish covers all keys and preserves English placeholder contracts", () => {
  const result = validateTranslation(pack(), reference);
  assert.equal(result.table.value.size, 106);
  assert.match(result.credit.value.entries[0].value, /BRØDA TS4/);
});
test("missing translation entry fails closed", () => {
  const pkg = pack(); table(pkg).value.deleteByKey(reference[0].key);
  assert.throws(() => validateTranslation(pkg, reference), /coverage/);
});
test("changed source placeholders require translator update", () => {
  const changed = reference.map(entry => entry.key === additions[0].key ? { ...entry, value: entry.value + " {9.String}" } : entry);
  assert.throws(() => validateTranslation(pack(), changed), /placeholders/);
});
test("blank translation fails closed", () => {
  const pkg = pack(); table(pkg).value.entries[0].value = " ";
  assert.throws(() => validateTranslation(pkg, reference), /Missing text/);
});
test("missing credit is rejected", () => {
  const pkg = pack(); pkg.deleteByKey(pkg.entries.find(entry => entry.key.instance === CREDIT_INSTANCE).key);
  assert.throws(() => validateTranslation(pkg, reference));
});
test("unexpected resources or locale are rejected", () => {
  const pkg = pack(); table(pkg).key = { ...table(pkg).key, instance: 0x00eb85778989bd91n };
  assert.throws(() => validateTranslation(pkg, reference), /Unexpected resource/);
});
