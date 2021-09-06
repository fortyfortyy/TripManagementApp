from django.urls import path
from trips import views as ex_views

urlpatterns = [
    path('', ex_views.TripsView.as_view(), name='trips'),
    path('trip/<str:pk>', ex_views.TripDetailsView.as_view(), name='trip'),
    path('trip-create/', ex_views.TripCreate.as_view(), name='trip-create-form'),
]
