# Generated by Django 5.0.6 on 2024-05-17 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emprendimiento', '0005_marketing'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketing',
            name='gastos_marketing',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
