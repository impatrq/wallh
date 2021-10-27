# Generated by Django 3.2.5 on 2021-08-10 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_apellido', models.CharField(max_length=90)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('dni', models.CharField(max_length=8)),
                ('afecciones', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Sensores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiebre', models.CharField(max_length=2)),
                ('pulso', models.IntegerField()),
                ('oxigeno', models.CharField(max_length=30)),
                ('fecha_medidas', models.DateField(auto_now_add=True)),
            ],
        ),
    ]