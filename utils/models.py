import braintree
from django.contrib.auth.models import User
import pytz
from django.utils.translation import ugettext_lazy as _
from django.db import models
from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from opentok import OpenTok, MediaModes
from django.conf import settings


def localize_datetime(dt):
    return pytz.timezone(timezone.get_current_timezone_name()).localize(
        dt, is_dst=None)


class UserMixin(models.Model):
    user = models.OneToOneField(User)
    second_last_name = models.CharField(_('Second last name'), max_length=30,
                                        blank=True, null=True)

    class Meta:
        abstract = True


class City(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class TimeZone(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=50)
    timezone = models.ManyToManyField(TimeZone)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Specialty(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Specialties'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Languages'

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
        ordering = ('name',)

    def __str__(self):
        return self.name


class AppointmentSchedule(models.Model):
    QUARTER = 15
    HALF = 30
    THREE_FOURTH = 45
    HOUR = 60
    DURATION_CHOICES = (
        (QUARTER, _('15 minutes')),
        (HALF, _('30 minutes')),
        (THREE_FOURTH, _('45 minutes')),
        (HOUR, _('1 hour'))
    )
    doctor = models.ForeignKey('doctor.Doctor', default=None)
    date = models.DateField()
    day_shift = models.BooleanField(default=False)
    day_from = models.TimeField(null=True, blank=True)
    day_to = models.TimeField(null=True, blank=True)
    night_shift = models.BooleanField(default=False)
    night_from = models.TimeField(null=True, blank=True)
    night_to = models.TimeField(null=True, blank=True)
    duration = models.SmallIntegerField(choices=DURATION_CHOICES,
                                        default=QUARTER)

    def __str__(self):
        return str(self.date)


class SupportUser(models.Model):
    TECHNICAL_SUPPORT = 0
    BILLING = 1
    COMMUNICATION = 2
    RESPONSIBILITY_CHOICES = (
        (TECHNICAL_SUPPORT, _('Technical issues')),
        (BILLING, _('Billing Enquiries')),
        (COMMUNICATION, _('Doctor-Patient communication')),
    )
    user = models.OneToOneField(User)
    responsibility = models.SmallIntegerField(
        choices=RESPONSIBILITY_CHOICES, default=TECHNICAL_SUPPORT)
    timezone = models.ForeignKey(TimeZone, null=True, blank=True, default=None)

    def __str__(self):
        return str(self.RESPONSIBILITY_CHOICES[self.responsibility][1])

    def __unicode__(self):
        return self.__str__()


class CaseMessage(models.Model):
    case = models.ForeignKey('patient.PatientCase')
    message = models.OneToOneField('postman.Message')


class CustomerUser(models.Model):
    user = models.OneToOneField(User)
    customer = models.IntegerField(blank=True, null=True)


@receiver(user_logged_in)
def select_type_user(sender, **kwargs):
    if hasattr(kwargs['user'], 'doctor'):
        kwargs['request'].session['type_user'] = 'doctor'

    if hasattr(kwargs['user'], 'patient'):
        kwargs['request'].session['type_user'] = 'patient'


@receiver(models.signals.post_save, sender='patient.Patient')
def create_customer_on_patient_create(sender, instance, created, **kwargs):
    user = instance.user
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    if created:
        result = braintree.Customer.create({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        })
        if result.is_success:
            CustomerUser.objects.create(
                user=user, customer=result.customer.id)

    else:
        braintree.Customer.update(str(user.customeruser.customer), {
            "first_name": first_name,
            "last_name": last_name,
        })


@receiver(models.signals.post_save, sender='patient.PatientCase')
def generate_opentok_token(sender, instance, created, **kwargs):
    if created:
        opentok = OpenTok(settings.OPENTOK_API_KEY, settings.OPENTOK_API_SECRET)
        session = opentok.create_session(media_mode=MediaModes.routed)
        instance.opentok_session = session.session_id
        instance.save()