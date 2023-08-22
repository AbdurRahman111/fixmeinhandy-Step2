from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Auftrag(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    email = models.EmailField()
    vorname = models.CharField(max_length=30)
    nachname = models.CharField(max_length=30)
    geburtsdatum = models.CharField(max_length=10, null=True, blank=True)
    # ort = models.CharField(max_length=30)
    Adresszeile = models.CharField(max_length=50)
    Hausnummer = models.CharField(max_length=50, default='')
    Stadt = models.CharField(max_length=50, default='')
    Postleitzahl = models.IntegerField()
    handy = models.CharField(max_length=30, null=True, blank=True)
    # schaden = models.CharField(max_length=30)
    marke = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    Schadensart = models.CharField(max_length=30)
    kosten = models.FloatField(blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)
    # PDF_label = models.FileField(upload_to='Auftrag_Pdf/', default=None, null=True, blank=True)
    status = (
        ("Processing", "Processing"),
        ("Complete", "Complete"),
    )
    Auftrag_status = models.CharField(max_length=20, choices=status, default="Processing")
    Zeit = models.DateField(default=datetime.now)

    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

class AuftragPdfResponseApi(models.Model):
    Auftrag = models.OneToOneField(Auftrag, on_delete=models.CASCADE)
    response = models.TextField()