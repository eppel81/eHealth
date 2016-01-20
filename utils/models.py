import pytz
from django.db import models
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone


def localize_datetime(dt):
    return pytz.timezone(timezone.get_current_timezone_name()).localize(dt, is_dst=None)


class City(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class TimeZone(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50)
    timezone = models.ManyToManyField(TimeZone)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Specialty(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Specialties'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name', )
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name


class AppointmentReason(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class ActivityType(models.Model):
    SIGNIN_TYPE = 'signin'
    SIGNUP_TYPE = 'signup'
    NEW_APPOINTMENT_TYPE = 'appointment'
    TYPE_CHOICES = (
        (SIGNIN_TYPE, 'Sign-in'),
        (SIGNUP_TYPE, 'Sign-Up'),
        (NEW_APPOINTMENT_TYPE, 'New Appointment')
    )
    name = models.CharField(max_length=50, choices=TYPE_CHOICES)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


@receiver(user_logged_in)
def select_type_user(sender, **kwargs):

    if hasattr(kwargs['user'], 'doctor'):
        kwargs['request'].session['type_user'] = 'doctor'

    if hasattr(kwargs['user'], 'patient'):
        kwargs['request'].session['type_user'] = 'patient'



