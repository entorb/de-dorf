#!/bin/sh
cd $(dirname $0)/..

python scripts/gen_requirements.py
echo copying
# config.toml -> config-prod.toml
uv run scripts/config_convert.py
rsync -uz .streamlit/config-prod.toml entorb@entorb.net:streamlit-de-dorf/.streamlit/config.toml
rsync -uz .streamlit/secrets.toml entorb@entorb.net:streamlit-de-dorf/.streamlit/secrets.toml
rsync -uz requirements.txt entorb@entorb.net:streamlit-de-dorf/
rsync -uz Weitere_Zahlen.md entorb@entorb.net:streamlit-de-dorf/
rsync -ruzv --no-links --delete --delete-excluded --exclude __pycache__ src/ entorb@entorb.net:streamlit-de-dorf/src/
rsync -ruzv --no-links --delete --delete-excluded data/* entorb@entorb.net:streamlit-de-dorf/data/

# echo installing packages
ssh entorb@entorb.net "pip3.11 install --user -r streamlit-de-dorf/requirements.txt > /dev/null"

echo restarting streamlit-de-dorf
ssh entorb@entorb.net "supervisorctl restart streamlit-de-dorf"
