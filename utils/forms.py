# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from allauth.account.forms import ChangePasswordForm
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _


class AccountPhotoWidget(forms.ClearableFileInput):
    """
    A ImageField Widget for admin that shows a thumbnail.
    """
    template_with_initial = '%(clear_template)s<br />%(input)s'


class FormControlMixin(object):
    exclude_fields = ['terms', 'hsa_card', 'primary', 'phone_appointment',
                      'video_appointment', 'hold', 'closed', 'weekday',
                      'day_shift', 'night_shift', 'remember']

    def __init__(self, *args, **kwargs):
        super(FormControlMixin, self).__init__(*args, **kwargs)
        for key, field in self.fields.iteritems():
            if key not in self.exclude_fields:
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': ''})


class DetailUserForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(DetailUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True  # hack
        self.fields['last_name'].required = True
        self.fields['email'].required = True


class MyChangePassForm(FormControlMixin, ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyChangePassForm, self).__init__(*args, **kwargs)
        for field in self.fields.itervalues():
            field.widget.attrs['placeholder'] = ''


class MyResetPassForm(FormControlMixin, PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'placeholder': _("E-mail address")}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        users = list(self.get_users(email))
        if not users:
            message = _("That email address doesn't have an associated user "
                        "account. Are you sure you've registered?")
            raise ValidationError(message)
        return email


class MySetPassForm(FormControlMixin, SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _("New password")}))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': _("Confirm password")}))
