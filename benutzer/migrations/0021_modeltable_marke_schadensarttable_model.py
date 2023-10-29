# Generated by Django 4.2.4 on 2023-10-11 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("benutzer", "0020_marketable_modeltable_schadensarttable"),
    ]

    operations = [
        migrations.AddField(
            model_name="modeltable",
            name="Marke",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="benutzer.marketable",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="schadensarttable",
            name="Model",
            field=models.ForeignKey(
                default="",
                on_delete=django.db.models.deletion.CASCADE,
                to="benutzer.modeltable",
            ),
            preserve_default=False,
        ),
    ]
