# Generated by Django 3.1.7 on 2024-09-16 15:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0066_auto_20240913_0900'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parametro',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('tipo', models.CharField(default='A', max_length=20)),
                ('valor', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Parametro',
                'verbose_name_plural': 'Parametros',
                'ordering': ['tipo'],
            },
        ),
    ]
