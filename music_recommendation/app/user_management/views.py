import json
import uuid
from json import JSONEncoder
from uuid import UUID

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render

from .models import Artist, Playlist, Song, Users
from app.recommender_collaborative.views import SVD


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def registerPage(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            # Check if the username already exists in the Users model
            if Users.objects.filter(username=username).exists():
                messages.error(request, 'Username "%s" is already in use.' % username)
                return render(request, "register.html", {"form": form})

            # Write the new user's account information to the Users model
            user_id = str(uuid.uuid4())
            print(user_id)
            user = Users.objects.create(
                user_id=user_id, username=username, password=password
            )
            user.save()
            print('User "%s" created' % username)
            messages.success(request, "Registration successed. Please login.")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def loginPage(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = Users.objects.get(username=username, password=password)
        except Users.DoesNotExist:
            user = None

        if user is not None:
            request.session["username"] = user.username
            request.session["user_id"] = str(user.user_id)

            playlist_query = Playlist.objects.filter(user_id=request.session["user_id"])

            playlist_info = []
            for playlist_entry in playlist_query:
                song = Song.objects.get(song_id=playlist_entry.song_id)
                artist = Artist.objects.get(artist_id=song.artist_id)
                playlist_info.append(
                    {
                        "song_title": song.title,
                        "artist_name": artist.artist_name,
                        "year": song.year,
                    }
                )
            request.session["user_playlist"] = playlist_info

            if request.session["user_playlist"]:             
                SVD(request)
                #request.session["svd"] =['a0c7d5ef-3fb7-4c2f-96cc-a509518018b5', 'b0384c14-fa01-4b13-a531-bb8320377d68', '60e4aca8-68bc-4401-badb-90b7cba70fa3', 'e0fd1c5e-c757-4e80-9093-8df2c9d9a6f5', 'e039a386-f237-4deb-9abb-5471c89e7d73']
                
            messages.success(request, "Login successed.")
            
            return redirect("home")

        messages.error(request, "Invalid username or password.")
        return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    if "username" in request.session:
        request.session.flush()
        print("flush")  
        messages.success(request, "Logout successed.")
    return redirect("home")
