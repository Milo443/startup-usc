# Generated by Django 5.0.6 on 2024-05-16 01:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emprendimiento', '0003_proyecto_fecha_creacion_alter_proyecto_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Financiero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ventas', models.FloatField(blank=True, null=True)),
                ('costos_produccion', models.FloatField(blank=True, null=True)),
                ('gastos_administrativos', models.FloatField(blank=True, null=True)),
                ('capital_propio', models.FloatField(blank=True, null=True)),
                ('prestamo', models.FloatField(blank=True, null=True)),
                ('inversores', models.FloatField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emprendimiento.proyecto')),
            ],
        ),
    ]
