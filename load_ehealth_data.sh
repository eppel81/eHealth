#!/bin/bash

#rm ./doctor/migrations/0*
#rm ./patient/migrations/0*
#rm ./utils/migrations/0*
#rm db.sqlite3

mkdir media
cp -r assets_media/* media

./manage.py makemigrations

./manage.py migrate

# ./manage.py loaddata fixtures.dev/ehealth/auth.json
# ./manage.py loaddata fixtures.dev/ehealth/account.json
./manage.py loaddata fixtures.dev/ehealth/utils.json
# ./manage.py loaddata fixtures.dev/ehealth/doctor.json
# ./manage.py loaddata fixtures.dev/ehealth/utils_appointmentschedule.json
# ./manage.py loaddata fixtures.dev/ehealth/doctor_doctorappointmenttime.json
# ./manage.py loaddata fixtures.dev/ehealth/patient.json
