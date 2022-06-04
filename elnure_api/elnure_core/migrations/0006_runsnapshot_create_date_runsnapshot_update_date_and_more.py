# Generated by Django 4.0.5 on 2022-06-04 21:31

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('elnure_core', '0005_rename_strategysnapshot_runsnapshot_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='runsnapshot',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='runsnapshot',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='capacity',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='electivecourse',
            name='capacity',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
