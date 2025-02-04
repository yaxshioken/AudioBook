# Generated by Django 5.1.4 on 2025-01-12 16:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="rating",
            field=models.IntegerField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
        ),
    ]
