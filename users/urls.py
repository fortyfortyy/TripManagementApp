from django.urls import path
from users import views as ex_views

urlpatterns = [
    path('<str:pk>', ex_views.UserView.as_view(), name='user-profile'),
    path('register/', ex_views.RegisterView.as_view(), name='register'),
    path('login/', ex_views.LoginView.as_view(), name='login'),
    path('logout/', ex_views.LogoutView.as_view(), name='logout'),
]
