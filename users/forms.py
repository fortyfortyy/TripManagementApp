from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from users.models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update(
            {'type': 'email', 'name': 'email', 'class': 'form-control', 'placeholder': 'Email address'})

        self.fields['username'].widget.attrs.update(
            {'type': 'text', 'name': 'username', 'class': 'form-control', 'placeholder': 'Username'})

        self.fields['password1'].widget.attrs.update(
            {'type': 'password', 'name': 'password1', 'class': 'form-control', 'placeholder': 'Password'})

        self.fields['password2'].widget.attrs.update(
            {'type': 'password', 'name': 'password2', 'class': 'form-control', 'placeholder': 'Confirm password'})

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if len(email) > 255:
            raise ValidationError(_('Email is too long. Max 255 characters. Please try again.'), code='long_email')

        try:
            account = Profile.objects.get(email=email)
        except Profile.DoesNotExist:
            return email
        raise ValidationError(f'Email {email} is already in use.', code='email_exists')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if len(username) > 60:
            raise ValidationError(_('Username is too long. Max 60 characters. Please try another one.'),
                                  code='long_username')
        try:
            account = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return username
        raise ValidationError(f'Username {username} is already in use.', code='username_exists')


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=60, widget=forms.TextInput(attrs={
        'type': 'text',
        'name': 'username',
        'class': 'form-control',
        'placeholder': 'Username',
    }))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'type': 'password',
        'name': 'password',
        'class': 'form-control',
        'placeholder': 'Password',
    }))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username').lower()
        if len(username) > 60:
            raise ValidationError(_('Username is too long. Max 60 characters. Please try another one.'),
                                  code='long_username')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'location', 'short_intro')

    def clean_first_name(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        if len(first_name) > 150:
            raise ValidationError(_(f'{first_name} is too long. Max 150 characters. Please try another one.'),
                                  code='long_first_name')
        return first_name

    def clean_last_name(self):
        cleaned_data = super().clean()
        last_name = cleaned_data.get('last_name')
        if len(last_name) > 150:
            raise ValidationError(_(f'{last_name} is too long. Max 150 characters. Please try another one.'),
                                  code='long_last_name')
        return last_name

    def clean_location(self):
        cleaned_data = super().clean()
        location = cleaned_data.get('location')
        if len(location) > 50:
            raise ValidationError(_(f'{location} is too long. 50 characters or fewer. Please try another one.'),
                                  code='long_location')
        return location

    def clean_short_intro(self):
        cleaned_data = super().clean()
        short_intro = cleaned_data.get('short_intro')
        if len(short_intro) > 200:
            raise ValidationError(_('Short intro is too long. Max 200 characters. Please try another one.'),
                                  code='long_short_intro')
        return short_intro
