# Generated by Django 5.1.5 on 2025-02-03 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='fitness_goal',
            field=models.CharField(choices=[('weight loss', 'Weight Loss'), ('muscle gain', 'Muscle Gain'), ('maintenance', 'Maintenance')], default='maintenance', max_length=50),
        ),
    ]
