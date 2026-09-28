#!/usr/bin/env node

"use strict";

const fs = require("fs");
const path = require("path");
const { Package, StringTableResource, XmlResource } = require("@s4tk/models");
const { BinaryResourceType, TuningResourceType } = require("@s4tk/models/enums");

const root = path.resolve(__dirname, "..");
const tuningDir = path.join(root, "tuning");
const outputDir = path.join(root, "dist");
const output = path.join(outputDir, "ValeriesJobs.package");
const modGroup = 0x80000000;

const tunings = [
  ["ValeriesJobs_AwayAction_JobInterview.xml", TuningResourceType.AwayAction, 11159348032265205096n],
  ["ValeriesJobs_JobInterview_OneHour.xml", TuningResourceType.Interaction, 3593708283765050562n],
  ["ValeriesJobs_JobInterview_TwoHours.xml", TuningResourceType.Interaction, 11473922217750090871n],
  ["ValeriesJobs_RabbitHole_JobInterview_OneHour.xml", TuningResourceType.RabbitHole, 5556844565946566721n],
  ["ValeriesJobs_RabbitHole_JobInterview_TwoHours.xml", TuningResourceType.RabbitHole, 10092612624710672942n],
];

const resources = tunings.map(([filename, type, instance]) => ({
  key: { type, group: modGroup, instance },
  value: new XmlResource(fs.readFileSync(path.join(tuningDir, filename), "utf8")),
}));

const strings = new StringTableResource([
  { key: 0x042dc034, value: "Job Interview" },
  { key: 0xe3ac5520, value: "Attend Job Interview" },
  { key: 0xe1e13b87, value: "At Job Interview" },
]);
resources.push({
  key: {
    type: BinaryResourceType.StringTable,
    group: modGroup,
    instance: 0x00eb85778989bd91n,
  },
  value: strings,
});

fs.mkdirSync(outputDir, { recursive: true });
const pkg = new Package(resources);
fs.writeFileSync(output, pkg.getBuffer(false, true));
process.stdout.write(`Built ${output} with ${resources.length} resources\n`);
