#!/bin/bash

rm ./doctor/migrations/0*
rm ./patient/migrations/0*
rm ./utils/migrations/0*
rm db.sqlite3

./manage.py makemigrations

./manage.py migrate

./manage.py loaddata fixtures.dev/user.json
./manage.py loaddata fixtures.dev/utils.json
./manage.py loaddata fixtures.dev/patient.json
./manage.py loaddata fixtures.dev/doctor.json
./manage.py loaddata fixtures.dev/account.json

#./manage.py createsuperuser --username admin --email admin@admin.loc