# Tagged releases

The GitHub Actions workflow builds and tests a pushed `v*` tag, packages the two functional mod files, publishes the GitHub prerelease, and uploads the same ZIP as a CurseForge Beta to project **1727866**.

## Configuration

- Repository Actions secret: **VALERIE_CURSE**, containing the author Upload API token. Its value belongs only in the secret store, never in source, release archives, or command output.
- Optional repository Actions variable: **CURSEFORGE_GAME_VERSION_IDS**, a comma-separated list of numeric Sims 4 game-version/category IDs from the dashboard/API. By default, the uploader looks up the unique **Base Game** entry in the authenticated Sims 4 version list. It fails with a clear instruction if that entry cannot be resolved, rather than guessing or marking expansion packs as required.
- Upload endpoint: `https://sims4.curseforge.com/api/projects/1727866/upload-file`.

The uploader validates tag/version consistency, ZIP contents, and game-version IDs before sending the file. API credentials go in a request header; redirects cannot forward credentials. Upload POSTs are not retried automatically because an uncertain response could otherwise duplicate a file.

## Next release

1. Make and test the mod changes; update `MOD_VERSION` in `src/valeries_jobs/version.py` and the compatibility baseline only if a new game patch has actually been validated.
2. Commit and push the changes.
3. Create and push a matching tag, for example `v0.3.3-dev` for `MOD_VERSION = "0.3.3-dev"`.
4. Inspect the Actions run and the CurseForge dashboard. Uploads still undergo moderation.

This configuration does not upload the existing pending `0.3.2-dev` build or retag it. The next tag must contain this workflow update. Beta uploads do not promote the mod to a stable release; change the workflow deliberately when a stable version is ready.

If the CurseForge step fails after GitHub publication, the GitHub release still exists. Inspect the CurseForge dashboard before resubmitting. Rerunning the entire workflow currently encounters the existing GitHub release, so recovery should target the failed CurseForge step without creating another GitHub release.

Validation covers local packaging and metadata logic; actual token validity, authenticated version lookup, and upload success are verified by the first Actions upload. The token was not retrieved from the user's Obsidian note or exposed during setup.

Reference: [CurseForge author Upload API](https://support.curseforge.com/support/solutions/articles/9000197321-curseforge-api).
