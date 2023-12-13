import json
import uuid
from json import JSONEncoder
from uuid import UUID

# # Create your views here.
# from django.contrib.auth.forms import AddSongForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Users, Artist, Song, Playlist

def add_song(request):
    if request.method == 'POST':
        song_name = request.POST.get('song_name')
        artist_name = request.POST.get('artist_name')
        date = request.POST.get('song_date')
        year = int(date.split("-")[0])

        username = request.session.get('username', None)
        user = Users.objects.get(username=username)
        user_id = user.user_id
        print(song_name)
        print(artist_name)
        print(year)

        # 更新藝人資料庫
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
            
        # 更新歌曲資料庫
        try:
            song = Song.objects.get(artist_id=artist_id, title=song_name)
            song_id = song.song_id
            print("Song is found, skip creating")
        except Song.DoesNotExist: 
            print("Song is not found, creating a new song info")
            song_id = str(uuid.uuid4())
            song = Song.objects.create(artist_id=artist_id, title=song_name, song_id=song_id, year=year)
            song.save()

        try:
            # Does the playlist exist? Which means whether user listend to any song.
            playlist = Playlist.objects.filter(user_id=user_id).first()
            playlist_id = playlist.playlist_id
            try:
                playlist = Playlist.objects.get(song_id=song_id, user_id=user_id)
                playlist.listen_count += 1
                playlist.save()
                print("1 User listened to this song before, just add listen count")
            except Playlist.DoesNotExist:
                print("2 User do have playlist, but doesn't listen to this song before")
                record_id = str(uuid.uuid4())
                listen_count = 1
                playlist = Playlist.objects.create(record_id=record_id, playlist_id=playlist_id, user_id=user_id, song_id=song_id, listen_count=listen_count)
                playlist.save()
        except Playlist.DoesNotExist: 
            print("3 User never listened to any song before, so we need to create a new playlist")
            playlist_id = str(uuid.uuid4())
            record_id = str(uuid.uuid4())
            listen_count = 1
            playlist = Playlist.objects.create(record_id=record_id, playlist_id=playlist_id, user_id=user_id, song_id=song_id, listen_count=listen_count)
            playlist.save()

        playlist_query = Playlist.objects.filter(user_id=user_id)
        playlist_info = []
        for playlist_entry in playlist_query:
            song = Song.objects.get(song_id=playlist_entry.song_id) 
            artist = Artist.objects.get(artist_id=song.artist_id)
            playlist_info.append({
                'song_title': song.title,
                'artist_name': artist.artist_name,
                'year': song.year,
            })
        request.session['user_playlist'] = playlist_info 

        return redirect("search")
    # return render(request, "search.html")
    return redirect("search")
