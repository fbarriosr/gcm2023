# Generated by Django 3.1.7 on 2024-05-03 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0055_torneo_galeria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='torneo',
            name='list_inscritos',
        ),
    ]
