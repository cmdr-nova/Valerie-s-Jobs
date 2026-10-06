"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { Package } = require("@s4tk/models");
const { BinaryResourceType, StringTableLocale } = require("@s4tk/models/enums");
const root = path.resolve(__dirname, "..");
const pkg = Package.from(fs.readFileSync(path.join(root, "dist/ValeriesJobs.package")));
const reference = JSON.parse(fs.readFileSync(path.join(root, "dist/translation-strings.json")));
const tables = pkg.entries.filter(entry => entry.key.type === BinaryResourceType.StringTable);
const locales = StringTableLocale.all();
assert.equal(tables.length, locales.length);
for (const locale of locales) {
  const instance = StringTableLocale.setHighByte(locale, 0x00eb85778989bd91n);
  const table = tables.find(entry => entry.key.instance === instance);
  assert.ok(table, `Missing locale ${locale}`);
  assert.equal(table.key.group, 0x80000000);
  assert.deepEqual(table.value.toJsonObject(false), reference.map(({ key, value }) => ({ key, value })));
}
const original = [0x042dc034, 0xe3ac5520, 0xe1e13b87, 0xa61a9f2f,
  0xa58982e0, 0xb0a5f214, 0x4925ed61, 0xf4eea8b8, 0x1e923aed];
for (const key of original) assert.ok(reference.some(entry => entry.key === key));
assert.equal(StringTableLocale.setHighByte(StringTableLocale.Spanish, 0x00eb85778989bd91n), 0x13eb85778989bd91n);
console.log(`Verified ${tables.length} locale STBLs, ${reference.length} entries each, and original keys.`);
