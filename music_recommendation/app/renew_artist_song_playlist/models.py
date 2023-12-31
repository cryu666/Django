from django.db import models

# Create your models here.


class Users(models.Model):
    user_id = models.UUIDField(db_column="User_ID", primary_key=True)
    username = models.CharField(db_column="Username", blank=True, null=True)
    password = models.CharField(db_column="Password", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "USERS"


class Artist(models.Model):
    artist_id = models.UUIDField(db_column="Artist_ID", primary_key=True)
    artist_name = models.CharField(db_column="Artist_Name", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ARTIST"


class Song(models.Model):
    song_id = models.UUIDField(db_column="Song_ID", primary_key=True)
    artist_id = models.UUIDField(db_column="Artist_ID")
    title = models.CharField(db_column="Title", blank=True, null=True)
    year = models.CharField(db_column="Year", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "SONG"


class Playlist(models.Model):
    record_id = models.UUIDField(db_column="Record_ID", primary_key=True)
    playlist_id = models.UUIDField(db_column="Playlist_ID")
    song_id = models.UUIDField(db_column="Song_ID")
    user_id = models.UUIDField(db_column="User_ID")
    listen_count = models.CharField(db_column="Listen_Count", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "PLAYLIST"
