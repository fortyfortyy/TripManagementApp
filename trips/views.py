from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import UpdateView

from trips.forms import CityFormSet, CountryFormSet, DescriptionFormSet, TagFormSet, TripCreateForm, \
    TripPlanCreateEditForm
from trips.models import Tag, Trip, TripPlan, Description


class TripPlansView(LoginRequiredMixin, View):
    """
    Either gets the TripPlans data or
    gets the TripPlans data from the given words from search.
    Then, returns it to the main page.
    """
    login_url = 'accounts/login/'
    template_class = 'trips/trip-plans.html'
    permission_denied_message = 'fck you'
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['trip_plans'] = TripPlan.objects.all()
        search_query = request.GET.get('search_query')
        if search_query:
            trip_plans = TripPlan.objects.filter(
                Q(name__icontains=search_query) |
                Q(trip__countries__country__icontains=search_query) |
                Q(trip__cities__city__icontains=search_query) |
                Q(tags__tag__icontains=search_query)
            ).distinct()
            self.context['trip_plans'] = trip_plans
        return render(request, self.template_class, self.context)


class TripPlanCreateView(LoginRequiredMixin, View):
    """
    Displays form to create the new TripPlan.
    Handles the data from the form and saves to database.
    Then, redirect to the trip create page.
    """
    login_url = 'accounts/login/'
    template_class = 'trips/trip-plan-create-form.html'
    form_class = TripPlanCreateEditForm
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Returns the forms for the tag/s and for the Trip Plan.
        """
        tag_formset = TagFormSet(queryset=Tag.objects.none(), prefix='tags')
        self.context['tag_formset'] = tag_formset
        self.context['form'] = self.form_class()
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        """
        Checks whether the data is valid. Saves tag/s to the Trip Plan given instance.
        """
        form = self.form_class(request.POST)
        tag_formset = TagFormSet(request.POST, request.FILES, prefix='tags')
        if form.is_valid() and tag_formset.is_valid():
            trip_plan = form.save(commit=False)
            trip_plan.owner = request.user
            trip_plan.save()
            for tag in tag_formset.cleaned_data:
                if tag['tag'] != '' and not tag['DELETE']:
                    trip_plan.tags.get_or_create(tag=tag['tag'])

            messages.success(request, 'The new trip plan has been added!')
            return redirect('create-trip', trip_plan.pk)

        messages.error(request, 'Ups, there was an error during sending.')
        self.context['tag_formset'] = tag_formset
        self.context['form'] = form
        return render(request, self.template_class, self.context)


class TripPlanDetailsView(LoginRequiredMixin, View):
    """
    Displays details of the TripPlan.
    """
    login_url = 'accounts/login/'
    template_class = 'trips/trip-plan-details.html'
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Returns more information about the Trip Plan of given pk.
        """
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        trips = Trip.objects.filter(plan=trip_plan)
        self.context['trips'] = trips
        self.context['trip_plan'] = trip_plan
        return render(request, self.template_class, self.context)


