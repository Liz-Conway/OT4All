# Generated by Django 4.0.6 on 2022-09-12 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("therapy", "0003_alter_therapy_course_sessions"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="therapy",
            name="image_url",
        ),
    ]
