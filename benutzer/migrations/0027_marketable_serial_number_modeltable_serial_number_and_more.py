# Generated by Django 4.2.4 on 2023-10-22 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("benutzer", "0026_ausgeführter_befehl_serial_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="marketable",
            name="Serial_Number",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="modeltable",
            name="Serial_Number",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="schadensarttable",
            name="Serial_Number",
            field=models.IntegerField(default=0),
        ),
    ]
