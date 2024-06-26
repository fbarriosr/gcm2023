# Generated by Django 3.1.7 on 2024-05-01 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socios', '0053_auto_20240429_1427'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultimediaImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.FileField(upload_to='multimedia/')),
                ('multimedia', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='socios.multimedia')),
            ],
            options={
                'verbose_name': 'MultimediaImg',
                'verbose_name_plural': 'MultimediasImg',
                'ordering': ['img'],
            },
        ),
    ]
