# Generated by Django 5.0.7 on 2024-08-19 10:50

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Match",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tournament",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "name",
                    models.CharField(
                        max_length=20,
                        validators=[
                            django.core.validators.MaxLengthValidator(20),
                            django.core.validators.RegexValidator(
                                message="Name must start with a letter and contain only letters, numbers, or underscores.",
                                regex="^[A-Za-z][A-Za-z0-9_]*$",
                            ),
                        ],
                    ),
                ),
                ("locked", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Player",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("points", models.IntegerField(default=0)),
                ("is_winner", models.BooleanField(default=False)),
                (
                    "match",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="game.match"
                    ),
                ),
            ],
        ),
    ]
