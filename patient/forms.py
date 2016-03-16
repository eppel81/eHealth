import os
from django.utils import timezone
from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import LoginForm, SignupForm
from django.db.models import Q
from postman import forms as postman_forms

from utils.forms import FormControlMixin, AccountPhotoWidget
import models
from utils import models as utils_models

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
    health_conditions = forms.ChoiceField(
        required=True, widget=forms.RadioSelect(), choices=SELECT_CHOICES,
        label=_('Do you have any health conditions?'))

    medications = forms.ChoiceField(
        required=True, widget=forms.RadioSelect(), choices=SELECT_CHOICES,
        label=_('Are you currently taking any medication?'))

    surgeries = forms.ChoiceField(
        required=True, widget=forms.RadioSelect(), choices=SELECT_CHOICES,
        label=_('Do you have any health surgeries?'))

    health_conditions_info = forms.CharField(
        required=False, max_length=255, widget=forms.Textarea(
            {'cols': 40, 'rows': 3, 'style': 'display:none'}), )

    medications_info = forms.CharField(
        required=False, max_length=255, widget=forms.Textarea(
            {'cols': 40, 'rows': 3, 'style': 'display:none'}))

    surgeries_info = forms.CharField(
        required=False, max_length=255, widget=forms.Textarea(
            {'cols': 40, 'rows': 3, 'style': 'display:none'}))

    class Meta:
        model = models.PatientHealthHistory
        fields = ['health_conditions', 'health_conditions_info',
                  'medications', 'medications_info',
                  'surgeries', 'surgeries_info']

    def clean(self):
        cleaned_data = super(HealthHistoryForm, self).clean()
        health_conditions = cleaned_data.get('health_conditions', '')
        health_conditions_info = cleaned_data.get('health_conditions_info', '')

        if health_conditions == 'True' and not health_conditions_info:
            message = "This field is required"
            self._errors['health_conditions_info'] = message

        medications_info = cleaned_data.get('medications_info', '')
        medications = cleaned_data.get('medications', '')

        if medications == 'True'and not medications_info:
            message = "This field is required"
            self._errors['medications_info'] = message

        surgeries = cleaned_data.get('surgeries', '')
        surgeries_info = cleaned_data.get('surgeries_info', '')

        if surgeries == 'True' and not surgeries_info:
            message = "This field is required"
            self._errors['surgeries_info'] = message
        return cleaned_data

    def save(self, commit=True):
        obj = super(HealthHistoryForm, self).save(commit=False)
        health_conditions = obj.health_conditions
        medications = obj.medications
        surgeries = obj.surgeries
        if not health_conditions:
            obj.health_conditions_info = ''
        if not medications:
            obj.medications_info = ''
        if not surgeries:
            obj.surgeries_info = ''
        obj.save()
        return obj


# class MyRecordsForm(FormControlMixin, forms.ModelForm):
#     class Meta:
#         model = models.PatientFile
#         fields = ['file', 'type']
#
#     def __init__(self, *args, **kwargs):
#         super(MyRecordsForm, self).__init__(*args, **kwargs)
#         self.fields['file'].label = _('Upload New Document')
#         self.fields['type'].label = _('Document Type')
#         for field in self.fields.itervalues():
#             field.widget.attrs['class'] += ' rounded-2x'


class LifestyleForm(FormControlMixin, forms.Form):
    def __init__(self, **kwargs):
        super(LifestyleForm, self).__init__(**kwargs)
        self.fields['height_ft'] = forms.IntegerField(
            max_value=10, min_value=0, required=True, label=_('Height'))
        self.fields['height_in'] = forms.IntegerField(
            max_value=12, min_value=0, required=True, label='')
        self.fields['weight'] = forms.IntegerField(
            max_value=400, min_value=0, required=True, label=_('Weight'))
        questions = models.PatientLifestyleQuestion.objects.all()
        for question in questions:
            self.fields['question_%s' % question.id] = forms.ChoiceField(
                required=True, widget=forms.RadioSelect(),
                choices=SELECT_CHOICES, label=_(question.question_string))

    def clean_height_ft(self):
        height_ft = self.cleaned_data['height_ft']
        if height_ft == 0:
            message = "This field must not be empty"
            raise ValidationError(message)
        return height_ft

    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if weight == 0:
            message = "This field must not be empty"
            raise ValidationError(message)
        return weight

    def clean(self):
        cleaned_data = super(LifestyleForm, self).clean()
        for field in cleaned_data.iterkeys():
            if field.startswith('question_'):
                cleaned_data[field] = 'True' in cleaned_data[field]


