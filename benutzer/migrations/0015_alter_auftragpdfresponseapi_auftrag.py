# Generated by Django 4.2.4 on 2023-08-21 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("benutzer", "0014_rename_auftrag_pdf_responseapi_auftragpdfresponseapi"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auftragpdfresponseapi",
            name="Auftrag",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="benutzer.auftrag"
            ),
        ),
    ]
