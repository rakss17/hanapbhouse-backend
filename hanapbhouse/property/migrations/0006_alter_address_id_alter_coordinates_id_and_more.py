# Generated by Django 5.0.6 on 2024-06-09 09:25

import property.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0005_alter_property_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='id',
            field=models.CharField(default=property.models.generate_custom_id, editable=False, max_length=17, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='coordinates',
            name='id',
            field=models.CharField(default=property.models.generate_custom_id, editable=False, max_length=17, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='id',
            field=models.CharField(default=property.models.generate_custom_id, editable=False, max_length=17, primary_key=True, serialize=False, unique=True),
        ),
    ]