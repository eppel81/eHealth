#!/bin/bash

rm ./doctor/migrations/0*
rm ./patient/migrations/0*
rm ./utils/migrations/0*
rm db.sqlite3

./manage.py makemigrations

./manage.py migrate

./manage.py loaddata fixtures.dev/*

#./manage.py createsuperuser --username admin --email admin@admin.loc