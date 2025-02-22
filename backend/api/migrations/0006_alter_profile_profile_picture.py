# Generated by Django 5.1.4 on 2025-02-12 11:25

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pics/default.jpg', max_length=255, null=True, upload_to=api.models.profile_picture_upload_path),
        ),
    ]
