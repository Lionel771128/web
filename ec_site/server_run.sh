#!/bin/bash

#chmod u+x /ec_site/manage.py
python /web/manage.py makemigrations
python /web/manage.py migrate
python /web/create_test_data.py --host /var/run/postgresql/
uwsgi --ini /web/ec_site/uwsgi.ini

while :
do
	echo Keep running
	echo "Press CTRL+C to exit"
	sleep 100
done