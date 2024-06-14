# Generated by Django 5.0.6 on 2024-06-13 01:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0005_message_room_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChannelTracking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('channel_name', models.CharField(blank=True, max_length=1000, null=True)),
                ('user', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
