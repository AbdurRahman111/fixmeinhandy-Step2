from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from datetime import datetime



class User_Profile(models.Model):
    class Meta:
        verbose_name_plural = 'User Profile'
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=255, null=True, blank=True)
    geburtsdatum = models.CharField(max_length=10, null=True, blank=True)
    ort = models.CharField(max_length=30, null=True, blank=True)
    Adresszeile = models.CharField(max_length=50, null=True, blank=True)
    Hausnummer = models.CharField(max_length=50, default='', null=True, blank=True)
    Stadt = models.CharField(max_length=50, default='', null=True, blank=True)
    Postleitzahl = models.IntegerField(null=True, blank=True)

