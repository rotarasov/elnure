# Generated by Django 4.0.5 on 2022-06-04 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elnure_config', '0001_initial'),
        ('elnure_core', '0004_rename_application_window_snapshot_strategysnapshot_application_window_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StrategySnapshot',
            new_name='RunSnapshot',
        ),
        migrations.AlterModelTable(
            name='runsnapshot',
            table='run_snapshots',
        ),
    ]
