#!/bin/sh
cd $(dirname $0)/..

uv remove numpy pandas pyarrow streamlit
uv remove --dev ruff pre-commit pytest pytest-cov tomli-w watchdog

uv lock --upgrade
uv sync --upgrade

uv add numpy==2.2.3 pandas==2.2.3 pyarrow==20.0.0 streamlit
uv add --dev ruff pre-commit pytest pytest-cov tomli-w watchdog

uv lock --upgrade
uv sync --upgrade
python scripts/gen_requirements.py
