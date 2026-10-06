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
- The Noble career, freelance work, schools, retirement, and unsupported custom careers safely bypass the interview system

## Installation

1. Download the newest ZIP from the **Releases** page.
2. Extract `ValeriesJobs.package` and `ValeriesJobs.ts4script` into `Documents/Electronic Arts/The Sims 4/Mods/ValeriesJobs`.
3. Enable **Custom Content and Mods** and **Script Mods Allowed** in the game's options.
4. Restart The Sims 4.

Do not place the script more than one folder beneath `Mods`.

## Development status

The current `0.3.3-dev` build is an early testing release for The Sims 4 version `1.128.90.1030`. It adds complete gameplay-text localization support; the new localized dialogs still need in-game verification. The preceding interview flow, rabbit-hole presentation, career assignment, clean return, and visible acceptance moodlet passed in-game testing. Save/reload persistence for an interview already in progress is not implemented yet, so use a disposable save while testing.

## Translations

Interview messages, career/skill labels, action names and moodlets now use STBL entries. Translators can provide a separate localization `.package` without editing the script. The original nine keys remain unchanged; download `translation-strings.json` from the release for the complete string list. English fallback is included, but a Spanish translation is not bundled yet. See [translation instructions](docs/localization.md), including placeholders and the Spanish STBL instance.

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
