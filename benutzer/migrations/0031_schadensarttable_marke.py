# Generated by Django 4.2.4 on 2023-10-29 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("benutzer", "0030_alter_modeltable_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="schadensarttable",
            name="Marke",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="benutzer.marketable",
            ),
        ),
    ]