class TripPlanEditView(LoginRequiredMixin, View):
    """
    Displays update form for the Trip Plan.
    Handles the data from the form and updates to database.
    Then, redirects to the main page.
    """
    login_url = 'accounts/login/'
    template_class = 'trips/trip-plan-create-form.html'
    form_class = TripPlanCreateEditForm
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Returns the forms that are based on previous data for the tag/s and for the Trip Plan.
        """
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        tag_formset = TagFormSet(queryset=trip_plan.tags.all(), prefix='tags')
        self.context['tag_formset'] = tag_formset
        self.context['form'] = self.form_class(instance=trip_plan)
        self.context['update'] = True
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        """
        Handles the data the forms, if there's no any error, saves to database.
        Then, redirects to the Trip Plan details page.
        """
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=trip_plan)
        tag_formset = TagFormSet(request.POST, request.FILES, prefix='tags')
        if form.is_valid() and tag_formset.is_valid():
            form.save()
            tags = tag_formset.save(commit=False)

            for tag in tags:
                if tag:
                    trip_plan.tags.get_or_create(tag=tag)
            tag_formset.save()
            messages.success(request, f"{trip_plan.name} has been updated!")
            return redirect('trip-plan-details', trip_plan.pk)

        messages.error(request, 'Ups there was an error during sending.')
        self.context['tag_formset'] = tag_formset
        self.context['form'] = form
        return render(request, self.template_class, self.context)


class TripPlanDeleteView(LoginRequiredMixin, View):
    """
    Deletes the Trip Plan object from the database.
    Then, redirects to the main page.
    """
    login_url = 'accounts/login/'
    template_class = 'trips/delete-form.html'
    context = {}

    def get(self, request, *args, **kwargs):
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        self.context['trip_plan'] = trip_plan
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        trip_plan.delete()
        messages.success(request, 'Trip Plan has been deleted successfully')
        return redirect('trip-plans')


class TripCreateView(LoginRequiredMixin, View):
    """
    Displays the create form for the Trip, then handles the data.
    """
    login_url = 'accounts/login/'
    template_class = 'trips/trip-create-form.html'
    form_class = TripCreateForm
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Displays the create form for based on the Trip Plan instance.
        """
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        form = self.form_class()
        self.context['trip_plan'] = trip_plan
        self.context['form'] = form
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        """
        Handles the data from the form.
        Displays the errors if exists or saves to the database.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            country, city, day_from, day_to, short_description = form.cleaned_data.items()
            trip = Trip.objects.create(
                plan=TripPlan.objects.get(pk=kwargs['pk']),
                short_description=short_description[1],
            )
            trip.days_set.create(trip=trip, day_from=day_from[1], day_to=day_to[1])
            trip.countries.create(country=country[1])
            trip.cities.create(city=city[1])
            messages.success(request, "Trip has been added successfully!")
            return redirect('trip-plan-details', kwargs['pk'])

        messages.error(request, 'Ups, something gone wrong')
        self.context['form'] = form
        return render(request, self.template_class, self.context)


class TripDetailsView(LoginRequiredMixin, View):
    """
    Displays the extended details of the chosen Trip.
    """
    login_url = 'accounts/login/'
    template_class = 'trips/trip-details.html'
    context = {}

    def get(self, request, *args, **kwargs):
        try:
            trip = Trip.objects.get(pk=kwargs['pk'])
        except Trip.DoesNotExist:
            messages.error(request, "Trip doesn't exists!")
            return redirect('trip-plans')

        self.context['trip_plan'] = trip.plan
        self.context['trip'] = trip
        return render(request, self.template_class, self.context)


class TripEditView(LoginRequiredMixin, UpdateView):
    """
    Displays update form for the Trip.
    Handles the data from the form and updates to database.
    Then, redirects to the Trip Details page.
    """
    login_url = 'accounts/login/'
    template_name = 'trips/trip-form.html'
    model = Trip
    fields = '__all__'

    def get_context_data(self, **kwargs):
        """
        Returns formsets for city, country, description objects.
        """
        context = super().get_context_data(**kwargs)
        trip_id = self.kwargs['pk']
        trip = Trip.objects.get(pk=trip_id)

        # City Formset
        city_formset = CityFormSet(queryset=trip.cities.all(), prefix='cities')
        context['city_formset'] = city_formset

        # Country Formset
        country_formset = CountryFormSet(queryset=trip.countries.all(), prefix='countries')
        context['country_formset'] = country_formset

        # Description Formset
        description_formset = DescriptionFormSet(
            queryset=trip.description_set.all(),
            initial=[{'trip': trip_id}],
            prefix='descriptions',
        )
        context['description_formset'] = description_formset
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles the data from the formsets.
        Saves to the database if all is correctly.
        """
        trip = Trip.objects.get(pk=kwargs['pk'])
        description_formset = DescriptionFormSet(request.POST, request.FILES, prefix='descriptions')
        city_formset = CityFormSet(request.POST, request.FILES, prefix='cities')
        country_formset = CountryFormSet(request.POST, request.FILES, prefix='countries')
        count = 0
        if description_formset.is_valid():
            for desc_form in description_formset:
                if desc_form.cleaned_data['content'] != '' and not desc_form.cleaned_data['DELETE']:
                    desc_form.save()
                if desc_form.cleaned_data['DELETE']:
                    try:
                        obj = Description.objects.filter(trip=trip, content=desc_form.cleaned_data['content'])
                        obj.delete()
                    except Description.DoesNotExist:
                        pass
            count += 1
        else:
            messages.error(request, "There was an error with the description.")
        if city_formset.is_valid():
            cities = city_formset.save(commit=False)
            for city in cities:
                if city:
                    trip.cities.get_or_create(city=city)
            city_formset.save()
            count += 1
        else:
            messages.error(request, "There was an error with the city.")
        if country_formset.is_valid():
            countries = country_formset.save(commit=False)
            for country in countries:
                if country:
                    trip.countries.get_or_create(country=country)
            country_formset.save()
            count += 1
        else:
            messages.error(request, "There was an error with the country.")
        if count == 3:
            messages.success(request, "Data has been correctly saved!")
            return redirect('trip-details', kwargs['pk'])
        return redirect('edit-trip', kwargs['pk'])


class TripDeleteView(LoginRequiredMixin, View):
    """
    Delete the Trip based on its Plan.
    """
    login_url = 'accounts/login/'
    template_class = 'trips/delete-form.html'
    context = {}

    def get(self, request, *args, **kwargs):
        """
        View that gets the Trip instance.
        """
        trip = Trip.objects.get(pk=kwargs['pk'])
        self.context['trip'] = trip
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        """
        Deletes the trip instance form the database.
        Then, redirect to the Trip Plan Details page.
        """
        trip = Trip.objects.get(pk=kwargs['pk'])
        trip.delete()
        messages.success(request, 'Trip has been deleted successfully')
        return redirect('trip-plan-details', trip.plan.pk)
