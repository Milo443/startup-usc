# Generated by Django 5.0.6 on 2024-06-05 15:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emprendimiento', '0012_alter_cargoempleado_descripcion_cargo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketing',
            name='mercado_objetivo',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analisis', models.TextField(blank=True, max_length=1000, null=True)),
                ('financiero', models.TextField(blank=True, max_length=1000, null=True)),
                ('marketing', models.TextField(blank=True, max_length=1000, null=True)),
                ('producto', models.TextField(blank=True, max_length=1000, null=True)),
                ('recursos', models.TextField(blank=True, max_length=1000, null=True)),
                ('identidad', models.TextField(blank=True, max_length=1000, null=True)),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emprendimiento.proyecto')),
            ],
        ),
    ]
