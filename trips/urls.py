from django.urls import path
from trips import views as ex_views

urlpatterns = [
    path('', ex_views.TripPlansView.as_view(), name='trip-plans'),
    path('trip-plan/create', ex_views.TripPlanCreateView.as_view(), name='create-trip-plan'),
    path('trip-plan/<str:pk>', ex_views.TripPlanDetailsView.as_view(), name='trip-plan-details'),
    path('trip-plan/edit/<str:pk>', ex_views.TripPlanEditView.as_view(), name='edit-trip-plan'),
    path('trip-plan/delete/<str:pk>', ex_views.TripPlanDeleteView.as_view(), name='delete-trip-plan'),


    path('trip/create/<str:pk>', ex_views.TripCreateView.as_view(), name='create-trip'),
    path('trip/<str:pk>', ex_views.TripDetailsView.as_view(), name='trip-details'),
    path('trip/edit/<str:pk>', ex_views.TripEditView.as_view(), name='edit-trip'),
    path('trip/delete/<str:pk>', ex_views.TripDeleteView.as_view(), name='delete-trip'),
]
