# Generated by Django 4.1.2 on 2022-10-21 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='setting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UTC', models.SmallIntegerField(blank=True, default=0)),
            ],
        ),
    ]
