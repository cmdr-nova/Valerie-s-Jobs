#!/usr/bin/env python3
"""Upload a tagged build using the author Upload API; never log the token."""

import json
import os
import sys
import uuid
import zipfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

ROOT = Path(__file__).resolve().parents[1]
API = "https://sims4.curseforge.com/api"


class NoRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Do not forward author credentials to a redirected host.
        return None


def game_version_ids(versions, configured):
    """Use explicit dashboard IDs, or resolve the base-game tag unambiguously."""
    available = {int(version["id"]) for version in versions}
    if configured.strip():
        ids = [int(value.strip()) for value in configured.split(",")]
        if not ids or any(value not in available for value in ids):
            raise ValueError("Configured game-version IDs are absent from the Sims 4 API.")
        return list(dict.fromkeys(ids))
    matches = [
        int(version["id"])
        for version in versions
        if str(version.get("name", "")).strip().casefold() == "base game"
    ]
    if len(matches) != 1:
        raise ValueError(
            "Cannot resolve a unique Base Game tag. Set the repository variable "
            "CURSEFORGE_GAME_VERSION_IDS to the comma-separated dashboard IDs."
        )
    return matches


def multipart(metadata, filename, data, boundary):
    prefix = (
        "--{0}\r\nContent-Disposition: form-data; name=\"metadata\"\r\n"
        "Content-Type: application/json\r\n\r\n{1}\r\n"
        "--{0}\r\nContent-Disposition: form-data; name=\"file\"; "
        "filename=\"{2}\"\r\nContent-Type: application/zip\r\n\r\n"
    ).format(boundary, json.dumps(metadata), filename).encode("utf-8")
    return prefix + data + ("\r\n--{}--\r\n".format(boundary)).encode("ascii")


def main():
    token = os.environ.get("CURSEFORGE_API_TOKEN", "").strip()
    if not token:
        raise ValueError("Missing repository Actions secret VALERIE_CURSE.")
    tag = os.environ.get("GITHUB_REF_NAME", "")
    namespace = {}
    exec((ROOT / "src/valeries_jobs/version.py").read_text(), namespace)
    if tag != "v" + namespace["MOD_VERSION"]:
        raise ValueError("Release tag must match MOD_VERSION in src/valeries_jobs/version.py.")
    project = os.environ.get("CURSEFORGE_PROJECT_ID", "")
    if not project.isdecimal():
        raise ValueError("CURSEFORGE_PROJECT_ID must be numeric.")
    archive_path = ROOT / "release" / ("ValeriesJobs-{}.zip".format(tag))
    with zipfile.ZipFile(archive_path) as archive:
        if sorted(archive.namelist()) != ["ValeriesJobs.package", "ValeriesJobs.ts4script"]:
            raise ValueError("Release ZIP must contain only the two functional mod files.")
        if archive.testzip() is not None:
            raise ValueError("Release ZIP failed its integrity check.")
    opener = build_opener(NoRedirects())
    headers = {"X-Api-Token": token, "User-Agent": "ValeriesJobs-release"}
    with opener.open(Request(API + "/game/versions", headers=headers), timeout=60) as response:
        versions = json.load(response)
    ids = game_version_ids(versions, os.environ.get("CURSEFORGE_GAME_VERSION_IDS", ""))
    supported = json.loads((ROOT / "compatibility/supported.json").read_text())["game_version"]
    metadata = {
        "displayName": "Valerie's Jobs " + namespace["MOD_VERSION"],
        "releaseType": "beta",
        "gameVersions": ids,
        "changelogType": "markdown",
        "changelog": (
            "Tagged testing build **{tag}**. Tested game baseline: **{game}**.\n\n"
            "See the [tagged source and changes](https://github.com/cmdr-nova/"
            "Valerie-s-Jobs/releases/tag/{tag}).\n\n"
            "Extract both mod files into Mods/ValeriesJobs and remove older copies. "
            "Saving and reloading during an interview is not supported yet."
        ).format(tag=tag, game=supported),
    }
    boundary = "ValeriesJobs" + uuid.uuid4().hex
    body = multipart(metadata, archive_path.name, archive_path.read_bytes(), boundary)
    request = Request(
        API + "/projects/" + project + "/upload-file",
        data=body,
        headers=dict(headers, **{"Content-Type": "multipart/form-data; boundary=" + boundary}),
        method="POST",
    )
    # Do not retry a POST: a lost response could otherwise cause a duplicate upload.
    with opener.open(request, timeout=60) as response:
        result = json.load(response)
    file_id = result.get("id")
    if not isinstance(file_id, int):
        raise ValueError("Upload response did not contain a file ID; inspect the dashboard before retrying.")
    print("Uploaded CurseForge Beta file {} to project {} (subject to moderation).".format(file_id, project))


if __name__ == "__main__":
    try:
        main()
    except HTTPError as error:
        # Avoid printing server response bodies that could echo credentials.
        print("CurseForge API returned HTTP {}. Check token permissions and project approval; "
              "inspect the dashboard before retrying an upload.".format(error.code), file=sys.stderr)
        sys.exit(1)
    except URLError:
        print("CurseForge API connection failed; inspect the dashboard before retrying.", file=sys.stderr)
        sys.exit(1)
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
