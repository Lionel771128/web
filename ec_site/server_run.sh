#!/bin/bash
chmod u+x /web/manage.py
python /web/manage.py migrate
python /web/manage.py runserver 0.0.0.0:8000