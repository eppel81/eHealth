import os

from django.http import QueryDict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ehealth.settings')
import django
django.setup()

import datetime
import pytz
from django.contrib.auth.models import User
from doctor.models import Doctor, DoctorAppointmentTime
from allauth.account.models import EmailAddress
from utils.models import AppointmentSchedule
from django.test.client import RequestFactory
from doctor.views import TimeView
from utils.middleware import TimezoneMiddleware

DATE_NOW = datetime.datetime.utcnow().date()

DOCTORS = [
    {
        'user': 'emedicaltest1',
        'email': 'emedicaltest1@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Azcona',
        'last_name': 'Guerra',
        'city_id': 1,
        'country_id': 2,
        'gender': True,
        'timezone_id': 212,
        'photo': 'photo/DR._GUERRA_AZCONA_yscUB0V.jpg'
    },
]


def populate_doctor_appointment_time(doctor, app_schedule, datetime_from, amount_terms):
    doctor_tz = pytz.timezone(doctor.timezone.name)
    doctor_tz = pytz.timezone('Europe/Kiev')
    utc_tz = pytz.timezone('UTC')
    app_datetime = datetime_from
    time_shift = datetime.timedelta(minutes=15)
    for i in xrange(amount_terms):
        DoctorAppointmentTime.objects.create(
            doctor=doctor,
            start_time=app_datetime,
            duration=app_schedule.duration,
            schedule=app_schedule
        )
        app_datetime += time_shift

def populate_doctor_appointment_day_night(current_day, doctor):
    # morning
    date_from = datetime.datetime.combine(current_day.date, current_day.day_from)
    date_to = datetime.datetime.combine(current_day.date, current_day.day_to)
    amount_terms = (date_to - date_from).seconds/60/current_day.duration

    populate_doctor_appointment_time(doctor, current_day, date_from, amount_terms)

    # evening
    date_from = datetime.datetime.combine(current_day.date, current_day.night_from)
    date_to = datetime.datetime.combine(current_day.date, current_day.night_to)
    amount_terms = (date_to - date_from).seconds/60/current_day.duration

    populate_doctor_appointment_time(doctor, current_day, date_from, amount_terms)


def create_doctor_schedule(doctor, day=DATE_NOW.day, month=DATE_NOW.month, year=DATE_NOW.year)
    try:
        start_date = datetime.date(year, month, day)
    except ValueError as e:
        return e.message

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


def main():
    doctor_obj_list = []

    # Create superuser
    # User.objects.create_superuser('admin', 'admin@admin.loc', 'zaq123')

    # Create user for doctor
    # user1 = User.objects.create_user('emedicaltest1', 'emedicaltest1@mail2tor.com', 'zaq123')

    user1 = User.objects.last()

    # doctor1 = Doctor.objects.create(user=user1, city_id=1,
    #                                 country_id=2, gender=True, timezone_id=212,
    #                                 photo='photo/DR._GUERRA_AZCONA_yscUB0V.jpg')

    doctor1 = Doctor.objects.last()

    # user1.first_name = 'Azcona'
    # user1.last_name = 'Guerra'
    # user1.save()
    # EmailAddress.objects.create(user=user1, verified=True,
    #                             email='emedicaltest1@mail2tor.com')

    # Create AppointmentShedule ==================
    first_date = datetime.datetime.utcnow().date()
    # day1 = AppointmentSchedule.objects.create(doctor=doctor1, date=first_date,
    #                                           day_shift=True,
    #                                           day_from=doctor1.default_morning_start_time,
    #                                           day_to=doctor1.default_morning_end_time,
    #                                           night_shift=True,
    #                                           night_from=doctor1.default_afternoon_start_time,
    #                                           night_to=doctor1.default_afternoon_end_time)

    # current_day = AppointmentSchedule.objects.last()
    # populate_doctor_appointment_day_night(current_day, doctor1)
    # ============================================




if __name__ == '__main__':
    main()
