# Generated by Django 4.1.4 on 2023-01-04 13:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=50)),
                ("color", models.CharField(max_length=6)),
                ("description", models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name="Homework",
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
                ("name", models.CharField(max_length=100)),
                (
                    "description",
                    models.TextField(blank=True, default=" ", max_length=1000),
                ),
                ("display", models.BooleanField(default=False)),
                ("created_at", models.DateField(auto_now=True)),
                ("start_at", models.DateField(default=django.utils.timezone.now)),
                ("expired_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="HomeworkDetail",
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
                ("detail_name", models.CharField(max_length=100)),
                (
                    "detail_description",
                    models.TextField(blank=True, default=" ", max_length=1000),
                ),
                (
                    "detail_risk",
                    models.CharField(
                        choices=[("L", "Low"), ("N", "Normal"), ("H", "High")],
                        default="L",
                        max_length=2,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
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
                ("post_url", models.URLField()),
                ("post_at", models.DateField(auto_now=True)),
                (
                    "homework",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="posts.homework"
                    ),
                ),
            ],
        ),
    ]
