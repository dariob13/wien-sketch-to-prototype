#!/bin/sh
# Build upload-ready skill ZIPs for the Claude app (Customize > Skills > Upload a skill)
# and for organization provisioning. Output: dist/wien-revamp.zip
# The ZIP holds one folder named exactly like the skill, with SKILL.md inside.
set -eu
cd "$(dirname "$0")/.."
mkdir -p dist
rm -f dist/wien-revamp.zip
( cd wien-sketch-to-prototype/skills && zip -qr ../../dist/wien-revamp.zip wien-revamp -x '*/__pycache__/*' '*.pyc' '*/.DS_Store' )
unzip -l dist/wien-revamp.zip | tail -1
