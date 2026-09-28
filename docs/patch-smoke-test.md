# Patch smoke-test checklist

Use a disposable save and a minimal Mods folder.

- [ ] Game reaches the main menu without a script error.
- [ ] Test household loads normally.
- [ ] `vj.hello` reports the expected mod version.
- [ ] `vj.test_apply 5 5` produces a bounded percentage and an outcome.
- [ ] No new `lastException` file is produced.
- [ ] Standard career selection still opens.
- [ ] A full-time career can be joined through the current prototype path.
- [ ] A part-time job preserves shift selection.
- [ ] Actor preserves agency selection, auditions, and gigs.
- [ ] Noble bypasses Valerie's Jobs.
- [ ] Save, reload, travel, and household switching preserve pending applications.
- [ ] Failure, acceptance, ghost listing, cancellation, and cooldown paths work.
- [ ] Test with the supported minimum mod set.
- [ ] Test once with common compatibility targets such as MCCC.

Items for features not yet implemented should be marked not applicable, not silently treated as passing.

