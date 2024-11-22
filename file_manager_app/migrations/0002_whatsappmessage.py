# Generated by Django 4.2.5 on 2024-02-12 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("file_manager_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="WhatsAppMessage",
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
                ("received_at", models.DateTimeField(auto_now_add=True)),
                ("sender_number", models.CharField(max_length=20)),
                ("payload", models.JSONField()),
            ],
        ),
    ]