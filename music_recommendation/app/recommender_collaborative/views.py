import datetime

import numpy as np
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django_pandas.io import read_frame
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split

from .model.knn_recommender import KNNRecommender
from .model.svd_recommender import SVDRecommender
from .models import Artist, Playlist, Song
import asyncio
import logging

# Create your views here.

playlist = Playlist.objects.all()
song_info = Song.objects.all()
artist_info = Artist.objects.all()

df_playlist = read_frame(playlist)
df_song_info = read_frame(song_info)
df_artist_info = read_frame(artist_info)

# df_playlist.to_csv('df_playlist.csv')

df_playlist = df_playlist[["user", "song", "listen_count"]]
df_song_info = df_song_info[["song_id", "title", "artist_id", "year"]]

# df_playlist[['user', 'song']] = df_playlist[['user', 'song']].astype("string")
# df_playlist['song'] = df_playlist['song'].str.extract(r"\((.*?)\)" , expand=False)

df_playlist_actual = df_playlist.drop_duplicates(subset=["song", "user"], keep=False)

df_tmp = pd.merge(
    df_playlist_actual, df_song_info, left_on="song", right_on="song_id", how="left"
)
df_tmp.drop(columns=["song_id"])

df_songs = pd.merge(
    df_tmp, df_artist_info, left_on="artist_id", right_on="artist_id", how="left"
)
df_songs = df_songs[["user", "song", "title", "artist_name", "listen_count", "year"]]
df_songs[["user", "song", "title", "artist_name"]] = df_songs[
    ["user", "song", "title", "artist_name"]
].astype("string")
# df_songs.to_csv("df_songs.csv")


def KNN(request):
    df_song_id_reduced = df_songs.reset_index(drop=True)

    # convert the dataframe into a pivot table
    df_songs_features = df_song_id_reduced.pivot(
        index="song", columns="user", values="listen_count"
    ).fillna(0)

    # obtain a sparse matrix
    mat_songs_features = csr_matrix(df_songs_features.values)

    df_unique_songs = df_songs.drop_duplicates(subset=["song"]).reset_index(drop=True)[
        ["song", "title"]
    ]

    decode_id_song = {
        song: i
        for i, song in enumerate(
            list(df_unique_songs.set_index("song").loc[df_songs_features.index].title)
        )
    }

    model = KNNRecommender(
        metric="cosine",
        algorithm="brute",
        k=20,
        data=mat_songs_features,
        decode_id_song=decode_id_song,
    )

    if request.method == "POST":
        song = request.POST.get("song_input")
        request.session["song"] = song

    knn_recommendation = model.make_recommendation(
        new_song=request.session["song"], n_recommendations=10
    )

    recommended_artists = []
    recommended_years = []

    for recommended_song in knn_recommendation:
        song_info = df_songs[df_songs["title"] == recommended_song].iloc[0]
        recommended_artists.append(song_info["artist_name"])
        recommended_years.append(song_info["year"])

    context = {
        "song": request.session["song"],
        "knn_recommendation": zip(
            knn_recommendation, recommended_artists, recommended_years
        ),
    }

    return render(request, "knn.html", context)  # type(context) should be dict


def SVD(request):
    df_songs_reduced = df_songs.reset_index(drop=True)[["song", "user", "listen_count"]]
    df_songs_reduced["listen_count"] = 1

    svd = SVDRecommender(no_of_features=8)

    train, test = train_test_split(df_songs_reduced)
    print("Split...")

    # Creates the user-item matrix, the user_id on the rows and the song_id on the columns.
    user_item_matrix, users, items = svd.create_utility_matrix(
        train,
        formatizer={"user": "user", "item": "song", "value": "listen_count"},
    )
    print("Create matrix...")

    # fits the svd model to the matrix data.
    svd.fit(user_item_matrix, users, items)
    print("Fit...")

    # outputs N most similar users to user with user_id x
    print(f"user id: {request.session['user_id']}")
    userId = request.session["user_id"]
    svd_recommendation = svd.topN_similar(x=userId, N=5, column="user")
    print("svd recommendation...")
    print(svd_recommendation)
    request.session["svd"] = svd_recommendation

    return render(request, "mainpage.html")

def SVD_playlist(request):      
    if request.method == "POST":
        similar_user = request.POST.get("similar_user")

        playlist_query = Playlist.objects.filter(user=similar_user)

        playlist_info = []
        for playlist_entry in playlist_query:
            song = Song.objects.get(song_id=playlist_entry.song)
            artist = Artist.objects.get(artist_id=song.artist_id)
            playlist_info.append(
                {
                    "song": song.title,
                    "artist": artist.artist_name,
                    "year": song.year,
                }
            )
        similar_user_playlist = playlist_info

    print(f"similar_user_playlist: {similar_user_playlist}")
    context = {
        "similar_user": similar_user,
        "recommendation_playlist": similar_user_playlist
    }

    return render(request, "temp.html", context)

