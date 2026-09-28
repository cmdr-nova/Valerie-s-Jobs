![Valerie's Jobs promotional banner](assets/valeries-jobs-banner-v1.png)

# Valerie's Jobs

Valerie's Jobs is a scripted gameplay mod for The Sims 4 that turns choosing a career into an actual hiring process.

Instead of joining immediately, your Sim travels to a one- or two-hour off-screen interview. Their relevant skills influence the result, beginner Sims still receive a fair chance, and a successful interview places them directly into the career. Occasionally, an employer may post a “ghost job” that was never genuinely available.

## Current features

- Skill-based interviews for supported full-time and part-time careers
- One- or two-hour rabbit-hole interviews
- Modal acceptance and rejection results with feedback
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

The current `0.2.3-dev` build is an early testing release for The Sims 4 version `1.128.90.1030`. The main interview flow, rabbit-hole presentation, outcome dialogs, and career assignment have passed in-game testing. Save/reload persistence for an interview already in progress is not implemented yet, so use a disposable save while testing.

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
