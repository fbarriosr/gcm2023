# Generated by Django 3.1.7 on 2024-05-13 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0058_torneo_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='torneo',
            name='recargo',
            field=models.IntegerField(default=5000),
        ),
    ]
