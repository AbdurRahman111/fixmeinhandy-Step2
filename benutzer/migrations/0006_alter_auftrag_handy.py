# Generated by Django 4.2.4 on 2023-08-16 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("benutzer", "0005_auftrag_pdf_label"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auftrag",
            name="handy",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]