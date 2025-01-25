#!/bin/sh
cd $(dirname $0)/..

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip freeze >requirements-all.txt
