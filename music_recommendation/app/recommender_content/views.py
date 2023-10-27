from django.shortcuts import render


# Create your views here.
from .recommender.file import recommend_songs ,spotify_data, search_song

from django.core.files.storage import FileSystemStorage
from django.conf import settings

import os

import cv2
from deepface import DeepFace

import json

# Create your views here.
def home(request):
    return render(request, 'mainpage.html')

def search(request):
    if request.method == 'POST':
        input_string = request.POST['string']
        tracks = search_song(input_string)
    return render(request, 'search.html', {"tracks": tracks})

def songs(request):
    if request.method == 'POST':
        name = request.POST['song_name']
        date = request.POST['song_date']
        year = int(date.split('-')[0])
        songs = recommend_songs([{'name': name, 'year': year}], spotify_data)
    return render(request, 'recommend_playlist.html', {"search":name, "songs": songs})
        

def upload_img(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage(location=settings.STATIC_ROOT + '/images')  
        filename = fs.save(uploaded_image.name, uploaded_image)
        image_url = settings.STATIC_URL + 'images/' + filename
        img = cv2.imread(settings.STATIC_ROOT + '/images/' + filename)
        try:
            emotion = DeepFace.analyze(img, actions=['emotion'])  
            if emotion[0]["dominant_emotion"][:] == 'angry':
                mood = 'Angry'
                songs = recommend_songs([{'name':'Believer', 'year': 2017},], spotify_data)
            if emotion[0]["dominant_emotion"][:] == 'disgust':
                mood = 'Disgust'
                songs = recommend_songs([{'name':'I Hate Everything About You', 'year': 2003},
                            ], spotify_data)
            if emotion[0]["dominant_emotion"][:] == 'fear':
                mood = 'Fear'
                songs = recommend_songs([{'name':'FEARLESS', 'year': 2022},
                            ], spotify_data)
            if emotion[0]["dominant_emotion"][:] == 'happy':
                mood = 'Happy'
                songs = recommend_songs([{'name':'Die Young', 'year': 2012},
                            ], spotify_data)
            if emotion[0]["dominant_emotion"][:] == 'sad':
                mood = 'Sad'
                songs = recommend_songs([{'name':'Lonely (with benny blanco)', 'year': 2020},
                            ], spotify_data)
            if emotion[0]["dominant_emotion"][:] == 'surprise':
                mood = 'Surprise'
                songs = recommend_songs([{'name':'Wow.', 'year': 2019},
                            ], spotify_data)
            if emotion[0]["dominant_emotion"][:] == 'neutral':
                mood = 'Neutral'
                songs = recommend_songs([{'name':'Not Angry', 'year': 2020},
                            ], spotify_data)
            return render(request, 'emotion_playlist.html', {'image_url': image_url, 'mood': mood, 'songs': songs})
        except:
            pass

        finally:
            if os.path.exists(settings.STATIC_ROOT + '/images/' + filename):
                os.remove(settings.STATIC_ROOT + '/images/' + filename)
    return render(request, 'mainpage.html')





