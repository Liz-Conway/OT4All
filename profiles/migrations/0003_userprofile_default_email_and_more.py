# Generated by Django 4.0.6 on 2022-09-21 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "profiles",
            "0002_rename_default_town_or_city_userprofile_default_city",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="default_email",
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="default_full_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
