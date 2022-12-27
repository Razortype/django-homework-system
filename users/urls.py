from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('profile', views.Profile.as_view(), name="user profile"),

    path('login', views.LoginView.as_view(), name="login"),
    path('logout', views.LogoutView.as_view(), name="logout"),
]