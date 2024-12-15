#!/bin/bash

cd ~/crypto_watch
source .venv/bin/activate
python generate_json.py
python generate_page.py

deactivate