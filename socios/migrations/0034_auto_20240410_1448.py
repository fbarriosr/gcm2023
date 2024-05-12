# Generated by Django 3.1.7 on 2024-04-10 14:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0033_multimedia'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElClub',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('titulo', models.CharField(max_length=200)),
                ('archivo', models.FileField(blank=True, max_length=254, upload_to='ElClub/')),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'ElClub',
                'verbose_name_plural': 'ElClubs',
                'ordering': ['order'],
            },
        ),
        migrations.RemoveField(
            model_name='multimedia',
            name='info',
        ),
    ]