class FamilyHistoryForm(forms.Form):
    def __init__(self, **kwargs):
        super(FamilyHistoryForm, self).__init__(**kwargs)
        conditions = models.PatientFamilyCondition.objects.filter(
            Q(patient_id=kwargs['initial']['patient_id']) | Q(patient_id=None))
        relationship = models.PatientFamilyRelationship.objects.all()
        for condition in conditions:
            self.fields['condition_%s' % condition.id] = forms.ModelChoiceField(
                required=False, widget=forms.Select(), queryset=relationship,
                label=_(condition.name), empty_label=_("Select"))
        for field in self.fields.itervalues():
            field.widget.attrs.update({'class': 'form-control'})


NUMBER_MESSAGE = 'Only numbers are allowed'
number_validator = RegexValidator(regex='^[0-9]*$', message=NUMBER_MESSAGE)


# class BillingForm(FormControlMixin, forms.ModelForm):
#     zip = forms.CharField(validators=[number_validator])
#     cvv_number = forms.CharField(validators=[number_validator])
#     card_number = forms.CharField(validators=[number_validator])
#
#     class Meta:
#         model = models.PatientBilling
#         fields = ['name', 'address1', 'address2', 'city', 'country',
#                   'zip', 'card_number', 'cvv_number', 'card_type',
#                   'hsa_card', 'expiration_date']
#
#     def __init__(self, **kwargs):
#         super(BillingForm, self).__init__(**kwargs)
#         for key, field in self.fields.iteritems():
#             if key == 'country' or key == 'city':
#                 field.empty_label = 'Select'
#
#     def clean_zip(self):
#         zip = self.cleaned_data['zip']
#         if len(zip) > 6:
#             message = 'Max length 6 symbols'
#             raise ValidationError(message)
#         return zip
#
#     def clean_card_number(self):
#         card_number = self.cleaned_data['card_number']
#         if len(card_number) > 8:
#             message = "Max length 8 symbols"
#             raise ValidationError(message)
#         return card_number
#
#     def clean_cvv_number(self):
#         cvv_number = self.cleaned_data['cvv_number']
#         if len(cvv_number) > 4:
#             message = "Max length 4 symbols"
#             raise ValidationError(message)
#         return cvv_number


