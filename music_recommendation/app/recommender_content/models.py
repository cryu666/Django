# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ContentBasedSongGenres(models.Model):
    valence = models.FloatField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    acousticness = models.FloatField(blank=True, null=True)
    artists = models.CharField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    duration_ms = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    explicit = models.IntegerField(blank=True, null=True)
    id = models.CharField(primary_key=True)
    instrumentalness = models.FloatField(blank=True, null=True)
    key = models.IntegerField(blank=True, null=True)
    liveness = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    mode = models.IntegerField(blank=True, null=True)
    name = models.CharField(blank=True, null=True)
    popularity = models.IntegerField(blank=True, null=True)
    release_date = models.CharField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_based_song_genres'


class ContentBasedStyleGenres(models.Model):
    mode = models.IntegerField(blank=True, null=True)
    genres = models.CharField(primary_key=True)
    acousticness = models.FloatField(blank=True, null=True)
    danceability = models.FloatField(blank=True, null=True)
    duration_ms = models.FloatField(blank=True, null=True)
    energy = models.FloatField(blank=True, null=True)
    instrumentalness = models.FloatField(blank=True, null=True)
    liveness = models.FloatField(blank=True, null=True)
    loudness = models.FloatField(blank=True, null=True)
    speechiness = models.FloatField(blank=True, null=True)
    tempo = models.FloatField(blank=True, null=True)
    valence = models.FloatField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    key = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'content_based_style_genres'
        db_table_comment = '音樂屬性'
