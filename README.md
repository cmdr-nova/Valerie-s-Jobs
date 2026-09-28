# Valerie's Jobs

Valerie's Jobs is a scripted gameplay mod for The Sims 4 that turns joining a career into an application and interview process. Relevant skills influence the outcome, while some employers post deliberately fake “ghost jobs.”

Status: playable interview vertical slice awaiting its second in-game smoke test on game version `1.128.90.1030`.

## Current prototype

The script archive provides these live development commands:

- `vj.hello` confirms that the mod loaded.
- `vj.test_apply <charisma> <primary_skill>` exercises the standalone scoring engine with supplied skill levels from 0 through 10.
- `vj.complete_interview` immediately completes the active Sim's pending interview for testing.

Normal player-confirmed career selections are now intercepted for mapped standard careers, active professions, and part-time jobs. Valerie's Jobs reads the Sim's real relevant skills, runs a one- or two-Sim-hour interview timer, shows a result notification with feedback, and invokes EA's original career join routine after an acceptance. Part-time jobs use an easier baseline. Noble, freelance/gig-style, and unknown careers fail open to EA's normal behavior.

The current slice uses a timed application state; the custom off-lot rabbit-hole interaction and save/reload persistence are the next milestones. Do not save, reload, or travel during this specific test build's short pending interview.

The first in-game test confirmed that the script loader and initial development commands work without a `lastException`. The career hook, notifications, timer, real skill reading, and career assignment still require an in-game test. See `docs/test-results.md`.

## Requirements

- The Sims 4 with script mods enabled
- Docker for the reproducible Python 3.7 compiler
- Python 3.10 or newer for repository tooling and tests
- Git

The game embeds Python 3.7. The project therefore compiles script bytecode in a pinned Python 3.7 container rather than using the host Python.

## Commands

```bash
make test
make build
make check-update
make extract-references
make deploy
```

`make deploy` copies only Valerie's Jobs artifacts into the configured `Mods/ValeriesJobs` folder. It does not alter saves or unrelated mods.

## Repository layout

- `src/valeries_jobs/` — game script and dependency-free domain logic
- `tools/` — build, deployment, reference extraction, and patch auditing
- `tests/` — host-side unit tests
- `compatibility/` — supported-version declaration and update snapshots
- `docs/` — development and compatibility documentation
- `dist/` — generated release artifacts; ignored by Git

## Copyright boundary

Extracted EA Python bytecode and game resources are placed under `.cache/`, ignored by Git, and must not be redistributed. Compatibility snapshots contain hashes and filenames only.
