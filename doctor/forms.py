# -*- coding: utf-8 -*-
from django import forms
from utils.forms import FormControlMixin
import models
from utils.models import Specialty
from bootstrap3_datetime.widgets import DateTimePicker
from django.utils.translation import ugettext_lazy as _
from patient import models as patient_models
from django.forms.models import inlineformset_factory



class PaymentForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = models.DoctorPayment
        fields = ['name', 'tax_id', 'bill', 'iban', 'hold']


class DetailForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = models.Doctor
        fields = ['city', 'country', 'gender', 'timezone', 'photo',
                  'languages', 'phone_appointment', 'video_appointment']


class SpecialtyForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = models.DoctorSpecialty
        fields = ['specialty', 'primary']

    def __init__(self, **kwargs):
        super(SpecialtyForm, self).__init__(**kwargs)
        self.fields['specialty'].queryset = Specialty.objects.exclude(id__in=kwargs['initial']['exclude_specialty'])


class ExperienceForm(FormControlMixin, forms.ModelForm):

    class Meta:
        model = models.DoctorWorkExperience
        fields = ['care_facility', 'position', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        self.fields['start_date'] = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                          "inLine": True, "pickTime": False}))
        self.fields['end_date'] = forms.DateField(widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                                                        "inline": True, "pickTime": False}))





