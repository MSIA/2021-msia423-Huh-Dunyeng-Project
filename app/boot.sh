#!/usr/bin/env bash

python3 run.py create_db
python3 run.py s3
python3 app.py