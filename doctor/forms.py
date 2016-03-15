# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
import models
import utils.models as utils_models
import html5.forms.widgets as html5_widgets
from datetime import datetime, date, timedelta
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.forms import modelformset_factory, BaseModelFormSet
from bootstrap3_datetime.widgets import DateTimePicker
from django.utils.translation import ugettext_lazy as _
from patient import models as patient_models
from patient.models import AppointmentNote
from utils.forms import FormControlMixin, AccountPhotoWidget
from postman import forms as postman_forms


class PaymentForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = models.DoctorPayment
        fields = ['name', 'tax_id', 'bill', 'iban', 'hold']


class DetailForm(FormControlMixin, forms.ModelForm):
    photo = forms.FileField(label=_('Photo'), widget=AccountPhotoWidget,
                            required=False)

    class Meta:
        model = models.Doctor
        fields = ['photo', 'city', 'country', 'gender',
                  'timezone', 'languages', 'phone_appointment',
                  'video_appointment', 'consult_rate']


class SpecialtyForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = models.DoctorSpecialty
        fields = ['specialty', 'primary']

    def __init__(self, **kwargs):
        super(SpecialtyForm, self).__init__(**kwargs)
        self.fields['specialty'].queryset = utils_models.Specialty.objects.exclude(
            id__in=kwargs['initial']['exclude_specialty'])


class ExperienceForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = models.DoctorWorkExperience
        fields = ['care_facility', 'position', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        self.fields['start_date'] = forms.DateField(
            widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                           "inLine": True, "pickTime": False}))
        self.fields['end_date'] = forms.DateField(
            widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                           "inline": True, "pickTime": False}))


class NoteForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = AppointmentNote
        exclude = ['appointment', 'doctor']
        widgets = {
            'anamnesis': forms.Textarea({'rows': 3}),
            'exploration': forms.Textarea({'rows': 3}),
            'diagnosis': forms.Textarea({'rows': 3}),
            'additional_tests': forms.Textarea({'rows': 3}),
            'treatment': forms.Textarea({'rows': 3}),
            'public_notes': forms.Textarea({'rows': 3}),
        }


