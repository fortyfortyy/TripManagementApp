from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import Profile

from dynamic_filenames import FilePattern
from stdimage import StdImageField, JPEGField

import uuid


# https://github.com/codingjoe/django-dynamic-filenames
# https://github.com/codingjoe/django-stdimage


def get_trip_image_filepath(self, filename):
    return f'trips/{str(self.pk)}/{filename}'


class TripPlan(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    members = models.ManyToManyField(Profile, related_name='trip_members', through='TripPlanGroup')
    name = models.CharField(_("Trip Plan Name"), max_length=200, unique=True)
    is_private = models.BooleanField(default=True)
    tags = models.ManyToManyField('Tag', related_name='tags')

    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    @property
    def dates(self):
        trips = Trip.objects.filter(plan=self.id)
        dates = []
        for trip in trips:
            if trip.date_range:
                for date in trip.date_range:
                    dates.append(date.strftime('%y-%m-%d'))
        if dates:
            dates.sort()
            return [dates[0], dates[-1]]
        return ''

    @property
    def countries(self):
        trips = Trip.objects.filter(plan=self.id)
        countries = []
        for trip in trips:
            for country_obj in trip.countries.all():
                if country_obj.country not in countries:
                    countries.append(country_obj.country)
        return countries

    @property
    def cities(self):
        trips = Trip.objects.filter(plan=self.id)
        cities = []
        for trip in trips:
            for city_obj in trip.cities.all():
                if city_obj.city not in cities:
                    cities.append(city_obj.city)
        return cities


class Trip(models.Model):
    plan = models.ForeignKey(TripPlan, on_delete=models.CASCADE)
    short_description = models.CharField(_('short_description'), null=True, blank=True, max_length=64)
    # creates a thumbnail resized to maximum size to fit a 100x75 area
    trip_images = models.ImageField(
        max_length=255, blank=True, null=True, upload_to=get_trip_image_filepath, default="")
    countries = models.ManyToManyField('Country', related_name='countries')
    cities = models.ManyToManyField('City', related_name='cities')

    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.short_description

    @property
    def descriptions(self):
        # TODO Shift + F6 change from descriptions to activity
        activities = self.description_set.all().values_list('content', flat=True)
        return activities

    @property
    def date_range(self):
        queryset = self.days_set.all().values_list('day_from', 'day_to')
        for days in queryset:
            return days


class TripPlanGroup(models.Model):
    """
    TODO in the future
    """
    trip_plan = models.OneToOneField(TripPlan, on_delete=models.CASCADE)
    profiles = models.ForeignKey(Profile, on_delete=models.CASCADE)
    has_edit_perm = models.BooleanField(default=True)


class Country(models.Model):
    country = models.CharField(_('country'), max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __str__(self):
        return self.country


class City(models.Model):
    city = models.CharField(_('city'), max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')

    def __str__(self):
        return self.city


class Tag(models.Model):
    tag = models.CharField(_('Tag Name'), max_length=20, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.tag


class Description(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    content = models.TextField(_('what would you like to do?'), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name = _('description')
        verbose_name_plural = _('descriptions')
        ordering = ('content',)

    def __str__(self):
        return self.content


class Days(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    day_from = models.DateField()
    day_to = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
