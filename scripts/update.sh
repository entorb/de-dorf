#!/bin/sh
set -e
cd "$(dirname "$0")/.."

# update dependencies
uv sync --upgrade

# ruff
uv run ruff format
uv run ruff check --fix

# pre-commit
prek autoupdate --cooldown-days 7
prek run --all-files

echo DONE
