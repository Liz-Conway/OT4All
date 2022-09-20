# Generated by Django 4.0.6 on 2022-09-20 18:00

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ("purchase", "0003_order_original_bookings_order_stripe_pid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="country",
            field=django_countries.fields.CountryField(max_length=2),
        ),
        migrations.AlterField(
            model_name="order",
            name="postcode",
            field=models.CharField(default="XXX", max_length=20),
            preserve_default=False,
        ),
    ]
