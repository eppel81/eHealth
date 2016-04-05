import os
import logging
import datetime
import traceback


import braintree
from django.conf import settings
from django.http import QueryDict
from django.db import transaction
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from allauth.account.models import EmailAddress

from doctor.models import (Doctor, DoctorAppointmentTime, DoctorSpecialty,
                           DoctorWorkExperience)
from patient.models import (Patient, PatientCase, PatientAppointment,
                            AppointmentNote, TestFileRecord)
from patient.forms import WriteMessageForm
from doctor.views import TimeView
from utils.middleware import TimezoneMiddleware
from utils.models import Specialty

from test_data import PAYMENT_NONCES

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
BASE_PATH = os.path.abspath(os.path.join(FILE_PATH, '..', '..'))

DATE_NOW = datetime.datetime.utcnow().date()
logging.basicConfig(level=logging.ERROR, format='[%(asctime)s %(levelname)s]: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


def try_except_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            logger.info('starting %s', func.__name__)
            obj = func(*args, **kwargs)
            logger.info('finished %s', func.__name__)
        except Exception as e:
            traceback.print_exc()
            logger.error(e.message)
            return None
        return obj
    return wrapper


def get_model_instance(model, many=False, **kwargs):
    data = model.objects.filter(**kwargs)
    if not many:
        data = data.first()
    return data


def check_object(obj, klass):
    if isinstance(obj, (int, basestring)):
        obj = get_model_instance(klass, pk=obj)
    return obj


def create_super_user():
    """
    Create admin-user
    """
    user = User.objects.create_superuser('admin', 'admin@admin.loc', 'zaq123')
    return user


@transaction.atomic
@try_except_decorator
def create_doctor(doctor_dict):
    """
    :param doctor_dict: doctor's dictionary (in test_data.py)
    :return: Doctor instance
    """
    doctor = get_doctor_by_email(doctor_dict['email'])
    if doctor:
        return doctor

    with transaction.atomic():
        # Create user for doctor
        user = User.objects.create_user(
            doctor_dict['username'], doctor_dict['email'],
            doctor_dict['password'],
            first_name=doctor_dict['first_name'],
            last_name=doctor_dict['last_name']
        )
        doctor = Doctor.objects.create(
            user=user, city_id=doctor_dict['city_id'],
            country_id=doctor_dict['country_id'],
            gender=doctor_dict['gender'],
            timezone_id=doctor_dict['timezone_id'],
            photo=doctor_dict['photo']
        )
        EmailAddress.objects.create(
            user=user, verified=True, email=doctor_dict['email']
        )
    return doctor


def get_doctor_by_email(email):
    """
    Get doctor by his email

    :param email: email
    :return: Doctor instance
    """
    return Doctor.objects.filter(user__email=email).first()


@try_except_decorator
def create_doctor_week_schedule(doctor, start_date):
    """
    Create schedule for week that includes needed date

    :param doctor: Doctor instance
    :param start_date: day, for which week need to create schedule
    """

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')

    doctor = check_object(doctor, Doctor)

    dat = DoctorAppointmentTime.objects.filter(
        doctor=doctor, start_time__year=start_date.year,
        start_time__month=start_date.month, start_time__day=start_date.day
    )
    assert not dat.exists(), 'Schedule is already exists for this day'

    post_dict = {
        'first_day': '',
        'last_day': '',
        'form-TOTAL_FORMS': '7',
        'form-INITIAL_FORMS': '7',
        'form-MIN_NUM_FORMS': '7',
        'form-MAX_NUM_FORMS': '7',
    }
    post_querydict = QueryDict('', mutable=True)

    current_week_day = start_date.weekday()
    day_from = start_date - datetime.timedelta(days=current_week_day)
    day_to = start_date + datetime.timedelta(days=(6 - current_week_day))
    post_dict['first_day'] = day_from.strftime('%m/%d/%Y')
    post_dict['last_day'] = day_to.strftime('%m/%d/%Y')

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


def add_doctor_specialty(doctor, **kwargs):
    """
    Add specialty for doctor

    :param doctor: Doctor instance
    :param kwargs: represents specialty
                   may contain key "specialty" for text representation or
                   "specialty_id" by which specialty will be retrieved
    :return: DoctorSpecialty instance
    """

    doctor = check_object(doctor, Doctor)

    spec_name = kwargs.get('specialty')
    spec_id = kwargs.get('specialty_id')
    assert spec_name or spec_id, 'specialty_id or specialty must be defined'
    params = {'name__iexact': spec_name} if spec_name else {'pk': spec_id}
    spec = get_model_instance(Specialty, **params)
    assert spec, 'there is no specialty with given parameters: {}'.format(params)
    specialty = DoctorSpecialty.objects.get_or_create(
        doctor=doctor, specialty=spec,
        primary=kwargs.get('primary', 0)
    )
    return specialty


@try_except_decorator
def add_doctor_work_experience(doctor, care_facility, position, start_date, end_date):
    """
    :param doctor: Doctor instance
    :param care_facility: text
    :param position: text
    :param start_date: use format yyyy-mm-dd
    :param end_date: use format yyyy-mm-dd
    :return: DoctorWorkExperience instance
    """

    doctor = check_object(doctor, Doctor)

    obj, created = DoctorWorkExperience.objects.get_or_create(
        doctor=doctor, care_facility=care_facility, position=position,
        start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d'),
        end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d')
    )
    return obj


@try_except_decorator
@transaction.atomic
def create_patient(patient_dict):
    """
    Create patient

    :param patient_dict: patient's dictionary (in test_data.py)
    :return: Patient instance
    """

    patient = get_patient_by_email(patient_dict['email'])
    if patient:
        return patient

    # Create user patient
    with transaction.atomic():
        # Create user for doctor
        user = User.objects.create_user(
            patient_dict['username'], patient_dict['email'],
            patient_dict['password'], first_name=patient_dict['first_name'],
            last_name=patient_dict['last_name']
        )
        patient = Patient.objects.create(
            user=user, country_id=patient_dict['country_id'],
            timezone_id=patient_dict['timezone_id'], photo=patient_dict['photo']
        )
        EmailAddress.objects.create(
            user=user, verified=True, email=patient_dict['email']
        )
    return patient


@try_except_decorator
def get_patient_by_email(email):
    """
    Get patient by his email
    """
    return Patient.objects.filter(user__email=email).first()


def add_payment_method(patient, method, default=False):
    """
    Add payment method for patient

    :param patient: Patient instance
    :param method: may be 'amex' or 'visa' or 'paypal'
    :return: True if added, otherwise False
    """

    patient = check_object(patient, Patient)

    payment_dict = {
        'customer_id': str(patient.user.customeruser.customer),
        'payment_method_nonce': PAYMENT_NONCES[method],
        'options': {
            # 'fail_on_duplicate_payment_method': True,
            'make_default': default
        }
    }
    if method.lower() == 'amex':
        payment_dict['options']['fail_on_duplicate_payment_method'] = False

    res = braintree.PaymentMethod.create(payment_dict)
    if not res.is_success:
        logger.error(res.message)
        return False
    return True


def get_default_payment_or_first_method(patient):
    """
    Get default payment method

    :param patient:
    :return: payment method
    """
    patient = check_object(patient, Patient)

    payment_methods = braintree.Customer.find(
        str(patient.user.customeruser.customer)).payment_methods
    payment_method = payment_methods[0]
    for item in payment_methods:
        if item.default:
            payment_method = item
            break
    return payment_method


@try_except_decorator
def create_patient_case(patient, doctor, problem, description):
    """
    Create case for patient

    :param patient: Patient instance
    :param doctor: Doctor instance
    :param problem: text of problem
    :param description: description text
    :return: Case instance
    """
    patient = check_object(patient, Patient)
    doctor = check_object(doctor, Doctor)

    case, created = PatientCase.objects.get_or_create(
        doctor=doctor,
        patient=patient,
        problem=problem,
        description=description
    )
    return case


@try_except_decorator
def get_appointmenttime_obj(doctor, date_time):
    """
    :param doctor: Doctor instance
    :param date_time: use format "2016-04-01 09:00:00 (UTC timezone)
    :return: DoctorAppointmentTime instance
    """

    doctor = check_object(doctor, Doctor)

    dat = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    obj = DoctorAppointmentTime.objects.get(doctor=doctor, start_time=dat)
    return obj


@try_except_decorator
def create_appointment(case, date_time):
    """
    Create appointment instance

    :param case: Case instance
    :param date_time: use format "2016-04-01 09:00:00 (UTC timezone)
    :return: PatientAppointment instance
    """

    case = check_object(case, PatientCase)

    app_time = get_appointmenttime_obj(case.doctor, date_time)
    assert app_time, 'AppointmentTime instance doesn\'t exist'

    appointment = PatientAppointment.objects.get_or_create(
            case=case,
            appointment_time=app_time,
            appointment_type='v',
            appointment_status=2)[0]

    if app_time.free:
        if not appointment.deposit_paid:
            payment_method = get_default_payment_or_first_method(case.patient)
            payment = braintree.Transaction.sale({
                    'customer_id': str(case.patient.user.customeruser.customer),
                    'amount': str(case.doctor.deposit),
                    'merchant_account_id': settings.MERCHANT_ID,
                    'payment_method_token': payment_method.token,
                    'custom_fields': {
                        'type': 'Deposit',
                        'appointment_date': appointment.appointment_time.start_time,
                        'case': case.problem
                    },
                    'options': {
                        'submit_for_settlement': True,
                    }
            })
            if payment.is_success:
                appointment.deposit_paid = True
                appointment.deposit_transaction = payment.transaction.id
                appointment.save()

                app_time.free = False
                app_time.save()
            else:
                raise AssertionError(payment.message)

    return appointment


@try_except_decorator
def delete_all_payment_methods(patient):
    patient = check_object(patient, Patient)
    payment_methods = braintree.Customer.find(
        str(patient.user.customeruser.customer)).payment_methods
    for item in payment_methods:
        res = braintree.PaymentMethod.delete(item.token)
    return True


@try_except_decorator
def complete_appointment(case, appointment):
    """
    Complete appointment

    :param case: Case instance
    :param appointment: PatientAppointment instance
    :return: PatientAppointment instance
    """

    case = check_object(case, PatientCase)
    appointment = check_object(appointment, PatientAppointment)

    if not appointment.consult_paid:
        payment_method = get_default_payment_or_first_method(case.patient)
        payment = braintree.Transaction.sale({
            'customer_id': str(case.patient.user.customeruser.customer),
            'amount': str(case.doctor.consult_rate - case.doctor.deposit),
            'merchant_account_id': settings.MERCHANT_ID,
            'payment_method_token': payment_method.token,
            'custom_fields': {
                'type': 'Consult Rate',
                'appointment_date': appointment.appointment_time.start_time,
                'case': case.problem
            },
            'options': {
                'submit_for_settlement': True,
            }
        })
        if payment.is_success:
            appointment.consult_paid = True
            appointment.consult_transaction = payment.transaction.id
            appointment.appointment_status = PatientAppointment.STATUS_COMPLETE
            appointment.save()
        else:
            raise AssertionError(payment.message)
    return appointment


@try_except_decorator
def add_appointment_notes(appointment, note):
    """
    Add notes to appointment

    :param appointment: appointment instance
    :param note: dictionary (from test_data.py)
    :return: AppointmentNote instance
    """
    appointment = check_object(appointment, PatientAppointment)

    app_note_obj = AppointmentNote.objects.get_or_create(appointment=appointment)[0]
    app_note_obj.anamnesis = note['anamnesis']
    app_note_obj.exploration = note['exploration']
    app_note_obj.diagnosis = note['diagnosis']
    app_note_obj.additional_tests = note['additional_tests']
    app_note_obj.treatment = note['treatment']
    app_note_obj.public_notes = note['public_notes']
    app_note_obj.save()
    return app_note_obj


def check_file_path(file_path):
    """
    Check file existing
    :param file_path:  path to file
    """
    path = os.path.join(BASE_PATH, 'media', file_path)
    return os.path.isfile(path)


@try_except_decorator
def add_test_record(case, type='test', request_form='', result_form='',
                    description='test description'):
    """
    :param case: case instance
    :param type: may be 'test' or 'record'
    :param request_form: path to file 'test_files/file_name.ext' in media folder
    :param result_form: same as above
    :return: TestFileRecord object
    """

    case = check_object(case, PatientCase)

    if type.lower() == 'test':
        if not check_file_path(request_form):
            raise AssertionError('%s file doesn\'t exist' % request_form)
        params = dict(
            type=TestFileRecord.TEST, description=description,
            request_form=request_form
        )
    else:
        if not check_file_path(request_form):
            raise AssertionError('%s file doesn\'t exist' % request_form)
        if not check_file_path(result_form):
            raise AssertionError('%s file doesn\'t exist' % result_form)
        params = dict(
            type=TestFileRecord.RECORD, description=description,
            request_form=request_form, result_report_or_record=result_form
        )
    test_record_obj, created = TestFileRecord.objects.get_or_create(**params)
    test_record_obj.case.add(case)
    test_record_obj.save()
    return test_record_obj


# @try_except_decorator
def send_message(case, subject='', text='', from_doctor=False):
    """
    Send messages between doctor and patient

    :param case: case instance
    :param subject: text
    :param text: text of message
    :param from_doctor: if True then sender is DOCTOR.  Else sender is PATIENT
    :return: True
    """
    case = check_object(case, PatientCase)

    if from_doctor:
        sender = case.doctor.user
        recipient = case.patient.user.id
    else:
        sender = case.patient.user
        recipient = case.doctor.user.id

    form = WriteMessageForm(sender=sender,
                            data={'case': case.id, 'recipients': recipient,
                                  'subject': subject, 'body': text})
    if form.is_valid():
        form.save()
    return True


def evaluate_test_record(test_record, conclusions='conclusions'):
    """
    Add conclusions to test_record instance

    :param test_record: instance of test_record
    :param conclusions: text of conclusions
    :return: test_record instance
    """
    test_record = check_object(test_record, TestFileRecord)
    test_record.conclusions = conclusions
    test_record.save()
    return test_record


def close_case(case):
    """
    :param case: case instant
    :return: case
    """
    case = check_object(case, PatientCase)
    case.status = PatientCase.CLOSED
    case.save()
    return case

