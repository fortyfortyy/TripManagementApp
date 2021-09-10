from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import Profile

from dynamic_filenames import FilePattern
from stdimage import StdImageField, JPEGField

import uuid

# Create your models here.


# https://github.com/codingjoe/django-dynamic-filenames
# https://github.com/codingjoe/django-stdimage

def get_trip_image_filepath(self, filename):
    return f'trips/{str(self.pk)}/{filename}'


class Trip(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(_('Trip Name'), max_length=200, unique=True)
    day_from = models.DateField()
    day_to = models.DateField()

    # creates a thumbnail resized to maximum size to fit a 100x75 area
    trip_images = models.ImageField(
        max_length=255, blank=True, null=True, upload_to=get_trip_image_filepath, default="")
    countries = models.ManyToManyField('Country', related_name='countries')
    cities = models.ManyToManyField('City', related_name='cities')
    tags = models.ManyToManyField('Tag', related_name='tags')
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    is_private = models.BooleanField(default=True)

    members = models.ManyToManyField(Profile, related_name='trip_members', through='TripGroup')

    def __str__(self):
        return self.name

    @property
    def descriptions(self):
        queryset = self.description_set.all().values_list('content', flat=True)
        # queryset = self.description_set.all().values_list('content')
        return queryset


class TripGroup(models.Model):
    """
    Możliwość dodawania uprawnień dla osób dodanych do wycieczki
    """
    trips = models.ForeignKey(Trip, on_delete=models.CASCADE)
    profiles = models.ForeignKey(Profile, on_delete=models.CASCADE)
    has_edit_perm = models.BooleanField(default=True)


class Country(models.Model):
    country = models.CharField(_('country'), max_length=50, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.country


class City(models.Model):
    city = models.CharField(_('city'), max_length=50, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.city


class Tag(models.Model):
    tag = models.CharField(_('tag name'), max_length=30, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.tag


class Description(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    content = models.TextField(_('description'), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.content
