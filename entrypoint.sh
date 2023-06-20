#!/usr/bin/env bash

python3 -m pip install --upgrade pip
python3 -m pip install --no-cache-dir -r requirements.txt

python3 -m flask db init
python3 -m flask db upgrade
