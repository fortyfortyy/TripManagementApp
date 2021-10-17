from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from users.forms import CustomUserCreationForm, ProfileForm, LoginForm
from users.models import Profile


class UserView(LoginRequiredMixin, View):
    """
    Show the user account page.
    """
    login_url = '/accounts/login/'
    form_class = ProfileForm
    form_class_template = 'users/user-profile-form.html'
    template_class = 'users/user-profile.html'
    context = {}

    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(pk=kwargs['pk'])
        except Profile.DoesNotExist:
            messages.error(request, "Sorry this profile doesn't exist!")
            return redirect('trip-plans')

        self.context['profile'] = profile
        if request.GET.get('edit-profile'):
            self.context['form'] = self.form_class(instance=profile)
            return render(request, self.form_class_template, self.context)
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=Profile.objects.get(pk=kwargs['pk']))
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated.")
            return redirect('trip-plans')

        messages.error(request, "Something gone wrong. Try again.")
        self.context['form'] = form
        return render(request, self.form_class_template, self.context)

    def handle_no_permission(self):
        messages.error(self.request, "You need first to log in to could see your profile!")
        return super(UserView, self).handle_no_permission()


class RegisterView(View):
    """
    Create the user account and also log in.
    """
    form_class = CustomUserCreationForm
    template_class = 'users/register.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, f'You are already authenticated as {request.user}')
            return redirect('trip-plans')
        self.context['registration_form'] = self.form_class
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('trip-plans')

        self.context['registration_form'] = form
        return render(request, self.template_class, self.context)


class LoginView(View):
    """
    Displays the login form and handles the login action.
    Then redirects to the trip plans page.
    """
    form_class = LoginForm
    template_class = 'users/login.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "Sorry you're already logged-in!")
            return redirect('trip-plans')

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
                return redirect('trip-plans')
        self.context['form'] = form
        messages.error(request, "There was an error. Please try with the correct username or password.")
        return render(request, self.template_class, self.context)


class LogoutView(LoginRequiredMixin, View):
    """
    Logs out the user and displays 'You are logged out' message.
    Then redirects to the log-in page.
    """
    login_url = 'login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'You are logged out!')
        return redirect('trip-plans')
