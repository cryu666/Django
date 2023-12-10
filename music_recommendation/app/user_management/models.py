from django.db import models

# Create your models here.


class Users(models.Model):
    user_id = models.UUIDField(db_column="User_ID", primary_key=True)
    username = models.CharField(db_column="Username", blank=True, null=True)
    password = models.CharField(db_column="Password", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "USERS"


class Playlist(models.Model):
    playlist_id = models.UUIDField(db_column='Playlist_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('Users', models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
    song = models.ForeignKey('Song', models.DO_NOTHING, db_column='Song_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PLAYLIST'

class Artist(models.Model):
    artist_id = models.UUIDField(db_column='Artist_ID', primary_key=True)  # Field name made lowercase.
    artist_name = models.CharField(db_column='Artist_Name')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ARTIST'

class Song(models.Model):
    song_id = models.UUIDField(db_column='Song_ID', primary_key=True)  # Field name made lowercase.
    artist = models.ForeignKey(Artist, models.DO_NOTHING, db_column='Artist_ID')  # Field name made lowercase.
    title = models.CharField(db_column='Title')  # Field name made lowercase.
    listen_count = models.IntegerField(db_column='Listen_Count')  # Field name made lowercase.
    year = models.CharField(db_column='Year')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SONG'


