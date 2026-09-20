#!/bin/sh

# ensure we are in the root dir
cd "$(dirname "$0")/.." || exit 1

# exit upon error
set -e

# update dependencies
uv sync --upgrade

# ruff
uv run ruff format
uv run ruff check --fix

# pre-commit
prek autoupdate
prek run --all-files

echo DONE
