# Valerie's Jobs

Valerie's Jobs is a scripted gameplay mod for The Sims 4 that turns joining a career into an application and interview process. Relevant skills influence the outcome, while some employers post deliberately fake “ghost jobs.”

Status: timed career interview and hiring flow verified in game; rabbit-hole/dialog revision awaiting verification on game version `1.128.90.1030`.

## Current prototype

The script archive provides these live development commands:

- `vj.hello` confirms that the mod loaded.
- `vj.test_apply <charisma> <primary_skill>` exercises the standalone scoring engine with supplied skill levels from 0 through 10.
- `vj.complete_interview` immediately completes the active Sim's pending interview for testing.

Normal player-confirmed career selections are intercepted for mapped standard careers, active professions, and part-time jobs. Valerie's Jobs reads the Sim's real relevant skills, sends the Sim into a one- or two-Sim-hour off-screen rabbit hole, shows modal result dialogs with feedback, and invokes EA's original career join routine after an acceptance. Part-time jobs use an easier baseline. Noble, freelance/gig-style, and unknown careers fail open to EA's normal behavior.

Save/reload persistence for pending application metadata remains a future milestone. Use a disposable save while verifying this development build.

The first in-game test confirmed the script loader without a `lastException`; the second confirmed career interception, skill-based timing/outcomes, and native career assignment. The new rabbit-hole and modal-dialog revision is the current test target. See `docs/test-results.md`.

## Requirements

- The Sims 4 with script mods enabled
- Docker for the reproducible Python 3.7 compiler
- Node.js and `npm install` for the tuning-package builder
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
