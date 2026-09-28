# Valerie's Jobs

Valerie's Jobs is a scripted gameplay mod for The Sims 4 that turns joining a career into an application and interview process. Relevant skills influence the outcome, while some employers post deliberately fake “ghost jobs.”

Status: development scaffold / no playable release yet.

## Current prototype

The first script archive provides two live commands:

- `vj.hello` confirms that the mod loaded.
- `vj.test_apply <charisma> <primary_skill>` exercises the standalone scoring engine with supplied skill levels from 0 through 10.

The prototype does not intercept the career picker or assign careers yet.

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

