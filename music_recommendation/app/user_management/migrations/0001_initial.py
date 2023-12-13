# Generated by Django 4.2.7 on 2023-12-09 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "artist_id",
                    models.UUIDField(
                        db_column="Artist_ID", primary_key=True, serialize=False
                    ),
                ),
                ("artist_name", models.CharField(db_column="Artist_Name")),
            ],
            options={"db_table": "ARTIST", "managed": False,},
        ),
        migrations.CreateModel(
            name="Playlist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("playlist_id", models.UUIDField(db_column="Playlist_ID")),
            ],
            options={"db_table": "PLAYLIST", "managed": False,},
        ),
        migrations.CreateModel(
            name="Song",
            fields=[
                (
                    "song_id",
                    models.UUIDField(
                        db_column="Song_ID", primary_key=True, serialize=False
                    ),
                ),
                ("title", models.CharField(db_column="Title")),
                ("listen_count", models.IntegerField(db_column="Listen_Count")),
                ("year", models.CharField(db_column="Year")),
            ],
            options={"db_table": "SONG", "managed": False,},
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                (
                    "user_id",
                    models.UUIDField(
                        db_column="User_ID", primary_key=True, serialize=False
                    ),
                ),
                (
                    "username",
                    models.CharField(blank=True, db_column="Username", null=True),
                ),
                (
                    "password",
                    models.CharField(blank=True, db_column="Password", null=True),
                ),
            ],
            options={"db_table": "USERS", "managed": False,},
        ),
    ]
