from django.core.management.base import BaseCommand
from utils.objects_creation import create_objects as co

class Command(BaseCommand):
    help = 'Run script to populate db with test objects'

    def handle(self, *args, **options):
        doctor = co.create_doctor(co.DOCTORS[5])

        # doctor = co.get_doctor_by_email(co.DOCTORS[5]['email'])

        # co.add_doctor_specialty(doctor, specialty='hepatology', primary=True)

        # co.add_doctor_work_experience(doctor, 'Anesthesiology', 'Anesthesiologist', '2015-01-02', '2016-02-28')
        # co.add_doctor_work_experience(doctor, 'Surgery', 'Surgeon', '2016-03-01', '2016-03-30')

        # co.create_doctor_week_schedule(doctor, '2016-04-05')

        # patient = co.create_patient(co.PATIENTS[8])

        # patient = co.get_patient_by_email('patient1@gmail.com')

        # co.delete_all_payment_methods(patient)
        # co.add_payment_method(patient, 'visa', default=True)

        # case = co.create_patient_case(patient, doctor, 'Head pain', 'fairly often')

        # appointment = co.create_appointment(case, '2016-04-05 09:00:00')

        # appointment = co.complete_appointment(case, appointment)

        # appointment_notes = co.add_appointment_notes(appointment, co.NOTES[0])

        # co.send_message(case, subject='finger fracture', text='Some text of problem', from_doctor=True)

        # test_record = co.add_test_record(case, type='test', request_form=co.TEST_FILES[0]['file'])

        # test_record = co.add_test_record(case, type='record', request_form=co.TEST_FILES[0]['file'],
        #                 result_form=co.RECORD_FILES[0]['file'])

        # test_record = co.evaluate_test_record(test_record, conclusions=co.RECORD_FILES[0]['conclusions'])

        # case = co.close_case(case)
