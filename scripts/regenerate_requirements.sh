#!/usr/bin/env bash

if [[ -d tmp_venv ]]; then
    rm -rf tmp_venv
fi

python3.7 -m venv tmp_venv

source tmp_venv/bin/activate
pip install -r requirements-base.txt
pip freeze > requirements.txt
deactivate
rm -rf tmp_venv
