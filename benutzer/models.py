from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


class MarkeTable(models.Model):
    class Meta:
        verbose_name_plural = 'Marke Table'
    Serial_Number = models.IntegerField(default=0)
    Name = models.CharField(max_length=255)
    def __str__(self):
        return self.Name


class ModelTable(models.Model):
    class Meta:
        verbose_name_plural = 'Model Table'
    Serial_Number = models.IntegerField(default=0)
    Marke = models.ForeignKey(MarkeTable, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)

    def __str__(self):
        return self.Name


class SchadensartTable(models.Model):
    class Meta:
        verbose_name_plural = 'Schadensart Table'
    Serial_Number = models.IntegerField(default=0)
    Marke = models.ForeignKey(MarkeTable, on_delete=models.CASCADE, default=None)
    Model = models.ForeignKey(ModelTable, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    Price = models.FloatField()

    def __str__(self):
        return self.Name


class Auftrag(models.Model):
    serial_number = models.CharField(max_length=255, blank=True, null=True, default='')
    sequence_number = models.CharField(max_length=255, blank=True, null=True, default='')
    User = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    email = models.EmailField()
    vorname = models.CharField(max_length=30)
    nachname = models.CharField(max_length=30)
    geburtsdatum = models.CharField(max_length=10, null=True, blank=True)
    # ort = models.CharField(max_length=30)
    Adresszeile = models.TextField()
    StreetName = models.CharField(max_length=255, default='', null=True, blank=True)
    Hausnummer = models.CharField(max_length=255, default='', null=True, blank=True)
    Stadt = models.CharField(max_length=255, default='', null=True, blank=True)
    Postleitzahl = models.IntegerField()
    Country = models.CharField(max_length=255, default='', null=True, blank=True)
    State = models.CharField(max_length=255, default='', null=True, blank=True)
    handy = models.CharField(max_length=30, null=True, blank=True)
    # schaden = models.CharField(max_length=30)
    marke = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    Schadensart = models.TextField()
    screen_protector_status_options = (
        ('yes', 'yes'),
        ('no', 'no'),
    )
    screen_protector_status = models.CharField(max_length=255, choices=screen_protector_status_options, default='no', null=True, blank=True)
    kosten = models.FloatField(blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)
    # PDF_label = models.FileField(upload_to='Auftrag_Pdf/', default=None, null=True, blank=True)
    status = (
        ("New Order", "New Order"),
        ("In Repair", "In Repair"),
        ("Completed", "Completed"),
    )
    Auftrag_status = models.CharField(max_length=20, choices=status, default="New Order")
    Zeit = models.DateField(default=datetime.now)

    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        main_str = str(self.Zeit).replace('-', '')[0:6]
        return str(self.sequence_number)+  " - " + str(self.vorname) +" "+ str(self.nachname) + " - [" + str(self.Auftrag_status)+"]"

    def save(self, *args, **kwargs):
        # Your custom logic here
        if self.Auftrag_status == "Completed":
            # Do something when the object is marked as Completed
            var_Ausgeführter_Befehl = Ausgeführter_Befehl(
                serial_number=self.serial_number,
                sequence_number=self.sequence_number,
                User=self.User,
                email=self.email,
                vorname=self.vorname,
                nachname=self.nachname,
                geburtsdatum=self.geburtsdatum,
                Adresszeile=self.Adresszeile,
                Hausnummer=self.Hausnummer,
                Stadt=self.Stadt,
                Postleitzahl=self.Postleitzahl,
                handy=self.handy,
                marke=self.marke,
                model=self.model,
                Schadensart=self.Schadensart,
                screen_protector_status=self.screen_protector_status,
                kosten=self.kosten,
                telefon=self.telefon,
                Auftrag_status=self.Auftrag_status,
                Zeit=self.Zeit
            )
            var_Ausgeführter_Befehl.save()
            self.delete()
        else:
            super(Auftrag, self).save(*args, **kwargs)


class Ausgeführter_Befehl(models.Model):
    class Meta:
        verbose_name_plural = 'Ausgeführter Befehl'

    serial_number = models.CharField(max_length=255, blank=True, null=True, default='')
    sequence_number = models.CharField(max_length=255, blank=True, null=True, default='')
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
    screen_protector_status_options = (
        ('yes', 'yes'),
        ('no', 'no'),
    )
    screen_protector_status = models.CharField(max_length=255, choices=screen_protector_status_options, default='no', null=True, blank=True)
    kosten = models.FloatField(blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)
    # PDF_label = models.FileField(upload_to='Auftrag_Pdf/', default=None, null=True, blank=True)
    status = (
        ("New Order", "New Order"),
        ("In Repair", "In Repair"),
        ("Completed", "Completed"),
    )
    Auftrag_status = models.CharField(max_length=20, choices=status, default="New Order")
    Zeit = models.DateField(default=datetime.now)

    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        main_str = str(self.Zeit).replace('-', '')[0:6]
        return str(self.sequence_number) + " - " + str(self.vorname) +" "+ str(self.nachname) + " - [" + str(self.Auftrag_status) + "]"





class AuftragPdfResponseApi(models.Model):
    Auftrag = models.OneToOneField(Auftrag, on_delete=models.CASCADE)
    response = models.BinaryField()