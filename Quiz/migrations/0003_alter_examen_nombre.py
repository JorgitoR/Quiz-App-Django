# Generated by Django 3.2 on 2021-04-06 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0002_alter_respuesta_correcta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examen',
            name='nombre',
            field=models.TextField(verbose_name='Nombre del Examen'),
        ),
    ]
