import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from utils.models import Country, ActivityType, TimeZone, City
from doctor.models import Doctor, DoctorAppointmentTime


def get_file_patch(instance, filename):
    if isinstance(instance, TestFileRecord):
        return 'files/%s/%s' % (
            instance.case.first().patient.user.email, filename)
    if isinstance(instance, AdditionalFile):
        return 'files/%s/%s' % (
            instance.test_file_record.case.first().patient.user.email, filename)


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

    @property
    def profile_complete(self):
        a = [self.health_complete, self.lifestyle_complete,
             self.family_complete]
        if sum(a) == len(a):
            return 100
        return int(100 * float(sum(a)) / len(a))

    def __str__(self):
        if self.user.first_name:
            return '%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return self.user.username

    def __unicode__(self):
        return self.__str__()


class PatientHistory(models.Model):
    patient = models.ForeignKey(Patient)
    record_date = models.DateField(auto_now_add=True)
    type = models.ForeignKey(ActivityType)
    provider = models.ForeignKey(Doctor, blank=True, null=True, default=None)

    class Meta:
        ordering = ('-record_date',)


class PatientHealthHistory(models.Model):
    patient = models.OneToOneField(Patient)
    health_conditions = models.BooleanField()
    health_conditions_info = models.CharField(max_length=255, blank=True,
                                              null=True, default=None)
    medications = models.BooleanField()
    medications_info = models.CharField(max_length=255, blank=True, null=True,
                                        default=None)
    surgeries = models.BooleanField()
    surgeries_info = models.CharField(max_length=255, blank=True, null=True,
                                      default=None)


class PatientLifestyleQuestion(models.Model):
    question_string = models.CharField(max_length=100)

    def __str__(self):
        return self.question_string

    def __unicode__(self):
        return self.__str__()


class PatientLifestyle(models.Model):
    patient = models.ForeignKey(Patient)
    question = models.ForeignKey(PatientLifestyleQuestion)
    answer = models.BooleanField()


class PatientFamilyRelationship(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class PatientFamilyCondition(models.Model):
    name = models.CharField(max_length=50)
    patient = models.ForeignKey(Patient, null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.__str__()


class PatientFamily(models.Model):
    patient = models.ForeignKey(Patient)
    condition = models.ForeignKey(PatientFamilyCondition)
    relationship = models.ForeignKey(PatientFamilyRelationship)


class PatientCase(models.Model):
    CLOSED = 0
    OPEN = 1
    STATUS_CHOICES = (
        (CLOSED, _('Closed')),
        (OPEN, _('Open'))
    )
    doctor = models.ForeignKey(Doctor)
    patient = models.ForeignKey(Patient, null=True, blank=True, default=None)
    problem = models.CharField(max_length=255)
    is_second_opinion = models.BooleanField(default=False)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=OPEN)
    description = models.TextField()
    test_file_records = models.ManyToManyField("TestFileRecord")
    opentok_session = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.problem

    def __unicode__(self):
        return self.__str__()


class TestFileRecord(models.Model):
    TEST = 0
    RECORD = 1
    STATUS_CHOICES = (
        (TEST, 'Test'),
        (RECORD, 'Record')
    )

    type = models.SmallIntegerField(choices=STATUS_CHOICES, default=TEST)
    description = models.CharField(max_length=254)
    request_form = models.FileField(blank=True, upload_to=get_file_patch)
    result_report_or_record = models.FileField(blank=True,
                                               upload_to=get_file_patch)
    case = models.ManyToManyField(PatientCase)
    conclusions = models.TextField(null=True, blank=True, default=None)
    requested_by = models.CharField(max_length=50, null=True, blank=True,
                                    default=None)
    completed_by = models.CharField(max_length=50, null=True, blank=True,
                                    default=None)

    def request_formname(self):
        return os.path.basename(self.request_form.name)

    def result_report_or_recordname(self):
        return os.path.basename(self.result_report_or_record.name)


class AdditionalFile(models.Model):
    file = models.FileField(blank=True, upload_to=get_file_patch)
    test_file_record = models.ForeignKey(TestFileRecord)

    def filename(self):
        return os.path.basename(self.file.name)


class AppointmentNote(models.Model):
    appointment = models.OneToOneField('PatientAppointment')
    anamnesis = models.TextField(null=True, blank=True, default=None)
    exploration = models.TextField(null=True, blank=True, default=None)
    diagnosis = models.TextField(null=True, blank=True, default=None)
    additional_tests = models.TextField(null=True, blank=True, default=None)
    treatment = models.TextField(null=True, blank=True, default=None)
    public_notes = models.TextField(null=True, blank=True, default=None)


class PatientAppointment(models.Model):
    PHONE_APPOINTMENT = 'p'
    VIDEO_APPOINTMENT = 'v'
    APPOINTMENT_CHOICES = (
        (PHONE_APPOINTMENT, _('Phone')),
        (VIDEO_APPOINTMENT, _('Video'))
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
        (STATUS_EDIT, _('Incomplete')),
        (STATUS_NEW, _('New')),
        (STATUS_DOCTOR_APPROVE, _('Doctor Confirm')),
        (STATUS_DOCTOR_CANCEL, _('Doctor Decline')),
        (STATUS_DOCTOR_RESCHEDULE, _('Doctor Reschedule')),
        (STATUS_PATIENT_APPROVE, _('Approved')),
        (STATUS_PATIENT_CANCEL, _('Canceled')),
        (STATUS_PATIENT_RESCHEDULE, _('Patient Reschedule')),
        (STATUS_COMPLETE, _('Completed'))
    )

    case = models.ForeignKey(PatientCase)
    appointment_time = models.ForeignKey(DoctorAppointmentTime)
    appointment_type = models.CharField(max_length=1,
                                        choices=APPOINTMENT_CHOICES,
                                        default=PHONE_APPOINTMENT)
    appointment_status = models.SmallIntegerField(choices=STATUS_CHOICES,
                                                  default=STATUS_EDIT)
    deposit_paid = models.BooleanField(default=False)
    consult_paid = models.BooleanField(default=False)
    deposit_transaction = models.CharField(max_length=255, blank=True, null=True)
    consult_transaction = models.CharField(max_length=255, blank=True, null=True)
    opentok_token = models.CharField(max_length=2000, null=True, blank=True)


    class Meta:
        ordering = ('appointment_time',)

    @property
    def status(self):
        return self.STATUS_CHOICES[self.appointment_status][1]


@receiver(user_signed_up)
def patient_create(sender, **kwargs):
    patient = Patient(user=kwargs.get('user'))
    patient.save()
    patient_history = PatientHistory(patient=patient,
                                     type=ActivityType.objects.get(
                                         name='signup'))
    patient_history.save()


@receiver(models.signals.post_delete, sender=TestFileRecord)
@receiver(models.signals.post_delete, sender=AdditionalFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if isinstance(instance, TestFileRecord):
        if instance.request_form:
            if os.path.isfile(instance.request_form.path):
                os.remove(instance.request_form.path)
        if instance.result_report_or_record:
            if os.path.isfile(instance.result_report_or_record.path):
                os.remove(instance.result_report_or_record.path)
    elif isinstance(instance, AdditionalFile):
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

