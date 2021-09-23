from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView

from trips.forms import TripPlanCreateEditForm, TripCreateForm, DescriptionFormSet
from trips.models import TripPlan, Trip, Tag


class TripPlansView(LoginRequiredMixin, View):
    """
    Either gets the TripPlans data or
    gets the TripPlans data from the given words from search.
    Then, returns it on the main page.
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
        self.context['form'] = self.form_class()
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name, tag, is_private = form.cleaned_data.items()
            trip_plan = TripPlan.objects.create(owner=request.user, name=name[1], is_private=is_private[1])
            trip_plan.name = name[1]
            trip_plan.is_private = is_private[1]
            tag_obj, created = Tag.objects.get_or_create(tag=tag[1])
            trip_plan.tags.add(tag_obj)
            trip_plan.save()

            messages.success(request, 'The new trip plan has been added!')
            return redirect('create-trip', trip_plan.pk)

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
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        trips = Trip.objects.filter(plan=trip_plan)
        self.context['trips'] = trips
        self.context['trip_plan'] = trip_plan

        return render(request, self.template_class, self.context)


class TripPlanEditView(LoginRequiredMixin, View):
    """
    Displays update form for the TripPlan.
    Handles the data from the form and updates to database.
    Then, redirect to the main page.
    """
    login_url = 'accounts/login/'
    template_class = 'trips/trip-plan-create-form.html'
    form_class = TripPlanCreateEditForm
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Shows update form for the TripPlan.
        """
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        self.context['form'] = self.form_class(instance=trip_plan)
        self.context['update'] = True
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        """
        Handles the data from the form, if there's no any error in form saves to database.
        Then, redirect to the main page.
        """
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        form = self.form_class(request.POST, instance=trip_plan)
        if form.is_valid():
            trip_plan = form.save(commit=False)
            # for tag in form.cleaned_data['tags']:
            tag, created = Tag.objects.get_or_create(tag=form.cleaned_data['tags'])
            trip_plan.tags.add(tag)
            trip_plan.save()
            # name, newtags, is_private = form.cleaned_data.items()
            # trip_plan.name = name[1]
            # trip_plan.is_private = is_private[1]
            # breakpoint()
            # # TODO w jaki sposob najlepiej usuwac stare tagi i aktualizować je nowymi wartoścami z formularza?
            # # old_tag = Tag.objects.get(tags_)
            # for tag in newtags:
            #     tag, created = Tag.objects.get_or_create(tag=tag)
            #     trip_plan.tags.add(tag)

            messages.success(request, "Trip Plan has been updated!")
            return redirect('trip-plans')

        self.context['form'] = form
        messages.error(request, "Ups, something gone wrong")
        return render(request, self.template_class, self.context)


class TripPlanDeleteView(LoginRequiredMixin, View):
    """
    Deletes the Trip Plan instance from the database.
    Then, redirect to the main page.
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
    Displays the trip create form and handles the data form the form.
    """
    login_url = 'accounts/login/'
    template_class = 'trips/trip-create-form.html'
    form_class = TripCreateForm
    context = {}

    def get(self, request, *args, **kwargs):
        """
        Displays the trip form form the trip plan instance.
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
    Displays the extended details of the chosen trip.
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
    Edit the Trip based.
    """
    login_url = 'accounts/login/'
    template_name = 'trips/trip-form.html'
    # form_class = TripDescriptionForm
    model = Trip
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip_id = self.kwargs['pk']
        trip = Trip.objects.get(pk=trip_id)
        # Below Edit Description
        formset = DescriptionFormSet(queryset=trip.description_set.all(), initial=[{'trip': trip_id}])
        context['formset'] = formset
        return context
        # ----------------------------------------------------------------------------------------------

    def post(self, request, *args, **kwargs):
        formset = DescriptionFormSet(request.POST)
        # day_from = request.POST['day_from']
        # day_to = request.POST['day_to']
        # city = request.POST['city']
        # country = request.POST['country']
        # short_description = request.POST['short_description']
        # trip = Trip.objects.get(pk=kwargs['pk'])
        if formset.is_valid():
            formset.save()
            messages.success(request, "Data has been saved!")
            return redirect('trip-details', kwargs['pk'])
        messages.error(request, 'There was an error.')
        return redirect('trip-details', kwargs['pk'])


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
        Then, redirect to the main page.
        """
        trip = Trip.objects.get(pk=kwargs['pk'])
        trip.delete()
        messages.success(request, 'Trip has been deleted successfully')
        return redirect('trip-plan-details', trip.plan.pk)
