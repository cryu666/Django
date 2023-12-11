from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path("add_song/", views.add_song, name="add_song"),
]
