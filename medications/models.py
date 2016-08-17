from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Doctors(models.Model):
    doc_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    expiration = models.DateTimeField()

class Patients(models.Model):
    patient_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    primary_doc = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    cell_phone = models.CharField(max_length=15)
    email = models.CharField(max_length=50)

class Medications(models.Model):
    name = models.CharField(max_length=100)
    patient_id = models.ForeignKey(Patients, on_delete=models.CASCADE)
    number_refills = models.IntegerField()
