# Generated by Django 3.1.7 on 2024-04-10 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0031_auto_20240408_1346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='torneo',
            old_name='proximo',
            new_name='actual',
        ),
        migrations.RemoveField(
            model_name='torneo',
            name='descripcion',
        ),
    ]