from django import forms
from django.contrib.auth.models import User


NON_FORM_CONTROL_WIDGETS = (
    'BootstrapCheckboxSelectMultiple',
    'CheckboxInput'
)

class BootstrapForm(forms.Form):
    def __init__(self, *args, **kwargs):

        super(BootstrapForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            field = self.fields[myField]
            if field.widget.__class__.__name__ not in NON_FORM_CONTROL_WIDGETS:
                field.widget.attrs['class'] = 'form-control'


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            field = self.fields[myField]
            if field.widget.__class__.__name__ not in NON_FORM_CONTROL_WIDGETS:
                field.widget.attrs['class'] = 'form-control'

class LoginForm(BootstrapForm):
    """ Basic Login Form. """
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=64,
                               widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
