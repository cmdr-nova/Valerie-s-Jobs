# Test results

## 2026-09-28 — Initial in-game smoke test

- Game version: `1.128.90.1030`
- Mod version: `0.0.1-dev`
- Artifact SHA-256: `081bda14b46e246eb3503155bfdaa876fc87bd3e3824477338c490f55152f5dd`
- `vj.hello`: passed; reported that Valerie's Jobs initialized
- `vj.test_apply 5 5`: passed; reported a 47% chance, rolled 28, and accepted
- `lastException`: none generated
- Compatibility result: promoted to `supported`
- User-supplied evidence: `/home/cmdr-nova/Pictures/Screenshots/Screenshot_2026-09-28_03-05-48.png`

This certifies the script loader, command registration, Python 3.7 bytecode, scoring calculation, randomized resolution, and cheat-console output. It does not yet certify career interception, career assignment, persistence, tuning resources, or interview interactions because those features are not implemented.

## 2026-09-28 — Interview vertical slice ready for test

- Mod version: `0.1.0-dev`
- Added mapped career interception, including Actor and known part-time jobs
- Added real skill reads and front-loaded entry-level scoring
- Added one- or two-Sim-hour interview timers
- Added success, rejection, and ghost-listing notifications
- Added native career assignment after acceptance
- Added `vj.complete_interview` to shorten development tests
- Host result: 14 unit tests passed; Python 3.7 script archive built

In-game result: passed. The user confirmed that career interception, the interview delay, outcome display, and hiring worked. This test did not cover a custom off-lot rabbit hole or modal result dialog.

## 2026-09-28 — Rabbit-hole and modal-dialog revision ready for test

- Mod version: `0.2.0-dev`
- Added Valerie-specific one-hour and two-hour managed rabbit-hole tunings
- Added a custom `At Job Interview` away action with no Actor audition rewards or buffs
- Replaced transient notifications with modal OK dialogs
- Kept a timed fallback if the tuning package cannot be loaded
- In-game result: pending
