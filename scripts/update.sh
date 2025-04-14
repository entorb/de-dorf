#!/bin/sh
cd $(dirname $0)/..

pyenv global 3.11
python -m pip install --upgrade pip
pip install --upgrade streamlit
pip freeze >requirements-all.txt
cat requirements-all.txt | grep streamlit >requirements.txt
