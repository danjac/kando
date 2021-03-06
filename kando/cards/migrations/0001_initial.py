# Generated by Django 3.1.3 on 2020-11-30 19:27

# Django
import django.utils.timezone
from django.db import migrations, models

# Third Party Libraries
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Card",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("position", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=0)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                ("deadline", models.DateField(blank=True, null=True)),
                ("complexity", models.PositiveIntegerField(default=1)),
                ("priority", models.PositiveIntegerField(default=1)),
                ("hours_estimated", models.PositiveIntegerField(default=0)),
                ("hours_spent", models.PositiveIntegerField(default=0)),
            ],
            options={"abstract": False,},
        ),
    ]
