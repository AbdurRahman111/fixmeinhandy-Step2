# Generated by Django 4.2.4 on 2023-08-14 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("benutzer", "0003_auftrag_hausnummer_auftrag_straße"),
    ]

    operations = [
        migrations.RenameField(
            model_name="auftrag",
            old_name="adresse",
            new_name="Adresszeile",
        ),
        migrations.RenameField(
            model_name="auftrag",
            old_name="postleitzahl",
            new_name="Postleitzahl",
        ),
        migrations.RenameField(
            model_name="auftrag",
            old_name="Straße",
            new_name="Stadt",
        ),
    ]
