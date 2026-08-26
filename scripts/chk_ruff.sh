#!/bin/sh

# ensure we are in the root dir
cd "$(dirname "$0")/.."

uv run --no-build ruff format
uv run --no-build ruff check --fix
