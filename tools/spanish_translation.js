"use strict";

const { BinaryResourceType } = require("@s4tk/models/enums");
const SPANISH_INSTANCE = 0x13eb85778989bd91n;
const CREDIT_INSTANCE = 0x13dd2cf5bfedb0e5n;

function tokens(value) {
  return [...value.matchAll(/\{[^{}]+\}/g)].map(match => match[0]).sort();
}

function validateTranslation(pkg, reference) {
  if (pkg.entries.length !== 2 || pkg.findRepeatedKeys().length) {
    throw new Error("Spanish package must contain exactly the translation and credit STBLs.");
  }
  for (const entry of pkg.entries) {
    if (entry.key.type !== BinaryResourceType.StringTable || entry.key.group !== 0x80000000 ||
        ![SPANISH_INSTANCE, CREDIT_INSTANCE].includes(entry.key.instance)) {
      throw new Error("Unexpected resource in Spanish translation package.");
    }
  }
  const table = pkg.entries.find(entry => entry.key.instance === SPANISH_INSTANCE);
  const credit = pkg.entries.find(entry => entry.key.instance === CREDIT_INSTANCE);
  if (!table || !credit || table.value.findRepeatedKeys().length || credit.value.size !== 1) {
    throw new Error("Missing/duplicate Spanish table or creator credit.");
  }
  const translated = table.value.toJsonObject(false);
  if (translated.length !== reference.length) throw new Error("Spanish translation coverage changed; coordinate with translator.");
  const byKey = new Map(translated.map(entry => [entry.key, entry.value]));
  for (const entry of reference) {
    const value = byKey.get(entry.key);
    if (typeof value !== "string" || !value.trim() || JSON.stringify(tokens(value)) !== JSON.stringify(tokens(entry.value))) {
      throw new Error(`Missing text or changed placeholders in Spanish key ${entry.key.toString(16)}.`);
    }
  }
  return { table, credit };
}

module.exports = { validateTranslation, SPANISH_INSTANCE, CREDIT_INSTANCE };
