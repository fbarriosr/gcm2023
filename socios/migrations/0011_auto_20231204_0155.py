# Generated by Django 3.1.7 on 2023-12-04 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0010_solicitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='estado',
            field=models.CharField(choices=[('P', 'Pendiente'), ('A', 'Aprobado'), ('R', 'Rechazado')], default='P', max_length=50, verbose_name='Estado'),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='motivo',
            field=models.TextField(blank=True, default='', verbose_name='Motivo'),
        ),
    ]
