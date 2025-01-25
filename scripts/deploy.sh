#!/bin/sh
cd $(dirname $0)/..

echo copying
# config.toml -> config-prod.toml
python3 scripts/config_convert.py
rsync -uz .streamlit/config-prod.toml entorb@entorb.net:streamlit-de-dorf/.streamlit/config.toml
rsync -uz requirements.txt entorb@entorb.net:streamlit-de-dorf/
rsync -ruzv --no-links --delete --delete-excluded --exclude __pycache__ src/ entorb@entorb.net:streamlit-de-dorf/src/
rsync -ruzv --no-links --delete --delete-excluded data/*.tsv entorb@entorb.net:streamlit-de-dorf/data/

echo installing packages
ssh entorb@entorb.net "pip3.11 install --user streamlit -r streamlit-de-dorf/requirements.txt > /dev/null"

echo restarting streamlit-de-dorf
ssh entorb@entorb.net "supervisorctl restart streamlit-de-dorf"