# Generated by Django 3.1.7 on 2024-05-01 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0054_multimediaimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='torneo',
            name='galeria',
            field=models.CharField(default='No Disponible', max_length=300, verbose_name='Url Galeria'),
        ),
    ]