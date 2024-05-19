# Generated by Django 5.0.6 on 2024-05-17 00:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emprendimiento', '0004_financiero'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marketing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mercado_objetivo', models.CharField(blank=True, max_length=250, null=True)),
                ('segmentacion_cliente', models.CharField(blank=True, max_length=250, null=True)),
                ('canal_marketing', models.CharField(blank=True, max_length=250, null=True)),
                ('estrategia_precio_promocion', models.CharField(blank=True, max_length=250, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, null=True)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emprendimiento.proyecto')),
            ],
        ),
    ]