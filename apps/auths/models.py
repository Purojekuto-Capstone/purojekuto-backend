from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    sub = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300)
    email = models.EmailField(null=False)
    picture = models.URLField()

    credentials = models.JSONField()
