from django.db import models
# Create your models here.


class Artist(models.Model):
    artist_id = models.UUIDField(db_column="Artist_ID", primary_key=True)
    artist_name = models.CharField(db_column="Artist_Name", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ARTIST"

class Song(models.Model):
    song_id = models.UUIDField(db_column="Song_ID", primary_key=True)
    artist_id_song = models.UUIDField(db_column="Artist_ID")
    title = models.CharField(db_column="Title", blank=True, null=True)
    listen_count = models.IntegerField(db_column="Listen_Count", blank=True, null=True)
    year = models.CharField(db_column="Year", blank=True, null=True)
    class Meta:
        managed = False
        db_table = "SONG"