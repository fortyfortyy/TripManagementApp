from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from trips.forms import TripCreateForm
from trips.models import Trip
from users.models import Profile


class TripsView(View):
    template_class = 'trips/trips.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['trips'] = Trip.objects.all()
        return render(request, self.template_class, self.context)


# TODO w tym miejscu potrzeba weryfikacji czy jest się zalogowanym (w przyszłości)
class TripDetailsView(View):
    template_class = 'trips/single-trip.html'
    context = {}

    def get(self, request, *args, **kwargs):
        try:
            trip = Trip.objects.get(pk=kwargs['pk'])
        except Trip.DoesNotExist:
            messages.error(request, 'Trip doesnt exists!')
            breakpoint()
            return redirect('trips')
        self.context['trip'] = trip
        return render(request, self.template_class, self.context)


# TODO w tym miejscu potrzeba weryfikacji czy jest się zalogowanym (w przyszłości)
class TripCreate(View):
    template_class = 'trips/trip-creation-form.html'
    form_class = TripCreateForm
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['form'] = self.form_class
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = Profile.objects.get(username='admin')

            trip_name, day_from, day_to = form.cleaned_data.items()
            Trip.objects.create(owner=username, name=trip_name[1], day_from=day_from[1], day_to=day_to[1])
            messages.success(request, 'Trip has been added!')
            return redirect('trips')
        self.context['form'] = form
        return render(request, self.template_class, self.context)