class DoctorScheduleForm(FormControlMixin, forms.ModelForm):
    weekday = forms.BooleanField(required=False)
    day_shift = forms.BooleanField(required=False, label=_('Morning'))
    night_shift = forms.BooleanField(required=False, label=_('Afternoon'))

    class Meta:
        fields = '__all__'
        model = utils_models.AppointmentSchedule
        widgets = {'date': forms.HiddenInput,
                   'doctor': forms.HiddenInput,
                   'day_from': html5_widgets.TimeInput(
                       attrs={'max': '12:00', 'min': '00:00'}),
                   'day_to': html5_widgets.TimeInput(
                       attrs={'max': '12:00', 'min': '00:00'}),
                   'night_from': html5_widgets.TimeInput(
                       attrs={'min': '12:00', 'max': '23:00'}),
                   'night_to': html5_widgets.TimeInput(
                       attrs={'min': '12:00', 'max': '23:00'}),
                   }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        self.request = request
        initial_date = kwargs.get('initial', {}).get('date')
        super(DoctorScheduleForm, self).__init__(*args, **kwargs)
        self._set_day_label(initial_date, self.instance)
        self._disable_fields(initial_date, self.instance)
        self._set_doctor(request)
        self._set_css_classes()

    def get_time_input_error(self):
        return _('Time must be chosen')

    def _set_doctor(self, request):
        self.fields['doctor'].initial = request.user.doctor

    def _set_day_label(self, initial_date, instance):
        if instance.date:
            self.fields['weekday'].label = instance.date.strftime("%A")
        elif initial_date:
            self.fields['weekday'].label = initial_date.strftime("%A")

    def _disable_fields(self, initial_date, instance):
        disabled_fields = ['day_shift', 'day_from', 'day_to',
                           'night_shift', 'night_from', 'night_to']
        errors = self.errors.as_data()

        if instance:
            if instance.day_shift and instance.night_shift:
                disabled_fields = []
                self.fields['weekday'].widget.attrs['checked'] = True
            elif instance.day_shift and not instance.night_shift:
                disabled_fields = ['night_from', 'night_to']
                self.fields['weekday'].widget.attrs['checked'] = True
            elif not instance.day_shift and instance.night_shift:
                disabled_fields = ['day_from', 'day_to']
                self.fields['weekday'].widget.attrs['checked'] = True
        elif errors:
            if 'day_to' in errors or 'day_from' in errors:
                [disabled_fields.remove(item) for item in
                 ['day_to', 'day_from']]
            if 'night_to' in errors or 'night_from' in errors:
                [disabled_fields.remove(item) for item in
                 ['night_to', 'night_from']]
            [disabled_fields.remove(item) for item in
             ['day_shift', 'night_shift']]
            self.fields['weekday'].widget.attrs['checked'] = True

        d = None
        if instance.pk:
            d = instance.date
        elif initial_date:
            d = initial_date
        if d and d <= timezone.now().date():
            disabled_fields.append('weekday')
            disabled_fields.append('day_shift')
            disabled_fields.append('day_from')
            disabled_fields.append('day_to')
            disabled_fields.append('night_shift')
            disabled_fields.append('night_from')
            disabled_fields.append('night_to')
        for _ in disabled_fields:
            self.fields[_].widget.attrs['disabled'] = True

    def _set_css_classes(self):
        css = {'weekday': 'weekday',
               'day_shift': 'shift-day', 'day_from': 'time day',
               'day_to': 'time day',
               'night_shift': 'shift-night', 'night_from': 'time night',
               'night_to': 'time night'}
        for k, v in css.iteritems():
            self.fields[k].widget.attrs['class'] += ' %s' % v
        self.fields['duration'].widget.attrs['class'] += ' duration'

    def clean_day_from(self):
        day_shift = self.cleaned_data.get('day_shift')
        day_from = self.cleaned_data.get('day_from')

        if day_shift and day_from is None:
            raise ValidationError(self.get_time_input_error())
        elif day_from is None:
            return
        else:
            self.is_divisible(day_from)
        min_value = datetime.strptime('00:00', '%H:%M').time()
        max_value = datetime.strptime('12:00', '%H:%M').time()

        if day_from < min_value or day_from > max_value:
            message = _(
                'Time must be in range %s - %s' % (min_value, max_value))
            raise ValidationError(message=message)

        return day_from

    def clean_day_to(self):
        day_shift = self.cleaned_data.get('day_shift')
        day_from = self.cleaned_data.get('day_from')
        day_to = self.cleaned_data.get('day_to')

        if day_shift and day_to is None:
            raise ValidationError(self.get_time_input_error())
        elif day_to is None or day_from is None:
            return
        else:
            self.is_divisible(day_to)
        if day_to < day_from:
            message = _('Time-to less then time-from')
            raise ValidationError(message=message)
        elif day_to == day_from:
            message = _('Time-to should not be equal to time-from')
            raise ValidationError(message=message)

        max_value = datetime.strptime('12:00', '%H:%M').time()
        min_value = datetime.strptime('00:00', '%H:%M').time()

        if day_to < min_value or day_to > max_value:
            message = _(
                'Time must be in range %s - %s' % (min_value, max_value))
            raise ValidationError(message=message)
        return day_to

    def clean_night_from(self):
        night_shift = self.cleaned_data.get('night_shift')
        night_from = self.cleaned_data.get('night_from')
        if night_shift and night_from is None:
            raise ValidationError(self.get_time_input_error())
        elif night_from is None:
            return
        else:
            self.is_divisible(night_from)
        min_value = datetime.strptime('12:00', '%H:%M').time()
        max_value = datetime.strptime('23:59', '%H:%M').time()

        if night_from < min_value or night_from > max_value:
            message = _(
                'Time must be in range %s - %s' % (min_value, max_value))
            raise ValidationError(message=message)
        return night_from

    def clean_night_to(self):
        night_shift = self.cleaned_data.get('night_shift')
        night_from = self.cleaned_data.get('night_from')
        night_to = self.cleaned_data.get('night_to')
        if night_shift and night_to is None:
            raise ValidationError(self.get_time_input_error())
        elif night_to is None or night_from is None:
            return
        else:
            self.is_divisible(night_to)

        if night_to < night_from:
            message = _('Time-to less then time-from')
            raise ValidationError(message=message)
        elif night_to == night_from:
            message = _('Time-to should not be equal to time-from')
            raise ValidationError(message=message)
        min_value = datetime.strptime('12:00', '%H:%M').time()
        max_value = datetime.strptime('23:59', '%H:%M').time()

        if night_to < min_value or night_to > max_value:
            message = _(
                'Time must be in range %s - %s' % (min_value, max_value))
            raise ValidationError(message=message)
        return night_to

    def is_divisible(self, time):
        if time.minute % 15:
            message = _('Time must be divisible by 15 minutes')
            raise ValidationError(message=message)

    def is_correct_period(self, start_time, end_time, duration):
        time_period_h = (datetime.combine(date.today(), end_time) -
                         datetime.combine(date.today(), start_time))
        time_period_min = time_period_h.seconds // 60
        if time_period_min % duration:
            message = _('The appointment length must enter into '
                        'the availability time correctly')
            return ValidationError(message=message, )

    def has_changed(self):
        """
        always return True only for new instances (without id field),
        otherwise call native method
        """
        if self.instance.pk:
            return super(DoctorScheduleForm, self).has_changed()
        else:
            return True

    def clean(self):

        cleaned_data = super(DoctorScheduleForm, self).clean()
        day_from = cleaned_data.get('day_from')
        day_to = cleaned_data.get('day_to')
        night_from = cleaned_data.get('night_from')
        night_to = cleaned_data.get('night_to')
        doctor = cleaned_data.get('doctor')
        app_date = cleaned_data.get('date')
        duration = cleaned_data.get('duration')

        if day_from and day_to:
            error = self.is_correct_period(day_from, day_to, duration)
            if error:
                self.add_error('day_to', error)
        if night_from and night_to:
            error = self.is_correct_period(night_from, night_to, duration)
            if error:
                self.add_error('night_to', error)

        if doctor and app_date:
            appointment_times = models.DoctorAppointmentTime.objects.filter(
                doctor=doctor, schedule=self.instance, free=False)
            if appointment_times.exists():
                message = _('There are appointments for {}'.format(app_date))
                raise ValidationError(message=message)
        return self.cleaned_data

    def get_appointment_to_create(self, schedule, count, time_from, time_to):
        appointments = []
        doctor = self.request.user.doctor
        tz = timezone.get_current_timezone()
        cur_date_time = tz.localize(datetime.combine(schedule.date, time_from))
        max_date_time = tz.localize(datetime.combine(schedule.date, time_to))
        for i in xrange(int(count)):
            if cur_date_time < max_date_time:
                appointments.append(models.DoctorAppointmentTime(
                    doctor=doctor,
                    schedule=schedule,
                    free=True,
                    duration=schedule.duration,
                    start_time=cur_date_time
                ))
                cur_date_time += timedelta(minutes=schedule.duration)

        return appointments

    def save(self, commit=True):
        obj = super(DoctorScheduleForm, self).save(commit)
        doctor = self.request.user.doctor
        models.DoctorAppointmentTime.objects.filter(
            doctor=doctor, schedule=obj).delete()

        new_appointment = []
        today = date.today()
        if obj.day_shift and obj.day_from and obj.day_to:
            minutes = (datetime.combine(today, obj.day_to) -
                       datetime.combine(today,
                                        obj.day_from)).total_seconds() / 60
            count_appointment = minutes / obj.duration
            new_appointment += self.get_appointment_to_create(
                obj, count_appointment, obj.day_from, obj.day_to)
        if obj.night_shift and obj.night_from and obj.night_to:
            minutes = (datetime.combine(today, obj.night_to) -
                       datetime.combine(today,
                                        obj.night_from)).total_seconds() / 60
            count_appointment = minutes / obj.duration
            new_appointment += self.get_appointment_to_create(
                obj, count_appointment, obj.night_from, obj.night_to)
        if new_appointment:
            models.DoctorAppointmentTime.objects.bulk_create(new_appointment)

        return obj


