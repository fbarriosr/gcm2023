# Generated by Django 3.1.7 on 2024-09-23 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0022_auto_20240916_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='categoria',
            field=models.CharField(choices=[('S', 'SENIOR'), ('SS', 'SUPERSENIOR'), ('V', 'VARON'), ('J', 'JUVENIL'), ('D', 'DAMA')], default='NI', max_length=20),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='condicion',
            field=models.CharField(blank=True, choices=[('R', 'RETIRO'), ('A', 'ACTIVO'), ('J', 'JUBILADO (A)'), ('NI', 'NO INFORMAR')], default='NI', max_length=20),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='grado',
            field=models.CharField(blank=True, choices=[('GDE', 'GENERAL DE EJÉRCITO'), ('GDD', 'GENERAL DE DIVISIÒN'), ('GDB', 'GENERAL DE BRIGADA'), ('BGR', 'BRIGADIER'), ('CRL', 'CORONEL'), ('TCL', 'TENIENTE CORONEL'), ('MAY', 'MAYOR'), ('CAP', 'CAPITAN'), ('TTE', 'TENIENTE'), ('STE', 'SUB TENIENTE'), ('ALF', 'ALFÉREZ'), ('CAD', 'CADETE '), ('SR', 'SEÑOR'), ('SRa', 'SEÑORA'), ('NI', 'NO INFORMAR')], default='NI', max_length=5),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='id',
            field=models.PositiveIntegerField(default=0, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='institucion',
            field=models.CharField(blank=True, choices=[('E', 'Ejército de Chile'), ('A', 'Armada de Chile'), ('FACH', 'Fuerza Aérea de Chile'), ('C', 'Carabineros de Chile'), ('PDI', 'Policia de Investigación'), ('NI', 'NO INFORMAR')], default='NI', max_length=20),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='region',
            field=models.CharField(blank=True, choices=[('XIII', 'Región Metropolitana de Santiago'), ('I', 'Región de Tarapacá'), ('II', 'Región de Antofagasta'), ('III', 'Región de Atacama'), ('IV', 'Región de Coquimbo'), ('V', 'Región de Valparaíso'), ('VI', 'Región del Libertador General Bernardo O’Higgins'), ('VII', 'Región del Maule'), ('VIII', 'Región del Bio-bío'), ('IX', 'Región de La Araucanía'), ('X', 'Región de Los Lagos'), ('XI', 'Región Aysén del General Carlos Ibáñez del Campo'), ('XII', 'Región de Magallanes y Antártica Chilena'), ('XIV', 'Región de Los Ríos'), ('XV', 'Región de Arica y Parinacota'), ('XVI', 'Región de Ñuble'), ('NI', 'NO INFORMAR')], default=' ', max_length=50, verbose_name='Region'),
        ),
    ]
