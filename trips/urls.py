from django.urls import path
from trips import views as ex_views

urlpatterns = [
    path('', ex_views.TripPlansView.as_view(), name='trip-plans'),
    path('create-trip-plan/', ex_views.TripPlanCreateView.as_view(), name='create-trip-plan'),
    path('trip-plan/<str:pk>', ex_views.TripPlanDetailsView.as_view(), name='trip-plan-details'),
    path('edit-trip-plan/<str:pk>', ex_views.TripPlanEditView.as_view(), name='edit-trip-plan'),
    # path('delete-trip-plan/<str:pk>', ex_views.TripPlanDeleteView.as_view(), name='delete-trip-plan'),


    path('create-trip/<str:pk>', ex_views.TripCreateView.as_view(), name='create-trip'),
    path('trip/<str:pk>', ex_views.TripDetailsView.as_view(), name='trip-details'),
    path('edit-trip/<str:pk>', ex_views.TripEditView.as_view(), name='edit-trip'),
    path('delete-trip/<str:pk>', ex_views.TripDeleteView.as_view(), name='delete-trip'),
]
