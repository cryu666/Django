from django.db import models

# Create your models here.


class Users(models.Model):
    user_id = models.UUIDField(db_column="User_ID", primary_key=True)
    username = models.CharField(db_column="Username", blank=True, null=True)
    email = models.CharField(db_column="Email", blank=True, null=True)
    password = models.CharField(db_column="Password", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "USERS"
