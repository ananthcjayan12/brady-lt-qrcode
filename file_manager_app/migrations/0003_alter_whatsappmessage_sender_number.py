# Generated by Django 4.2.5 on 2024-02-12 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("file_manager_app", "0002_whatsappmessage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="whatsappmessage",
            name="sender_number",
            field=models.CharField(blank=True, default=None, max_length=20),
        ),
    ]