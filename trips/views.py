from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q

from trips.forms import TripPlanCreateForm, TripCreateForm
# from trips.forms import TripPlanCreateForm, TripCreateForm, TripEditForm
from trips.models import TripPlan, Trip
from users.models import Profile


class TripPlansView(LoginRequiredMixin, View):
    login_url = 'login'
    template_class = 'trips/trip-plans.html'
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


class TripPlanDetailsView(LoginRequiredMixin, View):
    login_url = 'login'
    template_class = 'trips/trip-plan-details.html'
    context = {}

    def get(self, request, *args, **kwargs):
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        trips = Trip.objects.filter(plan=trip_plan)
        self.context['trips'] = trips
        self.context['trip_plan'] = trip_plan

        if request.GET.get('edit') is not None:
            self.context['edit'] = True

        return render(request, self.template_class, self.context)


class TripPlanCreateView(LoginRequiredMixin, View):
    login_url = 'login'
    template_class = 'trips/trip-form.html'
    form_class = TripPlanCreateForm
    context = {}

    def get(self, request, *args, **kwargs):
        self.context['form'] = self.form_class()
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name, is_private = form.cleaned_data.items()
            trip_plan = TripPlan.objects.create(owner=request.user, name=name[1], is_private=is_private[1])

            messages.success(request, 'The new trip plan has been added!')
            return redirect('create-trip', trip_plan.pk)

        self.context['form'] = form
        return render(request, self.template_class, self.context)


class TripPlanEditView(LoginRequiredMixin, View):
    login_url = 'login'
    template_class = 'trips/trip-form.html'
    form_class = TripPlanCreateForm
    context = {}

    def get(self, request, *args, **kwargs):
        trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
        self.context['form'] = self.form_class(instance=trip_plan)
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            name, is_private = form.cleaned_data.items()
            trip_plan = TripPlan.objects.get(pk=kwargs['pk'])
            trip_plan.name = name[1]
            trip_plan.is_private = is_private[1]
            trip_plan.save()

            messages.success(request, "Trip Plan has been updated!")
            return redirect('trip-plans')

        self.context['form'] = form
        messages.error(request, "Ups, something goes wrong")
        return render(request, self.template_class, self.context)


class TripPlanDeleteView(LoginRequiredMixin, View):
    login_url = 'login'
    template_class = 'trips/trip-delete.html'
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
############################################################################################


class TripCreateView(LoginRequiredMixin, View):
    login_url = 'login'
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
            messages.success(request, "Trip has been added successfully!")
            return redirect('trip-plan-details', kwargs['pk'])

        self.context['form'] = form
        return render(request, self.template_class, self.context)


class TripDetailsView(LoginRequiredMixin, View):
    login_url = 'login'
    template_class = 'trips/trip-plan-details.html'
    context = {}

    def get(self, request, *args, **kwargs):
        try:
            trip = Trip.objects.get(pk=kwargs['pk'])
        except Trip.DoesNotExist:
            messages.error(request, "Trip doesn't exists!")
            breakpoint()
            return redirect('trip-plans')
        if request.GET.get('edit'):
            self.context['edit'] = True

        self.context['trip'] = trip
        return render(request, self.template_class, self.context)


class TripEditView(LoginRequiredMixin, View):
    login_url = 'login'
    template_class = 'trips/trip-form.html'
    # form_class = TripEditForm
    context = {}

    # TODO jak stworzyć poprawnie formset dla tego formularza?
    # https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#using-a-model-formset-in-a-view
    # https://docs.djangoproject.com/en/3.2/topics/forms/formsets/#can-order

    # TripFormSet = inlineformset_factory(Trip, Country, City, )
    # TripFormSet = modelformset_factory(Trip, form=TripEditForm, extra=2)
    #
    # def get(self, request, *args, **kwargs):
    #     # trip = Trip.objects.get(pk=kwargs['pk'])
    #     formset = self.TripFormSet(queryset=Trip.objects.get(pk=kwargs['pk']))
    #
    #     # [x.name for x in formset.get_queryset()]
    #     breakpoint()
    #
    #     # form = self.form_class(initial={
    #     #             'day_from': trip.date_range[0],
    #     #             'day_to': trip.date_range[1],
    #     #             # 'trip_images': trip.trip_images,
    #     #             'countries': trip.countries.all(),
    #     #             'cities': trip.cities.all(),
    #     #             'description': trip.descriptions
    #     #         })
    #     self.context['formset'] = formset
    #     return render(request, self.template_class, self.context)
    #
    # def post(self, request, *args, **kwargs):
    #     formset = self.TripFormSet(request.POST)
    #     if formset.is_valid():
    #         breakpoint()
    #         formset.save_m2m()
    #
    #     self.context['formset'] = formset
    #     return render(request, self.template_class, self.context)


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


class TripDeleteView(LoginRequiredMixin, View):
    login_url = 'login'
    template_class = 'trips/trip-delete.html'
    context = {}

    def get(self, request, *args, **kwargs):
        trip = Trip.objects.get(pk=kwargs['pk'])
        self.context['trip'] = trip
        return render(request, self.template_class, self.context)

    def post(self, request, *args, **kwargs):
        trip = Trip.objects.get(pk=kwargs['pk'])
        trip.delete()
        messages.success(request, 'Trip has been deleted successfully')
        return redirect('trip-plan-details', kwargs['pk'])
