#!/bin/bash

git pull
/bin/python3 /home/timeglotch/Projects/SJSUParkingMonitor/main.py
git add *.json
git commit -m "AUTO: Update JSON files"
git push