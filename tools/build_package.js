#!/usr/bin/env node

"use strict";

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const {
  Package,
  SimDataResource,
  StringTableResource,
  XmlResource,
} = require("@s4tk/models");
const {
  BinaryResourceType,
  SimDataGroup,
  TuningResourceType,
  StringTableLocale,
} = require("@s4tk/models/enums");

const root = path.resolve(__dirname, "..");
const tuningDir = path.join(root, "tuning");
const simDataDir = path.join(root, "simdata");
const outputDir = path.join(root, "dist");
const output = path.join(outputDir, "ValeriesJobs.package");
const modGroup = 0x80000000;

const tunings = [
  ["ValeriesJobs_AwayAction_JobInterview.xml", TuningResourceType.AwayAction, 11159348032265205096n],
  ["ValeriesJobs_Buff_InterviewAccepted.xml", TuningResourceType.Buff, 8465629208866944119n],
  ["ValeriesJobs_Buff_InterviewRejected.xml", TuningResourceType.Buff, 15001183660286003602n],
  ["ValeriesJobs_Buff_GhostListing.xml", TuningResourceType.Buff, 6217764197368866584n],
  ["ValeriesJobs_JobInterview_OneHour.xml", TuningResourceType.Interaction, 3593708283765050562n],
  ["ValeriesJobs_JobInterview_TwoHours.xml", TuningResourceType.Interaction, 11473922217750090871n],
  ["ValeriesJobs_RabbitHole_JobInterview_OneHour.xml", TuningResourceType.RabbitHole, 5556844565946566721n],
  ["ValeriesJobs_RabbitHole_JobInterview_TwoHours.xml", TuningResourceType.RabbitHole, 10092612624710672942n],
];

const resources = tunings.map(([filename, type, instance]) => ({
  key: { type, group: modGroup, instance },
  value: new XmlResource(fs.readFileSync(path.join(tuningDir, filename), "utf8")),
}));

const buffSimData = [
  ["ValeriesJobs_Buff_InterviewAccepted.xml", 8465629208866944119n],
  ["ValeriesJobs_Buff_InterviewRejected.xml", 15001183660286003602n],
  ["ValeriesJobs_Buff_GhostListing.xml", 6217764197368866584n],
];
for (const [filename, instance] of buffSimData) {
  resources.push({
    key: {
      type: BinaryResourceType.SimData,
      group: SimDataGroup.Buff,
      instance,
    },
    value: SimDataResource.fromXml(fs.readFileSync(path.join(simDataDir, filename))),
  });
}

const originalStrings = [
  { key: 0x042dc034, value: "Job Interview" },
  { key: 0xe3ac5520, value: "Attend Job Interview" },
  { key: 0xe1e13b87, value: "At Job Interview" },
  { key: 0xa61a9f2f, value: "Nailed the Interview" },
  {
    key: 0xa58982e0,
    value: "That handshake had offer-letter energy. The new job is theirs—and they know they earned it.",
  },
  { key: 0xb0a5f214, value: "Back to the Listings" },
  {
    key: 0x4925ed61,
    value: "No offer this time. It stings, but every interview makes the next one a little easier.",
  },
  { key: 0xf4eea8b8, value: "Ghosted by the Job" },
  {
    key: 0x1e923aed,
    value: "All that preparation for a position they never planned to fill. At least the interview outfit looked good.",
  },
];
const additions = JSON.parse(execFileSync("python3", [path.join(root, "tools/export_strings.py")], { encoding: "utf8" }));
const allStrings = [...originalStrings, ...additions];
if (new Set(allStrings.map(entry => entry.key)).size !== allStrings.length) {
  throw new Error("Duplicate STBL keys: preserve existing keys and resolve collisions before release.");
}
// English fallback in each supported language; translators replace the matching
// locale resource in a separate package. Existing English instance is unchanged.
for (const locale of Object.values(StringTableLocale).filter(value => typeof value === "number")) {
  resources.push({
    key: {
      type: BinaryResourceType.StringTable,
      group: modGroup,
      instance: (BigInt(locale) << 56n) | 0x00eb85778989bd91n,
    },
    value: new StringTableResource(allStrings),
  });
}

fs.mkdirSync(outputDir, { recursive: true });
fs.writeFileSync(path.join(outputDir, "translation-strings.json"), JSON.stringify(allStrings, null, 2) + "\n");

fs.mkdirSync(outputDir, { recursive: true });
const pkg = new Package(resources);
fs.writeFileSync(output, pkg.getBuffer(false, true));
process.stdout.write(`Built ${output} with ${resources.length} resources\n`);
