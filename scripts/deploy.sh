#!/bin/sh
set -e
cd "$(dirname "$0")/.."

# cleanup
rm -f .DS_Store
rm -f -- */.DS_Store

# spelling
sh scripts/run_spelling.sh

# ruff
uv run --no-build ruff format
uv run --no-build ruff check

# build data.js from source tsv/csv
uv run --no-build python scripts/gen_data.py

echo copying
rsync -ruzv --delete web/ entorb@entorb.net:html/de-dorf/

echo DONE
