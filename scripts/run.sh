#!/bin/sh
cd $(dirname $0)/..

uv run streamlit run src/main.py
# for production better use
# uv run python -O -m streamlit run src/main.py
