from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from trips.forms import TripCreateForm
from trips.models import Trip
from users.models import Profile


class TripsView(View):
    template_class = 'trips/trips.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in first to see the trips. ')
            return redirect('login')

        search_query = request.GET.get('search_query')
        if search_query:
            trips = Trip.objects.filter(
                Q(name__icontains=search_query) |
                Q(countries__country__icontains=search_query) |
                Q(cities__city__icontains=search_query) |
                Q(tags__tag__icontains=search_query)
            )
            self.context['trips'] = trips
            return render(request, self.template_class, self.context)

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

    def post(self, request, *args, **kwargs):
        breakpoint()


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
            name, day_from, day_to, country, city, tag = form.cleaned_data.items()
            trip = Trip.objects.create(owner=username, name=name[1], day_from=day_from[1], day_to=day_to[1])
            trip.countries.create(country=country[1])
            trip.cities.create(city=city[1])
            trip.tags.create(tag=tag[1])

            messages.success(request, 'Trip has been added!')
            return redirect('trips')
        self.context['form'] = form
        return render(request, self.template_class, self.context)


class TripUpdateView(View):
    template_class = 'trips/trip-edit.html'
    form_class = TripCreateForm
    context = {}

    def get(self, request, *args, **kwargs):
        trip = Trip.objects.get(pk=kwargs['pk'])
        form = self.form_class(initial={
            'name': trip.name,
            'day_from': trip.day_from,
            'day_to': trip.day_to,
            'trip_images': trip.trip_images,
            'countries': trip.countries.all(),
            'cities': trip.cities.all(),
            'tags': trip.tags.all(),
        })
        self.context['form'] = form
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            pass


class TripDeleteView(View):
    template_class = 'trips/trip-delete.html'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['trip'] = Trip.objects.get(pk=kwargs['pk'])
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        trip = Trip.objects.get(pk=kwargs['pk'])
        trip.delete()
        messages.success(request, 'Trip has been deleted successfully')
        return redirect('trips')
