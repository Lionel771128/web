#!/bin/bash

#chmod u+x /ec_site/manage.py
python /web/ec_site/manage.py makemigrations
python /web/ec_site/manage.py migrate
#python /web/manage.py runserver 0.0.0.0:8000
uwsgi --ini /web/ec_site/uwsgi.ini

while :
do
	echo Keep running
	echo "Press CTRL+C to exit"
	sleep 100
done