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

### Failed `0.2.0-dev` test

The game produced two tuning-load exceptions (`'str' object has no attribute 'factory'`) for the interview interactions, followed by a transition exception (`'tuple' object has no attribute 'get'`). The queued interview consequently canceled instead of entering the rabbit hole. The causes were inherited animation-factory and posture-constraint structures that were invalid in the custom tuning context.

Version `0.2.1-dev` removes both structures and follows EA's simpler time-based rabbit-hole interaction schema. Regression tests now reject either structure if it is reintroduced.

### Failed `0.2.1-dev` test and corrected diagnosis

The same exception recurred. Bytecode inspection showed line 2339 accesses `liability.factory`: a tuning-defined basic liability had loaded as a string. That exception prevented the same callback from converting `_constraints` into its runtime mapping, which caused the later tuple error. Version `0.2.2-dev` therefore removes all tuning-defined liabilities and uses a small custom Python interaction to apply only EA's `HideSimLiability` after the Sim routes to the lot's `Spawn_Arrival` marker.

### Passed `0.2.2-dev` test and `0.2.3-dev` arrival-dialog revision

The user confirmed that `0.2.2-dev` routed the Sim to the rabbit hole, hid the Sim, completed the interview, and displayed the modal result correctly. Version `0.2.3-dev` moves the interview-start dialog into a one-shot callback fired from the custom interaction's run phase, after routing succeeds. If the managed rabbit hole is unavailable and the timed fallback is used, the dialog still appears immediately because there is no physical arrival to await.

## 2026-09-28 — Weather-interruption fix ready for test

- Mod version: `0.2.4-dev`
- A main-save test during snowfall showed the interview being canceled after it began.
- The custom interaction now uses the same critical push/high run priority pattern as EA's Actor audition rabbit hole, preventing weather autonomy from displacing it.
- Managed rabbit holes no longer start their duration during routing. A scripted alarm begins at the arrival callback and closes the rabbit hole normally after exactly one or two in-game hours.
- Deliberate interaction cancellation still follows the existing canceled-application path.
- In-game result: pending

### Failed `0.2.4-dev` test and constructor correction

The first test build failed while creating the interview interaction because the programmatically added `CriticalPriorityLiability` was not given its required interaction argument. The managed rabbit hole therefore fell back to a timer, displayed the start dialog immediately, and left the Sim at the computer. Version `0.2.5-dev` passes the interaction instance to the liability constructor and adds a regression assertion for that argument. The no-time-limit rabbit-hole tuning loaded without an exception.

### Canceled `0.2.5-dev` test and running-priority correction

The interaction instantiated without a new exception and reached the rabbit-hole exit, but EA canceled it immediately after the arrival popup and the Sim returned indoors. The priority liability was still dropping from Critical while queued to High while running, allowing the snowy-weather indoor reaction to displace it. Version `0.2.6-dev` keeps the interaction at Critical priority while running, following EA tuning used for protected career routing and other interactions that must not be displaced.

### Canceled `0.2.6-dev` test and displacement guard

The interview was still displaced immediately after arrival, this time by the autonomous vampire social “Spread the Gloom.” Inspection of EA's interaction code showed that super-interaction displacement uses `displace()` and may permit equal Critical-priority interactions to replace each other. Version `0.2.7-dev` rejects displacement on the custom interview interaction. Natural completion, scripted rabbit-hole removal, reset handling, and explicit player cancellation do not use this displacement path.

### Partially completed `0.2.7-dev` test and queue-exit guard

The interview reached almost 50% completion before it was canceled and followed by autonomous TV watching. This confirmed that routing, hiding, and the arrival-started timer were functioning, but another queue cancellation path remained. EA's super-interaction code can call `_cancel_eventually()` directly for priority, social, queue, and compatibility replacement without invoking `displace()`. Version `0.2.8-dev` blocks only those autonomy/queue replacement reasons while continuing to allow natural and conditional completion, explicit player cancellation, resets, failures, and cleanup.

### Passed `0.2.8-dev` lifecycle test and hidden-autonomy correction

The full interview completed and displayed a normal rejection result without cancellation. When the rabbit hole ended, however, the Sim was already indoors, seated, and talking to another Sim, showing that autonomy had continued moving and socializing the hidden Sim. Version `0.2.9-dev` restores EA's native off-screen posture (`23832`) and looping rabbit-hole animation (`23834`) to hold the Sim in the interview state. These fields were removed during the original tuning investigation, but the actual tuning-load fault was subsequently proven to be malformed basic liabilities.

### Completed `0.2.9-dev` test with stale hidden state

The interview completed, but the Sim's portrait remained faded afterward. Both the restored looping interaction and the scripted arrival alarm were ending at the same 60/120-minute boundary, creating a race between interaction cleanup and managed rabbit-hole removal. Version `0.2.10-dev` removes the interaction's duplicate time condition. The arrival-started alarm is now the sole completion owner and removes the managed rabbit hole naturally, allowing the loop and `HideSimLiability` to release through one path.

### Passed `0.2.10-dev` cleanup test and progress-bar restoration

The full interview completed, the Sim returned normally, and the portrait no longer remained faded. Removing the interaction's time condition also removed the queue progress bar because that condition supplies the game's progress display. Version `0.2.11-dev` restores a display/safety condition at 61 or 121 minutes and explicitly uses it for the progress bar. The arrival-started alarm remains the authoritative completion path at exactly 60 or 120 minutes, so normal completion occurs before the display condition and does not recreate the cleanup race.

## 2026-09-28 — Outcome moodlets ready for test

- Mod version: `0.3.0-dev`
- Accepted interviews grant **Nailed the Interview**, a +1 Confident moodlet lasting four in-game hours.
- Ordinary rejections grant **Back to the Listings**, a +1 Sad moodlet lasting two in-game hours.
- Ghost listings grant **Ghosted by the Job**, a +1 Scared moodlet lasting three in-game hours, complete with the base-game ghost icon.
- All three use base-game mood types, icons, and audio stings; a missing moodlet safely logs the problem without interrupting career assignment or the result dialog.
- In-game result: passed after the `0.3.2-dev` UI-data correction below

### Failed `0.3.1-dev` moodlet UI test and SimData correction

An ordinary rejection changed the Sim's emotional state to Sad, but no moodlet appeared to explain the change. The same session generated `lastUIException.txt` errors in `BuffInfo.MoodKey`, confirming that the client UI could not resolve the custom buff's static display data. The XML tuning was sufficient for the simulation to apply the emotion, but custom visible buffs also require matching Buff SimData resources. Version `0.3.2-dev` adds those records for all three outcomes, including their names, descriptions, icons, mood types, weights, and current UI schema.

### Passed `0.3.2-dev` acceptance and visible-moodlet test

The user confirmed that the Sim completed the interview, received the job, and displayed the custom **Nailed the Interview** Confident moodlet. This certifies the accepted outcome's career assignment, mood contribution, visible UI entry, and custom text path. The Sad rejection and Scared ghost-listing variants use the same tested SimData schema and are covered by regression tests, though their corrected UI records have not yet been independently exercised in game. Host result: 32 unit tests passed.
