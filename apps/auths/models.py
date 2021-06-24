from django.db import models


class User(models.Model):
    sub = models.CharField(max_length=100)
    name = models.CharField(max_length=300)
    email = models.EmailField(null=False)
    picture = models.URLField()

    id = models.AutoField(primary_key = True)
    token = models.CharField()
    refresh_token = models.CharField()

