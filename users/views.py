from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.views import View

from users.forms import CustomUserCreationForm, LoginForm
from users.models import Profile


class UserView(View):
    form_class = ''
    template_class = ''
    context = {}

    def get(self, request, *args, **kwargs):
        profiles = Profile.objects.all()
        return render(request, 'users/profiles.html', context={'profiles': profiles})


class RegisterView(View):
    form_class = CustomUserCreationForm
    template_class = 'users/register.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, f'You are already authenticated. ')
            return redirect('trips')
        self.context['registration_form'] = self.form_class
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        """
        Create the user account and also log in
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User account was created!')

            # login(request, user)
            return redirect('trips')

        self.context['registration_form'] = form
        return render(request, self.template_class, self.context)


class LoginView(View):
    form_class = LoginForm
    template_class = 'users/login.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "Sorry you're already logged in!")
            return redirect('trips')

        self.context['form'] = self.form_class
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('trips')

        self.context['form'] = form
        return render(request, self.template_class, self.context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'User was logged out!')
        return redirect('trips')
