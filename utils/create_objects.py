#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from django.http import QueryDict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ehealth.settings')
import django
django.setup()

import datetime
import pytz
from django.contrib.auth.models import User
from doctor.models import Doctor, DoctorAppointmentTime
from patient.models import Patient
from allauth.account.models import EmailAddress
from utils.models import AppointmentSchedule
from django.test.client import RequestFactory
from doctor.views import TimeView
from utils.middleware import TimezoneMiddleware

DATE_NOW = datetime.datetime.utcnow().date()

DOCTORS = [
    {
        'username': 'doctor1',
        'email': 'doctor1@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Azcona',
        'last_name': 'Guerra',
        'city_id': 1,
        'country_id': 2,
        'gender': True,
        'timezone_id': 212,
        'photo': 'photo/DR._GUERRA_AZCONA_pu7zytO.jpg',
    },
    {
        'username': 'doctor2',
        'email': 'doctor2@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Castell',
        'last_name': 'Gomez',
        'city_id': 1,
        'country_id': 2,
        'gender': True,
        'timezone_id': 212,
        'photo': 'photo/DR._CASTELL_GÓMEZ_37HKDDc.jpg',
    },
    {
        'username': 'doctor3',
        'email': 'doctor3@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Federico',
        'last_name': 'Castillo',
        'city_id': 1,
        'country_id': 2,
        'gender': True,
        'timezone_id': 212,
        'photo': 'photo/DR._DEL_CASTILLO_DÍEZ.jpg',
    },
    {
        'username': 'doctor4',
        'email': 'doctor4@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Freire',
        'last_name': 'Torres',
        'city_id': 1,
        'country_id': 2,
        'gender': True,
        'timezone_id': 212,
        'photo': 'photo/DR._FREIRE_TORRES.jpg',
    },
    {
        'username': 'doctor5',
        'email': 'doctor5@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Mora',
        'last_name': 'Sanz',
        'city_id': 1,
        'country_id': 2,
        'gender': True,
        'timezone_id': 212,
        'photo': 'photo/DR._MORA_SANZ.jpg',
    },
    {
        'username': 'doctor6',
        'email': 'doctor6@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Villar',
        'last_name': 'Riu',
        'city_id': 1,
        'country_id': 2,
        'gender': False,
        'timezone_id': 212,
        'photo': 'photo/DRA._VILLAR_RIU.jpg',
    }
]

PATIENTS = [
    {
        'username': 'patient1',
        'email': 'patient1@gmail.com',
        'password': 'zaq123',
        'first_name': 'Meike',
        'last_name': 'Ritter',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient1.jpg'
    },
    {
        'username': 'patient2',
        'email': 'patient2@gmail.com',
        'password': 'zaq123',
        'first_name': 'Ferdinand',
        'last_name': 'Lang',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient2.jpg'
    },
    {
        'username': 'patient3',
        'email': 'patient3@gmail.com',
        'password': 'zaq123',
        'first_name': 'Luise',
        'last_name': 'Breuer',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient3.jpg'
    },
]

def create_super_user():
    """
    Create admin-user
    """
    user = User.objects.create_superuser('admin', 'admin@admin.loc', 'zaq123')
    return user


# def create_doctor(username, email, password, country_id=2, city_id=1,
#                   timezone_id=212, gender=1):
def create_doctor(doctor_dict):
    # Create user for doctor
    try:
        user = User.objects.create_user(doctor_dict['username'],
                                        doctor_dict['email'],
                                        doctor_dict['password'],
                                        first_name=doctor_dict['first_name'],
                                        last_name=doctor_dict['last_name']
                                        )
        doctor = Doctor.objects.create(user=user, city_id=doctor_dict['city_id'],
                                       country_id=doctor_dict['country_id'],
                                       gender=doctor_dict['gender'],
                                       timezone_id=doctor_dict['timezone_id'],
                                       photo=doctor_dict['photo']
                                       )
        EmailAddress.objects.create(user=user, verified=True,
                                    email=doctor_dict['email'])
    except Exception as e:
        return None
    return doctor


