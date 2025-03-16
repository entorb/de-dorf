#!/bin/sh
cd $(dirname $0)/..

pyenv global 3.11
streamlit run src/app.py
# for production better use
# python -O -m streamlit run src/app.py
pyenv global 3.12
