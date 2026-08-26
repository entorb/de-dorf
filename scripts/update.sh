#!/bin/sh

# ensure we are in the root dir
cd "$(dirname "$0")/.."

# exit upon error
set -e

# update dependencies
uv --no-build sync --upgrade

# ruff
uv --no-build run ruff format
uv --no-build run ruff check --fix

# pre-commit
prek autoupdate
prek run --all-files

echo DONE
