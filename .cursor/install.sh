#!/usr/bin/env bash
# Idempotent dependency setup for the Task Tracker API.
# Safe to run repeatedly and on a fresh default image.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# The default base image ships Python 3.12 but not the venv/ensurepip module.
# Self-heal on a fresh image; a snapshot-backed build already has it and skips this.
if ! python3 -c "import ensurepip" >/dev/null 2>&1; then
  sudo apt-get update -qq
  sudo apt-get install -y -qq python3-venv
fi

cd "${repo_root}/backend"
python3 -m venv .venv
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt
