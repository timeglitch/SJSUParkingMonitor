#!/bin/bash

source ./.venv/bin/activate

git pull
python3 main.py
git add *.json
git commit -m "AUTO: Update JSON files"
git push
