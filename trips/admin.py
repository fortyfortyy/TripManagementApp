from django.contrib import admin
from .models import TripPlan, Trip, City, Tag, Description, TripPlanGroup, Country, Days

# Register your models here.
admin.site.register(TripPlan)
admin.site.register(Trip)
admin.site.register(City)
admin.site.register(Tag)
admin.site.register(Description)
admin.site.register(TripPlanGroup)
admin.site.register(Country)
admin.site.register(Days)
