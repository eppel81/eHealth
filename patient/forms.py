from fileinput import FileInput
from django import forms
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import LoginForm, SignupForm
from django.db.models import Q
import models
from utils.forms import FormControlMixin

SELECT_CHOICES = (
        (False, 'No'),
        (True, 'Yes')
    )


class AuthForm(FormControlMixin, LoginForm):
    login = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs={'placeholder': _('Email')}
    ))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(
        attrs={'placeholder': _('Password')}))


class RegistrationForm(FormControlMixin, SignupForm):
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(
        attrs={'placeholder': _('Email')}
    ))
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(
        attrs={'placeholder': _('Password')}
    ))
    password2 = forms.CharField(
        label=_("Password confirmation"), widget=forms.PasswordInput(
            attrs={'placeholder': _('Confirm Password')}),
        help_text=_("Enter the same password as above, for verification."))
    terms = forms.BooleanField(required=True, error_messages={
        'required': 'Please, look the terms!'})


class HealthHistoryForm(FormControlMixin, forms.ModelForm):
    health_conditions = forms.ChoiceField(required=True, widget=forms.RadioSelect(), choices=SELECT_CHOICES,
                                          label=_('Do you have any health conditions?'))
    medications = forms.ChoiceField(required=True, widget=forms.RadioSelect(), choices=SELECT_CHOICES,
                                    label=_('Are you currently taking any medication?'))
    surgeries = forms.ChoiceField(required=True, widget=forms.RadioSelect(), choices=SELECT_CHOICES,
                                  label=_('Do you have any health surgeries?'))
    health_conditions_info = forms.CharField(required=False, max_length=255,
                                             widget=forms.Textarea({'cols': 40, 'rows': 3}))
    medications_info = forms.CharField(required=False, max_length=255,
                                       widget=forms.Textarea({'cols': 40, 'rows': 3}))
    surgeries_info = forms.CharField(required=False, max_length=255,
                                     widget=forms.Textarea({'cols': 40, 'rows': 3}))

    class Meta:
        model = models.PatientHealthHistory
        fields = ['health_conditions', 'health_conditions_info',
                  'medications', 'medications_info',
                  'surgeries', 'surgeries_info']


class MyRecordsForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = models.PatientFile
        fields = ['file', 'type']

    def __init__(self, *args, **kwargs):
        super(MyRecordsForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = _('Upload New Document')
        self.fields['type'].label = _('Document Type')
        for field in self.fields.itervalues():
            field.widget.attrs['class'] += ' rounded-2x'


class LifestyleForm(FormControlMixin, forms.Form):

    def __init__(self, **kwargs):
        super(LifestyleForm, self).__init__(**kwargs)
        self.fields['height_ft'] = forms.IntegerField(max_value=10, min_value=0, required=True, label=_('Height'))
        self.fields['height_in'] = forms.IntegerField(max_value=12, min_value=0, required=True, label='')
        self.fields['weight'] = forms.IntegerField(max_value=400, min_value=0, required=True, label=_('Weight'))
        questions = models.PatientLifestyleQuestion.objects.all()
        for question in questions:
            self.fields['question_%s' % question.id] = forms.ChoiceField(required=True,
                                                                         widget=forms.RadioSelect(),
                                                                         choices=SELECT_CHOICES,
                                                                         label=_(question.question_string))

    def clean(self):
        cleaned_date = super(LifestyleForm, self).clean()
        for field in filter(lambda a: a.startswith('question_'), cleaned_date.keys()):
            cleaned_date[field] = 'True' in cleaned_date[field]


class FamilyHistoryForm(forms.Form):
    def __init__(self, **kwargs):
        super(FamilyHistoryForm, self).__init__(**kwargs)
        conditions = models.PatientFamilyCondition.objects.filter(Q(patient_id=kwargs['initial']['patient_id']) |
                                                                  Q(patient_id=None))
        relationship = models.PatientFamilyRelationship.objects.all()
        for condition in conditions:
            self.fields['condition_%s' % condition.id] = forms.ModelChoiceField(required=False,
                                                                                widget=forms.Select(),
                                                                                queryset=relationship,
                                                                                label=_(condition.name),
                                                                                empty_label=_("Select"))
        for field in self.fields.itervalues():
            field.widget.attrs.update({'class': 'form-control'})


class BillingForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = models.PatientBilling
        fields = ['name', 'address1', 'address2', 'city', 'country', 'zip',
                  'card_number', 'cvv_number', 'card_type', 'hsa_card', 'expiration_date']

    def __init__(self, **kwargs):
        super(BillingForm, self).__init__(**kwargs)
        for key, field in self.fields.iteritems():
            if key == 'country' or key == 'city':
                field.empty_label = 'Select'
            field.widget.attrs['class'] += ' rounded-2x'


class AdminImageWidget(forms.ClearableFileInput):
    """
    A ImageField Widget for admin that shows a thumbnail.
    """
    template_with_initial = '%(clear_template)s<br />%(input)s'


class DetailForm(FormControlMixin, forms.ModelForm):
    photo = forms.FileField(label=_('Photo'), widget=AdminImageWidget, required=False)

    class Meta:
        model = models.Patient
        fields = ['photo', 'country', 'timezone']

    def __init__(self, *args, **kwargs):
        super(DetailForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.iteritems():
            if key == 'country' or key == 'timezone':
                field.empty_label = 'Select'
            field.widget.attrs['class'] += ' rounded-2x'
        print self.fields['photo'].widget


class PatientAppointmentForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = models.PatientAppointment
        exclude = ['id', 'appointment_status', 'case']

    def __init__(self, *args, **kwargs):
        super(PatientAppointmentForm, self).__init__(*args, **kwargs)
        disabled_fields = ['patient', 'doctor', 'appointment_time']
        for field in disabled_fields:
            self.fields.get(field).widget.attrs.update({'disabled': True})


class PatientConsultationForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = models.PatientAppointment
        exclude = ['id', 'appointment_status', 'case', 'patient']

    def __init__(self, *args, **kwargs):
        super(PatientConsultationForm, self).__init__(*args, **kwargs)
        doctor = kwargs.get('instance').doctor
        self.fields.get('appointment_time').queryset = doctor.doctorappointmenttime_set.filter(
            Q(free=True) | Q(pk=self.initial.get('appointment_time')))

    def save(self, commit=True):
        saved = super(PatientConsultationForm, self).save(commit)
        doctor = self.cleaned_data.get('doctor')
        init_time = self.initial.get('appointment_time')
        change_time = self.cleaned_data.get('appointment_time').id
        if init_time != change_time:
            doctor.doctorappointmenttime_set.filter(pk=init_time).update(free=True)
            doctor.doctorappointmenttime_set.filter(pk=change_time).update(free=False)
        saved.appointment_status = models.PatientAppointment.STATUS_NEW
        saved.save()
