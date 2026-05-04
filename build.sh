#!/usr/bin/env bash
cd hamro_tweet
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
