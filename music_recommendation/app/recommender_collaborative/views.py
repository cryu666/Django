import datetime

import numpy as np
import pandas as pd
from app.recommender_collaborative.model.recommender import Recommender
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django_pandas.io import read_frame
from scipy.sparse import csr_matrix

from .models import UserBasedDataset

# Create your views here.


def index(request):
    songs = UserBasedDataset.objects.all()
    df_songs = read_frame(songs)

    # Filtered the dataset to keep only those users which have listened to at least 16 songs
    song_user = df_songs.groupby("user_id")["song_id"].count()
    song_ten_id = song_user[song_user > 16].index.to_list()
    df_song_id_more_ten = df_songs[df_songs["user_id"].isin(song_ten_id)].reset_index(
        drop=True
    )

    # convert the dataframe into a pivot table
    df_songs_features = df_song_id_more_ten.pivot(
        index="song_id", columns="user_id", values="listen_count"
    ).fillna(0)

    # obtain a sparse matrix
    mat_songs_features = csr_matrix(df_songs_features.values)

    df_unique_songs = df_songs.drop_duplicates(subset=["song_id"]).reset_index(
        drop=True
    )[["song_id", "title"]]

    decode_id_song = {
        song: i
        for i, song in enumerate(
            list(
                df_unique_songs.set_index("song_id").loc[df_songs_features.index].title
            )
        )
    }

    model = Recommender(
        metric="cosine",
        algorithm="brute",
        k=20,
        data=mat_songs_features,
        decode_id_song=decode_id_song,
    )
    song = request.POST.get("song_input", "I believe in miracles")  # !!!!!!!!!
    print(song)
    new_recommendation = model.make_recommendation(new_song=song, n_recommendations=10)

    context = {"new_recommendation": new_recommendation}

    return render(request, "knn_test.html", context)  # type(context) should be dict
