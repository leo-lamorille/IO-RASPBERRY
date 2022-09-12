#!/bin/bash
pip install -r requirements.txt
python dashboard/manage.py runserver 0:8000
tail -f /dev/null