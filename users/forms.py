from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


from users.models import Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required. Add a valid email address.')

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Profile.objects.exclude(pk=self.instance.pk).get(email=email)
        except Profile.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} is already in use.', code='email_exists_error')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = Profile.objects.exclude(pk=self.instance.pk).get(username=username)
        except Profile.DoesNotExist:
            return username
        raise forms.ValidationError(f'Username {username} is already in use.', code='username_exists_error')


class LoginForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        breakpoint()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Invalid username or password')


# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['first_name', 'last_name', 'username',
#                   'email', 'profile_image', 'location']
#
#     def __init__(self, *args, **kwargs):
#         super(ProfileForm, self).__init__(*args, **kwargs)
#
#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'input'})

