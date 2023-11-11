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
from .models import UserBasedDataset

# Create your views here.

songs = UserBasedDataset.objects.all()
df_songs = read_frame(songs)

# Filter users which have listen to at least 20 songs
user_counts = df_songs.groupby("user_id")["song_id"].count()
user_id_reduced = user_counts[user_counts > 20].index.to_list()

# Get songs which have been listened at least 20 times
song_counts = df_songs.groupby("song_id")["user_id"].count()
song_id_reduced = song_counts[song_counts > 20].index.to_list()


def KNN(request):

    df_song_id_reduced = df_songs[
        df_songs["user_id"].isin(user_id_reduced)
    ].reset_index(drop=True)

    # convert the dataframe into a pivot table
    df_songs_features = df_song_id_reduced.pivot(
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

    model = KNNRecommender(
        metric="cosine",
        algorithm="brute",
        k=20,
        data=mat_songs_features,
        decode_id_song=decode_id_song,
    )
    song = request.POST.get("song_input", "I believe in miracles")  # !!!!!!!!!
    knn_recommendation = model.make_recommendation(new_song=song, n_recommendations=10)

    context = {
        "knn_recommendation": knn_recommendation,
    }

    return render(request, "knn.html", context)  # type(context) should be dict


def SVD(request):

    df_songs_reduced = df_songs[
        (df_songs["user_id"].isin(user_id_reduced))
        & (df_songs["song_id"].isin(song_id_reduced))
    ].reset_index(drop=True)[["user_id", "song_id", "listen_count"]]
    df_songs_reduced["listen_count"] = 1

    svd = SVDRecommender(no_of_features=8)

    train, test = train_test_split(df_songs_reduced)

    # Creates the user-item matrix, the user_id on the rows and the song_id on the columns.
    user_item_matrix, users, items = svd.create_utility_matrix(
        train,
        formatizer={"user": "user_id", "item": "song_id", "value": "listen_count"},
    )

    # fits the svd model to the matrix data.
    svd.fit(user_item_matrix, users, items)

    # outputs N most similar users to user with user_id x
    userId = request.POST.get(
        "userId_input", "b80344d063b5ccb3212f76538f3d9e43d87dca9e"
    )  # !!!!!!!!!
    svd_recommendation = svd.topN_similar(x=userId, N=5, column="user")

    context = {
        "svd_recommendation": svd_recommendation,
    }

    return render(request, "svd.html", context)
