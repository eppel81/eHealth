# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from allauth.account.forms import ChangePasswordForm


class FormControlMixin(object):
    exclude_fields = ['terms', 'hsa_card', 'primary', 'phone_appointment', 'video_appointment', 'hold', 'closed']

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
        for field in self.fields.itervalues():
            field.widget.attrs['class'] += ' rounded-2x'
        self.fields['first_name'].required = True  # hack
        self.fields['last_name'].required = True
        self.fields['email'].required = True


class MyChangePassForm(FormControlMixin, ChangePasswordForm):

    def __init__(self, *args, **kwargs):
        super(MyChangePassForm, self).__init__(*args, **kwargs)
        for field in self.fields.itervalues():
            field.widget.attrs['class'] += ' rounded-2x'
            field.widget.attrs['placeholder'] = ''
