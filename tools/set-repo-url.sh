#!/bin/sh
# Fill the <REPO-URL> placeholder in all docs once the repo exists.
# Usage: tools/set-repo-url.sh https://github.com/<owner>/<repo>
set -eu
[ $# -eq 1 ] || { echo "usage: $0 <repo-url>"; exit 1; }
url=${1%/}
cd "$(dirname "$0")/.."
files=$(grep -rl '<REPO-URL>' --include='*.md' . || true)
[ -n "$files" ] || { echo "No <REPO-URL> placeholders left."; exit 0; }
for f in $files; do
  sed -i '' "s|<REPO-URL>|$url|g" "$f"
  echo "updated $f"
done
python3 -I wien-sketch-to-prototype/docs/build_cheatsheet.py >/dev/null
echo "Done. Review with: git diff"
