# Translation support (0.3.4-dev)

Normal gameplay dialogs, moodlets, interview action names, career labels and
skill labels use STBL entries. Debug cheat-console output and logs remain English.
No script changes are required for translation. Neutral Spanish by **BRØDA TS4**
is bundled starting with 0.3.4-dev. Other locales retain English fallback tables.
The original contributed package and credit are preserved in localization/es.
Remove an older standalone Spanish override when installing the bundled version.

## Separate translation package

Open ValeriesJobs.package in a Sims 4 localization editor and translate the STBL
for your language into a separate .package. Preserve resource type, group,
locale-specific instance and every string key. Include the WHOLE translated
table: an override can replace the entire STBL, so old nine-entry translations
must be updated. Ensure your translation overrides the base language resource
in package load order, then test in your game language. Do not replace the mod's
functional package or script; install your localization alongside them.

- STBL type: `0x220557DA`; group: `0x80000000`.
- English instance: `0x00EB85778989BD91` (unchanged).
- Spanish instance: `0x13EB85778989BD91`.

Preserve `{0.String}` and `{1.Number}` placeholders exactly; reorder them freely.
String tokens can contain names, localized career/skill labels or nested feedback.
The number token in result.body is the chance percentage. One-hour and two-hour
start messages are separate sentences, without an English plural suffix.

New keys are CRC32 of UTF-8 `valeries_jobs.` plus identifier; identifiers must
remain stable even when English wording changes. Career identifiers use tuning
IDs. Original nine tuning/moodlet keys remain unchanged.

Dialog source: localization/strings.json. Label source: catalog.py, exported by
tools/export_strings.py. These English catalog labels are build/diagnostic data,
not raw dialog tokens. make build exports the COMPLETE key/text list (including
the original nine entries) to dist/translation-strings.json. Tagged releases
attach that list for translators.

Test start (both durations), already scheduled, cancellation, acceptance (both
feedback variants), rejection (three variants), ghost listing and all moodlets.
Translate skill/career labels too. Automated checks do not replace in-game
Spanish and English smoke tests.
