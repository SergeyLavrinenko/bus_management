# Generated by Django 4.1.2 on 2022-10-22 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_bus_drivers_buses_task_working_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='flight_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
