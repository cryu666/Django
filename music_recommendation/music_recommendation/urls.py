"""
URL configuration for music_recommendation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from app.recommender_collaborative import views as views_coll

# from app.recommender_content import views as views_con
# from app.user_management import views as views_user


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path("knn/", views_coll.KNN, name="knn"),
    path("temp/", views_coll.SVD_playlist, name="temp"),
    path("", include("app.recommender_content.urls")),
    path("", include("app.user_management.urls")),
    path("", include("app.renew_artist_song_playlist.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
