from django.db import models
from django.contrib.auth.models import User
import os
from django.utils import timezone
from utils.models import Country, AppointmentReason, ActivityType, TimeZone, City
from doctor.models import Doctor, DoctorAppointmentDate, DoctorAppointmentTime
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


def get_file_patch(instance, filename):
    return 'files/%s/%s' % (instance.patient.user.email, filename)


class Patient(models.Model):
    user = models.OneToOneField(User)
    country = models.ForeignKey(Country, null=True, blank=True, default=None)
    timezone = models.ForeignKey(TimeZone, null=True, blank=True, default=None)
    photo = models.FileField(upload_to='photo', blank=True, default=None)
    height_ft = models.SmallIntegerField(blank=True, default=0)
    height_in = models.SmallIntegerField(blank=True, default=0)
    weight = models.SmallIntegerField(blank=True, default=0)
    health_complete = models.BooleanField(blank=True, default=False)
    lifestyle_complete = models.BooleanField(blank=True, default=False)
    family_complete = models.BooleanField(blank=True, default=False)
    last_update = models.DateTimeField(auto_now=True)
    billing_complete = models.BooleanField(blank=True, default=False)

    @property
    def profile_complete(self):
        a = [self.health_complete, self.lifestyle_complete, self.family_complete]
        if sum(a) == len(a):
            return 100
        return int(100*float(sum(a))/len(a))

    def __str__(self):
        if self.user.first_name:
            return '%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return self.user.username


class PatientBilling(models.Model):
    VISA_CARD = 'visa'
    MASTERCARD_CARD = 'mastercard'
    AMERICAN_CARD = 'americanexpress'
    CARD_CHOICES = (
        (VISA_CARD, 'Visa'),
        (MASTERCARD_CARD, 'MasterCard'),
        (AMERICAN_CARD, 'American Express')
    )
    patient = models.OneToOneField(Patient)
    name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True, default=None)
    city = models.ForeignKey(City)
    country = models.ForeignKey(Country)
    zip = models.CharField(max_length=20)
    card_number = models.CharField(max_length=20)
    cvv_number = models.CharField(max_length=4)
    card_type = models.CharField(max_length=20, choices=CARD_CHOICES, default=VISA_CARD)
    hsa_card = models.BooleanField(default=False)
    expiration_date = models.DateField(default=timezone.now)


class PatientHistory(models.Model):
    patient = models.ForeignKey(Patient)
    record_date = models.DateField(auto_now_add=True)
    type = models.ForeignKey(ActivityType)
    provider = models.ForeignKey(Doctor, blank=True, null=True, default=None)

    class Meta:
        ordering = ('-record_date', )


class PatientFile(models.Model):
    PATIENT_FILE = 'patientrecord'
    TEST_FILE = 'testresult'
    FILE_CHOICES = (
        (PATIENT_FILE, 'Patient Record'),
        (TEST_FILE, 'Test Result'),
    )
    patient = models.ForeignKey(Patient)
    file = models.FileField(upload_to=get_file_patch)
    type = models.CharField(max_length=20, choices=FILE_CHOICES, default=PATIENT_FILE)


class PatientHealthHistory(models.Model):
    patient = models.OneToOneField(Patient)
    health_conditions = models.BooleanField()
    health_conditions_info = models.CharField(max_length=255, blank=True, null=True, default=None)
    medications = models.BooleanField()
    medications_info = models.CharField(max_length=255, blank=True, null=True, default=None)
    surgeries = models.BooleanField()
    surgeries_info = models.CharField(max_length=255, blank=True, null=True, default=None)


class PatientLifestyleQuestion(models.Model):
    question_string = models.CharField(max_length=100)

    def __str__(self):
        return self.question_string


class PatientLifestyle(models.Model):
    patient = models.ForeignKey(Patient)
    question = models.ForeignKey(PatientLifestyleQuestion)
    answer = models.BooleanField()


