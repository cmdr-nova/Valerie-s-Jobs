# Valerie's Jobs

Getting a job is no longer just a menu click! Valerie's Jobs adds a hiring process to The Sims 4: your Sim attends an interview, their relevant skills influence the result, and getting hired isn't guaranteed.

Interviews last one or two in-game hours in a rabbit hole. Beginner Sims still have a fair chance—relevant skill levels around 2–3 already help.

## Features

- Interviews for supported full-time careers, including Actor, and part-time jobs.
- Pop-up dialogs announcing the interview and explaining its outcome.
- Automatic career assignment after a successful interview.
- Custom moodlets: Nailed the Interview (Confident), Back to the Listings (Sad), and Ghosted by the Job (Scared).
- Occasional fake job listings from employers who never intended to hire anyone. The rejection explains when the employer is to blame!
- Optional one-use interview skip cheat for new saves and storytelling.

The Noble career, freelance work, school, retirement, and unsupported custom careers bypass interviews.

## Skip an interview (0.3.5 and later)

Need a career immediately when starting a save? Select the Sim in Live Mode, open the cheat console (`Ctrl+Shift+C`), and enter:

```text
vj.skip_next_interview
```

Apply for a supported job normally. That Sim joins without an interview, skill roll, ghost listing, or interview-outcome moodlet. Normal career replacement confirmations and shift/agency selections are preserved.

The cheat affects only that Sim and is consumed only after a successful career join. Canceling a picker or confirmation retains it. Other Sims still need interviews, and the next application needs an interview again unless you re-enter the cheat.

To cancel an unused skip, enter:

```text
vj.skip_next_interview false
```

Skips do not stack or survive restarting the game. Finish or cancel an existing interview before arming one. Careers that already bypass interviews do not consume the skip. `testingcheats true` is not required.

## Spanish translation

**Spanish translation by [BRØDA TS4](https://www.patreon.com/BR0DA_TS4/posts/valeries-jobs-v0-171744476).** The complete neutral Spanish translation is included with permission in the main mod package, with the translator's internal creator credit preserved. Thank you for making the mod accessible to Spanish-speaking players!

All 106 Spanish strings remain included, with unchanged localization keys and placeholders. No separate Spanish download is required. Cheat-console feedback is English; gameplay dialogs and moodlets retain their localization.

If you previously installed BRØDA TS4's standalone translation package, remove that separate package when updating to avoid stale overrides. This does not apply to players who never installed a separate translation.

## Installation

1. Extract both `ValeriesJobs.package` and `ValeriesJobs.ts4script` into `Documents/Electronic Arts/The Sims 4/Mods/ValeriesJobs`.
2. Enable **Custom Content and Mods** and **Script Mods Allowed** in the game options.
3. Restart the game.

Keep the script no more than one folder beneath `Mods`, and remove older copies of the mod when updating.

## Current version and compatibility

Version **0.3.5** adds the optional interview skip cheat. The user tested immediate Detective career entry with the cheat, then confirmed a subsequent application required an interview, on The Sims 4 `1.129.39.1030`. All 72 automated tests pass. This focused test does not certify every feature on that patch; the previous compatibility baseline is `1.128.90.1030`. Spanish rendering still needs in-game verification.

Saving and reloading during an interview is not supported yet. Complete interviews before saving and exiting, and back up saves before testing. Other mods that change career joining may conflict.

## Source and bug reports

[Source code and development](https://github.com/cmdr-nova/Valerie-s-Jobs) · [Report a bug](https://github.com/cmdr-nova/Valerie-s-Jobs/issues)

Please include your game version, mod version, what happened, and any relevant exception report. Review reports for personal information before posting them publicly.

This is an unofficial fan-made mod and is not affiliated with or endorsed by Electronic Arts or Maxis.
