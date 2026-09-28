# EA patch compatibility workflow

Valerie's Jobs treats each game patch as unverified until its relevant interfaces have been reviewed and tested.

## What is monitored

- The reported game version
- Whole-file hashes for the game's Python archives, generated API archive, and primary simulation tuning packages
- Individual hashes for career tracking, career selection, active-career, acting, and Noble-career Python modules

Snapshots contain hashes only. They do not copy or redistribute EA code.

## After an EA update

1. Run `make check-update`.
2. If review is required, run `make snapshot-update` to record the new installation state.
3. Compare the old and new snapshots with `python3 tools/compatibility.py diff OLD NEW`.
4. Refresh local API references with `make extract-references`.
5. Review every changed monitored module and any affected tuning.
6. Run `make test` and `make build`.
7. Test in a disposable save using the checklist in `docs/patch-smoke-test.md`.
8. Only after successful testing, run:

   `python3 tools/compatibility.py mark-supported --version VERSION --tested`

The explicit `--tested` flag is intentional. The checker never assumes that unchanged hashes guarantee compatibility.

## Status meanings

- `development` — baseline recorded, but no release has been certified
- `supported` — rebuild and in-game smoke test completed for this exact patch
- `review_required` — installed version or monitored resources differ from the supported snapshot