class PatientFamilyRelationship(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class PatientFamilyCondition(models.Model):
    name = models.CharField(max_length=50)
    patient = models.ForeignKey(Patient, null=True, blank=True, default=None)

    def __str__(self):
        return self.name


class PatientFamily(models.Model):
    patient = models.ForeignKey(Patient)
    condition = models.ForeignKey(PatientFamilyCondition)
    relationship = models.ForeignKey(PatientFamilyRelationship)


class PatientCase(models.Model):
    doctor = models.ForeignKey(Doctor)
    patient = models.ForeignKey(Patient, null=True, blank=True, default=None)
    reason = models.ForeignKey(AppointmentReason, null=True, blank=True, default=None)
    closed = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)


class Test(models.Model):
    case = models.ForeignKey(PatientCase)
    test = models.TextField()
    record_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.test


class Note(models.Model):
    case = models.ForeignKey(PatientCase)
    note = models.TextField()
    record_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.note


class PatientAppointment(models.Model):
    PHONE_APPOINTMENT = 'p'
    VIDEO_APPOINTMENT = 'v'
    APPOINTMENT_CHOICES = (
        (PHONE_APPOINTMENT, 'Phone'),
        (VIDEO_APPOINTMENT, 'Video')
    )
    STATUS_EDIT = 0
    STATUS_NEW = 1
    STATUS_DOCTOR_APPROVE = 2
    STATUS_DOCTOR_CANCEL = 3
    STATUS_DOCTOR_RESCHEDULE = 4
    STATUS_PATIENT_APPROVE = 5
    STATUS_PATIENT_CANCEL = 6
    STATUS_PATIENT_RESCHEDULE = 7
    STATUS_COMPLETE = 8
    STATUS_CHOICES = (
        (STATUS_EDIT, 'Uncomplited'),
        (STATUS_NEW, 'New'),
        (STATUS_DOCTOR_APPROVE, 'Doctor Confirm'),
        (STATUS_DOCTOR_CANCEL, 'Doctor Decline'),
        (STATUS_DOCTOR_RESCHEDULE, 'Doctor Reschedule'),
        (STATUS_PATIENT_APPROVE, 'Approved'),
        (STATUS_PATIENT_CANCEL, 'Canceled'),
        (STATUS_PATIENT_RESCHEDULE, 'Patient Edit'),
        (STATUS_COMPLETE, 'Completed')
    )
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(Doctor)
    case = models.ForeignKey(PatientCase, null=True, blank=True, default=None)
    appointment_date = models.ForeignKey(DoctorAppointmentDate)
    appointment_time = models.ForeignKey(DoctorAppointmentTime)
    reason = models.ForeignKey(AppointmentReason)
    comments = models.TextField()
    appointment_type = models.CharField(max_length=1, choices=APPOINTMENT_CHOICES, default=PHONE_APPOINTMENT)
    appointment_status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_EDIT)

    class Meta:
        ordering = ('appointment_date', )

    @property
    def status(self):
        return self.STATUS_CHOICES[self.appointment_status][1]


@receiver(user_signed_up)
def patient_create(sender, **kwargs):
    patient = Patient(user=kwargs.get('user'))
    patient.save()
    patient_history = PatientHistory(patient=patient, type=ActivityType.objects.get(name='signup'))
    patient_history.save()


@receiver(models.signals.post_delete, sender=Patient)
@receiver(models.signals.post_delete, sender=PatientFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.post_save, sender=PatientAppointment)
def auto_create_case_for_appointment(sender, instance, **kwargs):
    if instance.appointment_status == sender.STATUS_NEW:
        if PatientCase.objects.filter(doctor=instance.doctor, patient=instance.patient, closed=False).count() == 0:
            case = PatientCase(doctor=instance.doctor, patient=instance.patient,
                               created_date=timezone.now(), updated_date=timezone.now(), reason=instance.reason)
            case.save()
            instance.case = case
            instance.save()
