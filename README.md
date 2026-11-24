![Valerie's Jobs promotional banner](assets/valeries-jobs-banner-v1.png)

# Valerie's Jobs

Valerie's Jobs is a scripted gameplay mod for The Sims 4 that turns choosing a career into an actual hiring process.

Instead of joining immediately, your Sim travels to a one- or two-hour off-screen interview. Their relevant skills influence the result, beginner Sims still receive a fair chance, and a successful interview places them directly into the career. Occasionally, an employer may post a “ghost job” that was never genuinely available.

## Current features

- Skill-based interviews for supported full-time and part-time careers
- One- or two-hour rabbit-hole interviews
- Modal acceptance and rejection results with feedback
- Temporary Confident, Sad, or Scared moodlets with outcome-specific flavor text
- Easier expectations for entry-level and part-time applicants
- A small chance of encountering a fake job listing
- Automatic career assignment after a successful interview
- Optional one-use cheat to skip the selected Sim's next interview and join immediately
- The Noble career, freelance work, schools, retirement, and unsupported custom careers safely bypass the interview system

## Installation

1. Download the newest ZIP from the **Releases** page.
2. Extract `ValeriesJobs.package` and `ValeriesJobs.ts4script` into `Documents/Electronic Arts/The Sims 4/Mods/ValeriesJobs`.
3. Enable **Custom Content and Mods** and **Script Mods Allowed** in the game's options.
4. Restart The Sims 4.

Do not place the script more than one folder beneath `Mods`.

## Development status

The current `0.3.5` release adds a one-use interview skip cheat. On November 24, 2026, the user verified immediate entry into Detective with the cheat, then confirmed that applying again without re-entering it required an interview. This focused test used The Sims 4 `1.129.39.1030`; it is not a complete certification of all features on that patch. The previous compatibility baseline is `1.128.90.1030`.

Spanish localization remains bundled. The earlier English application/interview flow, popups, and outcome moodlet passed in-game testing; Spanish rendering still needs in-game verification. Saving/reloading during an interview is not supported: finish interviews before saving and exiting, and back up saves before testing.

## Skip an interview (0.3.5 and later)

For setting up a new save or storytelling, select the Sim in Live Mode, open the cheat console (`Ctrl+Shift+C`), and enter:

```text
vj.skip_next_interview
```

Then apply for a supported job normally. That Sim joins immediately without an interview, skill roll, ghost listing, or interview-outcome moodlet. Normal career replacement confirmations and shift/agency selections are preserved. The skip is used only after the Sim actually joins; canceling a picker or confirmation does not use it. Other Sims still need interviews.

Enter `vj.skip_next_interview false` to cancel an unused skip. Repeating the command does not stack skips. Unsupported careers and Noble do not consume it. Finish or cancel an existing interview before arming the cheat. Unused skips last only for the current game session, not across a game restart. `testingcheats true` is not required.

## Translations

**Spanish translation: [BRØDA TS4](https://www.patreon.com/BR0DA_TS4/posts/valeries-jobs-v0-171744476).** The complete neutral Spanish translation is bundled with permission reported by the author, and its internal creator credit is preserved. Thank you for contributing!

Interview messages, career/skill labels, action names and moodlets use STBL entries. Spanish is included automatically for Spanish-language games; other supported languages retain English fallback. Installation remains the same two files. Remove any older standalone Valerie's Jobs Spanish translation package when updating to avoid stale overrides.

Translators can still provide separate localization packages without editing the script. Existing keys are unchanged; download `translation-strings.json` from the release for the complete source list. See [translation instructions](docs/localization.md). Bundled translation sources are in [localization/es](localization/es); inclusion does not imply a blanket license for unrelated reuse.

Please report bugs through GitHub Issues and include your game version, mod version, what your Sim was doing, and any `lastException` file.

## Building from source

The game embeds Python 3.7. This project uses Docker for reproducible Python 3.7 bytecode, Node.js for the tuning package, and host-side Python tests.

```bash
npm install
make test
make build
```

Extracted EA code and game resources are used only as local compatibility references. They are excluded from the repository and are not redistributed.

## Disclaimer

This is an unofficial fan-made mod and is not affiliated with or endorsed by Electronic Arts or Maxis.