class DetailForm(FormControlMixin, forms.ModelForm):
    photo = forms.FileField(label=_('Photo'), widget=AccountPhotoWidget,
                            required=False)

    class Meta:
        model = models.Patient
        fields = ['second_last_name', 'photo', 'country', 'timezone']
        labels = {
            'country': _('Country'),
            'timezone': _('Timezone'),
        }

    def __init__(self, *args, **kwargs):
        super(DetailForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.iteritems():
            if key == 'country' or key == 'timezone':
                field.empty_label = 'Select'


class PatientAppointmentForm(FormControlMixin, forms.ModelForm):
    follow_up = forms.BooleanField(required=False,
                                   label='Is a follow-up appointment')
    patient = forms.ModelChoiceField(models.Patient.objects.none())
    doctor = forms.ModelChoiceField(models.Doctor.objects.none())
    problem = forms.CharField(max_length=255, required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)
    is_second_opinion = forms.BooleanField(required=False)

    class Meta:
        model = models.PatientAppointment

        fields = ['follow_up', 'patient', 'doctor', 'appointment_time',
                  'appointment_type', 'problem', 'comments',
                  'is_second_opinion', 'case']

    def __init__(self, *args, **kwargs):
        self.exclude_fields += ['follow_up', 'is_second_opinion']
        super(PatientAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['case'].required = False
        disabled_fields = ['patient', 'doctor', 'appointment_time']
        for field in disabled_fields:
            self.fields.get(field).widget.attrs.update({'disabled': True})

    def get_required_error(self):
        return _('This field is required')

    def get_empty_error(self):
        return _('This field must be empty')

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')
        patient = self.cleaned_data.get('patient')
        doctor = self.cleaned_data.get('doctor')
        query = models.PatientAppointment.objects.filter(
            case__doctor=doctor,
            appointment_time__start_time=appointment_time.start_time,
            appointment_time__free=False)
        if query.exists():
            message = _('This time has been already taken.')
            raise ValidationError(message)

        patient_time = query.filter(case__patient=patient)
        if patient_time.exists():
            message = _(
                'You already have an appointment to another doctor for '
                'this time.')
            raise ValidationError(message)

        return appointment_time

    def clean_case(self):
        follow_up = self.cleaned_data.get('follow_up')
        case = self.cleaned_data.get('case')
        if follow_up and not case:
            raise ValidationError(self.get_required_error())
        return case

    def clean_comments(self):
        follow_up = self.cleaned_data.get('follow_up')
        comments = self.cleaned_data.get('comments')
        if not follow_up and not comments:
            raise ValidationError(self.get_required_error())
        return comments

    def clean_problem(self):
        follow_up = self.cleaned_data.get('follow_up')
        problem = self.cleaned_data.get('problem')
        if not follow_up and not problem:
            raise ValidationError(self.get_required_error())
        return problem

    def clean_is_second_opinion(self):
        return bool(self.cleaned_data.get('is_second_opinion'))

    def get_or_create_case(self, commit=True):
        case = self.cleaned_data.get('case')
        if not case:
            case = models.PatientCase()
            case.doctor = self.cleaned_data['doctor']
            case.patient = self.cleaned_data['patient']
            case.description = self.cleaned_data['comments']
            case.problem = self.cleaned_data['problem']
        case.is_second_opinion = self.cleaned_data['is_second_opinion']
        case.status = models.PatientCase.OPEN
        if commit:
            case.save()
        return case

    def clean(self):
        cleaned_data = super(PatientAppointmentForm, self).clean()
        patient = self.cleaned_data['patient']
        case = cleaned_data.get('case', '')
        follow_up = cleaned_data['follow_up']
        if follow_up and case:
            cleaned_data.pop('problem')
            cleaned_data.pop('comments')
        if not follow_up and case:
            cleaned_data.pop('case')

        incomplete_appointments = models.PatientAppointment.objects.filter(
            appointment_status=models.PatientAppointment.STATUS_EDIT,
            case__patient=patient)
        if incomplete_appointments.exists():
            message = _('You have an incomplete appointment')
            raise ValidationError(message=message)
        return cleaned_data

    def save(self, commit=True):
        case = self.get_or_create_case(commit)
        obj = super(PatientAppointmentForm, self).save(commit=False)
        obj.case = case
        obj.save()
        models.AppointmentNote.objects.create(appointment=obj)
        return obj


class PatientConsultationForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = models.PatientAppointment
        fields = ['case', 'appointment_time', 'appointment_type']

    def __init__(self, *args, **kwargs):
        super(PatientConsultationForm, self).__init__(*args, **kwargs)
        doctor = kwargs.get('instance').case.doctor
        patient = kwargs.get('instance').case.patient
        self.fields.get('case').queryset = models.PatientCase.objects.filter(
            doctor=doctor, patient=patient)
        current_time = timezone.now()
        self.fields.get('appointment_time').queryset = \
            doctor.doctorappointmenttime_set.filter(
                Q(free=True, start_time__gte=current_time) | Q(pk=self.initial.get('appointment_time')))

    def save(self, commit=True):
        saved = super(PatientConsultationForm, self).save(commit)
        doctor = self.cleaned_data.get('case').doctor
        init_time = self.initial.get('appointment_time')
        change_time = self.cleaned_data.get('appointment_time').id
        used_appointment_time = models.DoctorAppointmentTime.objects.filter(
            free=False, patientappointment__isnull=False, pk=init_time)
        is_appointment_incomplete = True if saved.appointment_status == \
                                            models.PatientAppointment.STATUS_EDIT else False
        if init_time != change_time and not used_appointment_time and \
                not is_appointment_incomplete:
            doctor.doctorappointmenttime_set.filter(pk=init_time).update(
                free=True)
            doctor.doctorappointmenttime_set.filter(pk=change_time).update(
                free=False)
            status = saved.appointment_status
            if status != models.PatientAppointment.STATUS_EDIT and \
                            status != models.PatientAppointment.STATUS_NEW:
                saved.appointment_status = \
                    models.PatientAppointment.STATUS_PATIENT_RESCHEDULE
        saved.save()
        return saved

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data.get('appointment_time')
        patient = self.cleaned_data.get('patient')
        patient_time = models.PatientAppointment.objects.filter(
            case__patient=patient,
            appointment_time__start_time=appointment_time.start_time,
            appointment_time__free=False).exists()

        appointment_initial = models.DoctorAppointmentTime.objects.get(id=self.initial.get('appointment_time'))
        if appointment_time.free is False and appointment_time != appointment_initial:
            message = _('The appointment time has been already taken. '
                        'Please choose another one')
            raise ValidationError(message)
        if patient_time:
            message = _(
                'You already have an appointment to another doctor for this time.')
            raise ValidationError(message)
        return appointment_time


class FilesAddForm(FormControlMixin, forms.ModelForm):
    all_extensions = ['.txt', '.pdf', '.doc', '.docx', '.csx', '.xls',
                      '.xlsx', '.gif', '.png', '.pjpeg']
    case = forms.ModelMultipleChoiceField(
        queryset=models.PatientCase.objects.all())

    class Meta:
        model = models.TestFileRecord
        exclude = ['id', 'conclusions']

    def clean_result_report_or_record(self):
        type = self.cleaned_data.get('type')
        result_report_or_record = self.cleaned_data.get(
            'result_report_or_record')

        if type and not result_report_or_record:
            message = 'This field is required for record type'
            raise ValidationError(message)
        elif result_report_or_record:
            name_file, extension_file = os.path.splitext(
                result_report_or_record.name)
            if extension_file not in self.all_extensions:
                message = "The file has wrong extension"
                raise ValidationError(message)
        return result_report_or_record

    def clean_request_form(self):
        request_form = self.cleaned_data.get('request_form')
        if not request_form:
            message = 'This field is required'
            raise ValidationError(message)
        else:
            name_file, extension_file = os.path.splitext(request_form.name)
            if extension_file not in self.all_extensions:
                message = "The file has wrong extension"
                raise ValidationError(message)
        return request_form

    def save(self, commit=True):
        request_form = self.cleaned_data.pop('request_form')
        report = self.cleaned_data.pop('result_report_or_record')
        if not self.instance.pk:
            self.instance.result_report_or_record = None
            self.instance.request_form = None
        obj = super(FilesAddForm, self).save(commit)
        obj.request_form = request_form
        obj.result_report_or_record = report
        obj.save()
        return obj


class AdditionalFilesForm(FormControlMixin, forms.ModelForm):
    test_file_record = forms.HiddenInput()
    all_extensions = ['.txt', '.pdf', '.doc', '.docx', '.csx', '.xls',
                      '.xlsx', '.gif', '.png', '.pjpeg']

    class Meta:
        model = models.AdditionalFile
        exclude = ['id']

    def clean_file(self):
        add_file = self.cleaned_data.get('file')
        if add_file:
            name_file, extension_file = os.path.splitext(add_file.name)
            if extension_file not in self.all_extensions:
                message = "The file has wrong extension"
                raise ValidationError(message)
        return add_file


AdditionalFilesInlineFormSet = inlineformset_factory(
    models.TestFileRecord,
    models.AdditionalFile,
    can_delete=True,
    extra=1,
    form=AdditionalFilesForm,
)


class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()


class WriteMessageForm(FormControlMixin, postman_forms.WriteForm):
    recipients = UserModelChoiceField(
        label=_("Doctor"), queryset=User.objects.all())

    case = forms.ModelChoiceField(
        label=_('Case'),
        queryset=models.PatientCase.objects.none())

    class Meta(postman_forms.WriteForm.Meta):
        fields = ('recipients', 'case', 'subject', 'body')
        labels = {
            'recipients': _('Recipients'),
            'subject': _('Subject'),
            'body': _('Body'),
        }

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
        utils_models.CaseMessage.objects.create(
            case=case, message=instance)
        return instance


class SupportUserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.supportuser:
            return utils_models.SupportUser.RESPONSIBILITY_CHOICES[
                obj.supportuser.responsibility][1]


class WriteMessageSupportForm(FormControlMixin, postman_forms.WriteForm):
    recipients = SupportUserModelChoiceField(label=_("Support"), queryset=User.objects.filter(supportuser__isnull=False))

    class Meta(postman_forms.WriteForm.Meta):
        fields = ('recipients', 'subject', 'body')
        labels = {
            'recipients': _('Recipients'),
            'subject': _('Subject'),
            'body': _('Body'),
        }

    def clean(self):
        cleaned_data = super(WriteMessageSupportForm, self).clean()
        recipients = cleaned_data.get('recipients')
        if recipients:
            cleaned_data['recipients'] = [recipients,]
        return cleaned_data

