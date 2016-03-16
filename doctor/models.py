import os
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from utils.models import (Country, City, Specialty, TimeZone,
                          Language, ActivityType, UserMixin)


class Doctor(UserMixin, models.Model):
    MALE_GENDER = True
    FEMALE_GENDER = False
    GENDER_CHOICES = (
        (MALE_GENDER, _('Male')),
        (FEMALE_GENDER, _('Female'))
    )
    city = models.ForeignKey(City)
    country = models.ForeignKey(Country)
    gender = models.BooleanField(choices=GENDER_CHOICES, default=FEMALE_GENDER)
    timezone = models.ForeignKey(TimeZone)
    photo = models.FileField(upload_to='photo', null=True, blank=True,
                             default=None)
    languages = models.ManyToManyField(Language)
    phone_appointment = models.BooleanField(default=False)
    video_appointment = models.BooleanField(default=False)
    consult_rate = models.IntegerField(default=50)
    deposit = models.IntegerField(default=25)

    def __str__(self):
        if self.user.first_name and self.second_last_name:
            return '%s %s %s' % (self.user.first_name, self.user.last_name,
                                 self.second_last_name)
        elif self.user.first_name:
            return '%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return self.user.username

    def __unicode__(self):
        return self.__str__()

    def get_available_time(self, patient):
        time = None
        try:
            time = self.doctorappointmenttime_set.filter(
                start_time__gte=timezone.now(), free=True).exclude(
                patientappointment__case__patient=patient,
                patientappointment__appointment_status=0).first()
        except AttributeError:
            time = None
        return time


class DoctorPayment(models.Model):
    doctor = models.OneToOneField(Doctor)
    name = models.CharField(max_length=100)
    tax_id = models.CharField(max_length=20)
    bill = models.CharField(max_length=50)
    iban = models.CharField(max_length=34)
    hold = models.BooleanField(default=False, blank=True)


class DoctorHistory(models.Model):
    doctor = models.ForeignKey(Doctor)
    record_date = models.DateField(auto_now_add=True)
    type = models.ForeignKey(ActivityType)

    class Meta:
        ordering = ('-record_date',)


class DoctorPaymentHistory(models.Model):
    doctor = models.ForeignKey(Doctor)
    record_date = models.DateField(auto_now_add=True)
    payment = models.CharField(max_length=250)
    money = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ('-record_date',)


class DoctorSpecialty(models.Model):
    doctor = models.ForeignKey(Doctor)
    specialty = models.ForeignKey(Specialty)
    primary = models.BooleanField()

    class Meta:
        ordering = ('-primary',)

    def __str__(self):
        return self.specialty.name

    def __unicode__(self):
        return self.__str__()


class DoctorWorkExperience(models.Model):
    doctor = models.ForeignKey(Doctor)
    care_facility = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


class DoctorAppointmentTime(models.Model):
    doctor = models.ForeignKey(Doctor)
    start_time = models.DateTimeField()
    duration = models.SmallIntegerField(default=0)
    free = models.BooleanField(default=True)
    schedule = models.ForeignKey('utils.AppointmentSchedule', default=None)

    class Meta:
        ordering = ('start_time',)

    def __str__(self):
        return self.start_time.astimezone(
            timezone.get_current_timezone()).strftime('%x %X')

    @property
    def name(self):
        return self.start_time


@receiver(models.signals.post_delete, sender=Doctor)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
