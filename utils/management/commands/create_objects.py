from django.core.management.base import BaseCommand
from utils.objects_creation import create_objects as co
from utils.objects_creation.test_data import DOCTORS, PATIENTS, NOTES, TEST_FILES, RECORD_FILES


class Command(BaseCommand):
    help = 'This code is a sample script to create objects. If necessary, you can change it.'

    def handle(self, *args, **options):
        doctor = co.create_doctor(DOCTORS[5])

        co.add_doctor_specialty(doctor, specialty='hepatology', primary=True)

        co.add_doctor_work_experience(doctor, 'Anesthesiology', 'Anesthesiologist', '2015-01-02', '2016-02-28')
        co.add_doctor_work_experience(doctor, 'Surgery', 'Surgeon', '2016-03-01', '2016-03-30')

        co.create_doctor_week_schedule(doctor, '2016-04-05')

        patient = co.create_patient(PATIENTS[5])
        # co.get_patient_by_email(PATIENTS[5]['email'])

        # co.delete_all_payment_methods(patient)
        co.add_payment_method(patient, 'amex', default=True)

        case = co.create_patient_case(patient, doctor, 'Head pain', 'fairly often')

        # create appointment instance and make deposit_transaction.
        appointment = co.create_appointment(case, '2016-04-05 09:00:00')

        # create appointment instance and make  consult_transaction.
        # (transaction limit - 30 seconds)
        co.complete_appointment(case, appointment)

        appointment_notes = co.add_appointment_notes(appointment, NOTES[0])

        co.send_message(case, subject='finger fracture', text='Some text of problem', from_doctor=True)

        test_record = co.add_test_record(case, type='test', request_form=TEST_FILES[0]['file'])

        # test_record = co.add_test_record(case, type='record', request_form=TEST_FILES[0]['file'],
        #                 result_form=RECORD_FILES[0]['file'])

        co.evaluate_test_record(test_record, conclusions=RECORD_FILES[0]['conclusions'])

        case = co.close_case(case)
