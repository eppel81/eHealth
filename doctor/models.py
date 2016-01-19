import os
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from utils.models import (Country, City, Specialty, TimeZone,
                          Language, ActivityType, AppointmentReason)


class Doctor(models.Model):
    MALE_GENDER = True
    FEMALE_GENDER = False
    GENDER_CHOICES = (
        (MALE_GENDER, 'Male'),
        (FEMALE_GENDER, 'Female')
    )
    user = models.OneToOneField(User)
    city = models.ForeignKey(City)
    country = models.ForeignKey(Country)
    gender = models.BooleanField(choices=GENDER_CHOICES, default=FEMALE_GENDER)
    timezone = models.ForeignKey(TimeZone)
    photo = models.FileField(upload_to='photo', null=True, blank=True, default=None)
    languages = models.ManyToManyField(Language)
    phone_appointment = models.BooleanField(default=False)
    video_appointment = models.BooleanField(default=False)

    def __str__(self):
        if self.user.first_name:
            return '%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return self.user.email

    def get_available_time(self):
        time = None
        try:
            date = self.doctorappointmentdate_set.filter(appointment_date__gte=timezone.now())
            for day in date:
                try:
                    time = day.doctorappointmenttime_set.filter(free=True).first()
                    time = time.start_time
                    break
                except AttributeError:
                    time = None
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
        ordering = ('-record_date', )


class DoctorPaymentHistory(models.Model):
    doctor = models.ForeignKey(Doctor)
    record_date = models.DateField(auto_now_add=True)
    payment = models.CharField(max_length=250)
    money = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        ordering = ('-record_date', )


class DoctorSpecialty(models.Model):
    doctor = models.ForeignKey(Doctor)
    specialty = models.ForeignKey(Specialty)
    primary = models.BooleanField()

    class Meta:
        ordering = ('-primary', )

    def __str__(self):
        return self.specialty.name


class DoctorWorkExperience(models.Model):
    doctor = models.ForeignKey(Doctor)
    care_facility = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


class DoctorAppointmentDate(models.Model):
    doctor = models.ForeignKey(Doctor)
    appointment_date = models.DateField()

    class Meta:
        ordering = ('appointment_date', )

    def __str__(self):
        return self.appointment_date.strftime('%Y-%m-%d')


class DoctorAppointmentTime(models.Model):
    appointment_date = models.ForeignKey(DoctorAppointmentDate)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    free = models.BooleanField(default=True)

    class Meta:
        ordering = ('start_time', )

    def __str__(self):
        return self.start_time.strftime('%H:%M')+'-'+self.end_time.strftime('%H:%M')

    # todo: timezone support!!!
    @property
    def name(self):
        return str(self)


@receiver(models.signals.post_delete, sender=Doctor)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
