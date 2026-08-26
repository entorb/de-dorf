#!/bin/sh

# ensure we are in the root dir
cd "$(dirname "$0")/.."

# exit upon error
set -e

# cleanup
rm -f .DS_Store
rm -f -- */.DS_Store

# ruff
uv run --no-build ruff format
uv run --no-build ruff check

# build data.js from source tsv/csv
uv run --no-build python scripts/gen_data.py

echo copying
rsync -ruzv --delete web/ entorb@entorb.net:html/de-dorf/

echo DONE
