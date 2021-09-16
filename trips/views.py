from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from trips.forms import TripPlanCreateForm, TripCreateForm
from trips.models import TripPlan, Trip
from users.models import Profile


class TripPlansView(View):
    template_class = 'trips/trip-plans.html'
    context = {}

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in first to see the plans of the trips. ')
            return redirect('login')

        self.context['trip_plans'] = TripPlan.objects.all()
        search_query = request.GET.get('search_query')
        if search_query:
            trip_plans = TripPlan.objects.filter(
                Q(name__icontains=search_query) |
                Q(trip__countries__country__icontains=search_query) |
                Q(trip__cities__city__icontains=search_query) |
                Q(trip__tags__tag__icontains=search_query)
            )
            self.context['trip_plans'] = trip_plans
        return render(request, self.template_class, self.context)


class TripPlanDetailsView(View):
    template_class = 'trips/trip-details.html'
    context = {}

    def get(self, request, *args, **kwargs):
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        trips = Trip.objects.filter(plan=trip_plan)
        self.context['trips'] = trips
        self.context['trip_plan'] = trip_plan
        return render(request, self.template_class, self.context)


# TODO w tym miejscu potrzeba weryfikacji czy jest się zalogowanym (w przyszłości)
class TripPlanCreateView(View):
    template_class = 'trips/trip-form.html'
    form_class = TripPlanCreateForm
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['form'] = self.form_class
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = Profile.objects.get(username='admin')
            name, is_private = form.cleaned_data.items()
            trip_plan = TripPlan.objects.create(owner=username, name=name[1], is_private=is_private[1])

            messages.success(request, 'The new trip plan has been added!')
            return redirect('create-trip', trip_plan.pk)
        self.context['form'] = form
        return render(request, self.template_class, self.context)


############################################################################################
############################################################################################
############################################################################################
############################################################################################
class TripCreateView(View):
    template_class = 'trips/trip-form.html'
    form_class = TripCreateForm
    context = {}

    def get(self, request, *args, **kwargs):
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        form = self.form_class()
        self.context['trip_plan'] = trip_plan
        self.context['form'] = form
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            country, city, day_from, day_to, description = form.cleaned_data.items()

            trip = Trip.objects.create(plan=TripPlan.objects.get(pk=kwargs['pk']))
            trip.days_set.create(trip=trip, day_from=day_from[1], day_to=day_to[1])
            trip.countries.create(country=country[1])
            trip.cities.create(city=city[1])
            trip.description_set.create(content=description[1])

            return redirect('trip-plans')
        self.context['form'] = form
        return render(request, self.template_class, self.context)


# TODO w tym miejscu potrzeba weryfikacji czy jest się zalogowanym (w przyszłości)
class TripDetailsView(View):
    template_class = 'trips/trip-details.html'
    context = {}

    def get(self, request, *args, **kwargs):
        try:
            trip = Trip.objects.get(pk=kwargs['pk'])
        except Trip.DoesNotExist:
            messages.error(request, 'Trip doesnt exists!')
            breakpoint()
            return redirect('trip-plans')
        if request.GET.get('edit'):
            self.context['edit'] = True
        self.context['trip'] = trip
        return render(request, self.template_class, self.context)


# class TripEditView(View):
#     template_class = 'trips/trip-edit.html'
#     form_class = SmallTripCreateForm
#     context = {}
#
#     def get(self, request, *args, **kwargs):
#         trip = Trip.objects.get(pk=kwargs['pk'])
#         form = self.form_class(initial={
#             'name': trip.name,
#             'day_from': trip.day_from,
#             'day_to': trip.day_to,
#             'trip_images': trip.trip_images,
#             'countries': trip.countries.all(),
#             'cities': trip.cities.all(),
#         })
#         self.context['form'] = form
#         return render(request, self.template_class, self.context)
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             pass


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
