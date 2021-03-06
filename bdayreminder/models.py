from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Doctor(models.Model):
    username = models.CharField(max_length=100)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    expiration = models.DateTimeField()
