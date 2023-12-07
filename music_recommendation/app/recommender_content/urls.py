from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("content_based/", views.songs, name="songs"),
    path("upload_img/", views.upload_img, name="upload_img"),
    path("emotion_playist/", views.upload_img, name="emo"),
    path("search/", views.search, name="search"),
]