class CustomModelFormset(BaseModelFormSet):
    def __init__(self, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CustomModelFormset, self).__init__(**kwargs)

    def _construct_form(self, *args, **kwargs):
        kwargs['request'] = self.request
        return super(CustomModelFormset, self)._construct_form(*args, **kwargs)


DoctorScheduleFormSet = modelformset_factory(
    formset=CustomModelFormset,
    model=utils_models.AppointmentSchedule,
    form=DoctorScheduleForm,
    extra=0, min_num=7, max_num=7
)


class EditFileRecordForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = patient_models.TestFileRecord
        fields = ['type', 'description', 'conclusions']

    def __init__(self, *args, **kwargs):
        super(EditFileRecordForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.iteritems():
            if key != 'conclusions':
                field.widget.attrs.update({'disabled': True})


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()


class WriteMessageForm(FormControlMixin, postman_forms.WriteForm):
    recipients = UserModelChoiceField(label=_("Patient"), queryset=User.objects.all())
    case = forms.ModelChoiceField(
        queryset=patient_models.PatientCase.objects.none(), required=False)

    class Meta(postman_forms.WriteForm.Meta):
        fields = ('recipients', 'case', 'subject', 'body')

    def clean(self):
        cleaned_data = super(WriteMessageForm, self).clean()
        recipients = cleaned_data.get('recipients')
        if recipients:
            cleaned_data['recipients'] = [recipients,]
        return cleaned_data

    def save(self, **kwargs):
        super(WriteMessageForm, self).save(**kwargs)
        instance = self.instance
        case = self.cleaned_data.get('case')
        if case:
            utils_models.CaseMessage.objects.create(
                case=case, message=instance)
        return instance


class WriteDoctorMessageForm(FormControlMixin, postman_forms.WriteForm):
    recipients = UserModelChoiceField(label=_("Doctor"), queryset=User.objects.all())

    class Meta(postman_forms.WriteForm.Meta):
        fields = ('recipients', 'subject', 'body')

    def clean(self):
        cleaned_data = super(WriteDoctorMessageForm, self).clean()
        recipients = cleaned_data.get('recipients')
        if recipients:
            cleaned_data['recipients'] = [recipients,]
        return cleaned_data


class SupportUserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.supportuser:
            return utils_models.SupportUser.RESPONSIBILITY_CHOICES[
                obj.supportuser.responsibility][1]


class WriteMessageSupportForm(FormControlMixin, postman_forms.WriteForm):
    recipients = SupportUserModelChoiceField(label=_("Support"), queryset=User.objects.filter(supportuser__isnull=False))

    class Meta(postman_forms.WriteForm.Meta):
        fields = ('recipients', 'subject', 'body')

    def clean(self):
        cleaned_data = super(WriteMessageSupportForm, self).clean()
        recipients = cleaned_data.get('recipients')
        if recipients:
            cleaned_data['recipients'] = [recipients,]
        return cleaned_data
