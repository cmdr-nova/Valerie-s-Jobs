#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

docker run --rm \
  --user "$(id -u):$(id -g)" \
  --volume "${project_root}:/workspace" \
  --workdir /workspace \
  python:3.7.17-slim-bullseye \
  python tools/build_py37.py

node tools/build_package.js
node tools/verify_localization.js
