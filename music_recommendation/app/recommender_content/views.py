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
        request.session["string"] = input_string
    tracks = search_song(request.session["string"])
    return render(request, "search.html", {"tracks": tracks})


def songs(request):
    if request.method == "POST":
        name = request.POST["song_name"]
        date = request.POST["song_date"]
        year = int(date.split("-")[0])
        request.session["name"] = name
        request.session["year"] = year

    songs = recommend_songs(
        [{"name": request.session["name"], "year": request.session["year"]}],
        spotify_data,
    )

    # Iterate through each song and modify the 'artists' key
    for song in songs:
        # Extracting the artist names from the string representation of the list
        artists_str = song["artists"][1:-1]  # Removing the square brackets
        artists_list = [artist.strip()[1:-1] for artist in artists_str.split(",")]

        # Joining the artist names into a comma-separated string
        artists_display = ", ".join(artists_list)

        # Update the 'artists' key in the dictionary
        song["artists"] = artists_display

    context = {
        "search": request.session["name"],
        "songs": songs,
    }

    return render(request, "content_based.html", context)


def upload_img(request):
    if request.method == "POST":
        uploaded_image = request.FILES.get("image")
        if uploaded_image is None:
            return render(
                request, "mainpage.html", {"message": "Please select an image."}
            )

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

            # Iterate through each song and modify the 'artists' key
            for song in songs:
                # Extracting the artist names from the string representation of the list
                artists_str = song["artists"][1:-1]  # Removing the square brackets
                artists_list = [
                    artist.strip()[1:-1] for artist in artists_str.split(",")
                ]

                # Joining the artist names into a comma-separated string
                artists_display = ", ".join(artists_list)

                # Update the 'artists' key in the dictionary
                song["artists"] = artists_display

            context = {"mood": mood, "songs": songs}

            return render(request, "emotion_playlist.html", context)
        except:
            return render(
                request,
                "mainpage.html",
                {"message": "Please upload a clear personal photo of your face."},
            )

        finally:
            if os.path.exists(settings.STATICFILES_DIRS[0] + "/images/" + filename):
                os.remove(settings.STATICFILES_DIRS[0] + "/images/" + filename)

    return render(request, "mainpage.html")
