from django.db import models

# Create your models here.

class UserBasedDataset(models.Model):
    user_id = models.CharField(primary_key=True, blank=True)
    song_id = models.CharField(blank=True, null=True)
    listen_count = models.IntegerField(blank=True, null=True)
    title = models.CharField(blank=True, null=True)
    release = models.CharField(blank=True, null=True)
    artist_name = models.CharField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_based_dataset'