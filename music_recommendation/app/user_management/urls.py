from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
