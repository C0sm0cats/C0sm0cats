#!/usr/bin/env bash
# Regenerate every static asset and the README.
# Usage (from anywhere): tools/build.sh
# Live data (badges, activity, contributions) is refreshed by .github/workflows/badges.yml;
# run it locally with: GH_TOKEN=$(gh auth token) python3 .github/scripts/{badges,live}.py
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/banner.py assets >/dev/null
python3 tools/headers.py assets/headers
python3 tools/ui.py assets
python3 tools/footer.py assets
python3 tools/readme.py
echo "Rebuilt assets and README.md"
