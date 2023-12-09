import json
import uuid
from json import JSONEncoder
from uuid import UUID

# # Create your views here.
# from django.contrib.auth.forms import AddSongForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Artist, Song

def add_song(request):
    if request.method == 'POST':
        song_name = request.POST.get('song_name')
        artist_name = request.POST.get('artist_name')

        print(song_name)
        print(artist_name)

        try:
            artist = Artist.objects.get(artist_name=artist_name)
            artist_id = artist.artist_id
            print("Artist is found, skip creating")
        except Artist.DoesNotExist:
            print("Artist is not found, creating a new artist info")
            artist_id = str(uuid.uuid4())
            # print(artist_id, artist_name)
            artist = Artist.objects.create(artist_name=artist_name, artist_id=artist_id)
            artist.save()

        try:
            song = Song.objects.get(artist_id_song=artist_id, title=song_name)
            song_id = song.song_id
            print("Song is found, skip creating")
        except Song.DoesNotExist: 
            print("Song is not found, creating a new song info")
            song_id = str(uuid.uuid4())
            listen_count = 1
            year = 0
            song = Song.objects.create(artist_id_song=artist_id, title=song_name, song_id=song_id, year=year, listen_count=listen_count)
            song.save()
        print(f"Song_id:{song_id}, Artist_id:{artist_id}, Title:{song_name}")
        
        
        return redirect("search")

    # return render(request, "search.html")
    return redirect("search")
