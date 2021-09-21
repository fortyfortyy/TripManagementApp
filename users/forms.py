from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from users.models import Profile


class CustomUserCreationForm(UserCreationForm):
    # email = forms.EmailField(max_length=60)

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
        if len(email) > 60:
            raise ValidationError(_('Email is too long. Max 60 characters. Please try another one.'), code='long_email')
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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get('username').lower()
    #     if len(username) > 60:
    #         raise ValidationError(_('Username is too long. Max 60 characters. Please try another one.'),
    #                               code='long_username')
    #
    #     password = cleaned_data.get('password')
    #     if not authenticate(email=username, password=password):
    #         raise ValidationError('Invalid username or password', code='invalid_authenticate')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'username', 'profile_image', 'location', 'short_intro')

    # def __init__(self, *args, **kwargs):
    #     super(ProfileForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['first_name'].widget.attrs.update(
    #         {'type': 'text', 'name': 'first_name', 'class': 'form-control', 'placeholder': 'first name'})
    #
    #     self.fields['last_name'].widget.attrs.update(
    #         {'type': 'text', 'name': 'last_name', 'class': 'form-control', 'placeholder': 'surname'})
    #
    #     self.fields['username'].widget.attrs.update(
    #         {'type': 'text', 'name': 'username', 'class': 'form-control', 'placeholder': 'username'})
    #
    #     self.fields['short_intro'].widget.attrs.update(
    #         {'type': 'text', 'name': 'short_intro', 'class': 'form-control', 'placeholder': 'bio'})
    #
    #     self.fields['location'].widget.attrs.update(
    #         {'type': 'text', 'name': 'location', 'class': 'form-control', 'placeholder': 'location'})