def get_doctor_by_email(email):
    """
    Get doctor by his email
    """
    return Doctor.objects.filter(user__email=email).first()


def create_doctor_week_schedule(doctor, day=DATE_NOW.day, month=DATE_NOW.month, year=DATE_NOW.year):
    """
    Create schedule for week
    """
    try:
        start_date = datetime.date(year, month, day)
    except ValueError as e:
        return None

    post_dict = {
        'first_day': '',
        'last_day': '',
        'form-TOTAL_FORMS': '7',
        'form-INITIAL_FORMS': '7',
        'form-MIN_NUM_FORMS': '7',
        'form-MAX_NUM_FORMS': '7',
    }
    post_querydict = QueryDict('', mutable=True)

    current_week_day = datetime.datetime.weekday(start_date)
    post_dict['first_day'] = (start_date - datetime.timedelta(days=current_week_day))\
        .strftime('%m/%d/%Y')
    post_dict['last_day'] = \
        (start_date + datetime.timedelta(days=(6 - current_week_day))).strftime('%m/%d/%Y')

    form_day = start_date - datetime.timedelta(days=current_week_day)
    form_day_delta = datetime.timedelta(days=1)

    for day in xrange(7):
        if day >= current_week_day:
            post_dict.update({
                'form-%d-weekday' % day: 'on',
                'form-%d-day_shift' % day: 'on',
                'form-%d-day_from' % day: str(doctor.default_morning_start_time),
                'form-%d-day_to' % day: str(doctor.default_morning_end_time),
                'form-%d-night_shift' % day: 'on',
                'form-%d-night_from' % day: str(doctor.default_afternoon_start_time),
                'form-%d-night_to' % day: str(doctor.default_afternoon_end_time),
                'form-%d-date' % day: form_day.strftime('%Y-%m-%d'),
                'form-%d-doctor' % day: str(doctor.id),
                'form-%d-duration' % day: '15',
            })
        else:
            post_dict.update({
                'form-%d-weekday' % day: '',
                'form-%d-day_shift' % day: '',
                'form-%d-day_from' % day: '',
                'form-%d-day_to' % day: '',
                'form-%d-night_shift' % day: '',
                'form-%d-night_from' % day: '',
                'form-%d-night_to' % day: '',
                'form-%d-date' % day: form_day.strftime('%Y-%m-%d'),
                'form-%d-doctor' % day: str(doctor.id),
                'form-%d-duration' % day: '15'
            })
        post_dict['form-%s-id' % day] = '0'
        form_day += form_day_delta

    post_querydict.update(post_dict)

    tmp_factory = RequestFactory()
    req = tmp_factory.post('/en/doctor/schedule/time/')
    req.user = doctor.user
    mdware = TimezoneMiddleware()
    mdware.process_request(req)
    req.POST = post_querydict
    resp = TimeView.as_view()(req)
    return True


def create_patient(username, email, password, photo=None, country_id=2,
                   timezone_id=180):
    # Create user patient
    try:
        user = User.objects.create_user(username, email, password)
        patient = Patient.objects.create(user=user, country_id=country_id,
                                         timezone_id=timezone_id, photo=photo)
        EmailAddress.objects.create(user=user, verified=True,
                                    email=email)
    except Exception as e:
        return None
    return patient


def get_patient_by_email(email):
    """
    Get doctor by his email
    """
    return Patient.objects.filter(user__email=email).first()


def complete_patient_history(patient):
    pass

def main():
    user = create_doctor(DOCTORS[0])
    # doctor = get_doctor_by_email('dem@gmail.com')
    # add_doctor_profile(doctor, 'Dmitry', 'Gogenko', 'photo/DR._GUERRA_AZCONA_yscUB0V.jpg')
    # create_doctor_week_schedule(doctor, day=1, month=4)


    #patient
    # patient = create_patient('emedicaltestPatient1', 'emedicaltestPatient1@gmail.com', 'zaq123', photo='photo/patient1.jpg')

    print 're'

if __name__ == '__main__':
    main()
