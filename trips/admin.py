from django.contrib import admin
from .models import Trip, City, Tag, Description, TripGroup, Country

# Register your models here.
admin.site.register(Trip)
admin.site.register(City)
admin.site.register(Tag)
admin.site.register(Description)
admin.site.register(TripGroup)
admin.site.register(Country)
