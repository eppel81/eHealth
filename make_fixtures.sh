#!/bin/bash

mkdir fixtures.tmp
./manage.py dumpdata patient >./fixtures.tmp/patient.json
./manage.py dumpdata utils >./fixtures.tmp/utils.json
./manage.py dumpdata doctor >./fixtures.tmp/doctor.json
./manage.py dumpdata auth.user >./fixtures.tmp/user.json