from django.urls import path
from . import views

from django.conf import settings


urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logout_view, name='logout'),
    
]

