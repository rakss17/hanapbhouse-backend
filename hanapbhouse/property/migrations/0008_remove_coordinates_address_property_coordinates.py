# Generated by Django 5.0.6 on 2024-06-09 12:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_remove_address_coordinates_coordinates_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coordinates',
            name='address',
        ),
        migrations.AddField(
            model_name='property',
            name='coordinates',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_coordinates', to='property.coordinates'),
        ),
    ]
