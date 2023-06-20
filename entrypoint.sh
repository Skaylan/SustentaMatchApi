#!/usr/bin/env bash

python3 -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

python3 -m flask db init
python3 -m flask db upgrade
