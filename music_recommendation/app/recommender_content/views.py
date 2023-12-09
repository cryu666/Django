import json
import os

import cv2
from deepface import DeepFace
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

# Create your views here.
from .recommender.file import recommend_songs, search_song, spotify_data


# Create your views here.
def home(request):
    return render(request, "mainpage.html")


def search(request):
    tracks = []
    if request.method == "POST":
        input_string = request.POST["string"]
        tracks = search_song(input_string)
    return render(request, "search.html", {"tracks": tracks})


def songs(request):
    if request.method == "POST":
        name = request.POST["song_name"]
        date = request.POST["song_date"]
        year = int(date.split("-")[0])
        songs = recommend_songs([{"name": name, "year": year}], spotify_data)
        context = {
            "search": name,
            "songs": songs,
        }
    return render(request, "content_based.html", context)


def upload_img(request):
    if request.method == "POST" and request.FILES["image"]:
        uploaded_image = request.FILES["image"]
        fs = FileSystemStorage(location=settings.STATICFILES_DIRS[0] + "/images")
        filename = fs.save(uploaded_image.name, uploaded_image)
        image_url = settings.STATIC_URL + "images/" + filename
        img = cv2.imread(settings.STATICFILES_DIRS[0] + "/images/" + filename)
        emo_recom_dict = {
            "angry": {"name": "Believer", "year": 2017},
            "disgust": {"name": "I Hate Everything About You", "year": 2003},
            "fear": {"name": "FEARLESS", "year": 2022},
            "happy": {"name": "Die Young", "year": 2012},
            "sad": {"name": "Lonely (with benny blanco)", "year": 2020},
            "surprise": {"name": "Wow.", "year": 2019},
            "neutral": {"name": "Not Angry", "year": 2020},
        }
        try:
            emotion = DeepFace.analyze(img, actions=["emotion"])
            mood = emotion[0]["dominant_emotion"][:]
            songs = recommend_songs([emo_recom_dict[mood]], spotify_data)
            context = {"mood": mood, "songs": songs}
            return render(request, "emotion_playlist.html", context)
        except:
            pass

        finally:
            if os.path.exists(settings.STATICFILES_DIRS[0] + "/images/" + filename):
                os.remove(settings.STATICFILES_DIRS[0] + "/images/" + filename)

    return render(request, "mainpage.html")
