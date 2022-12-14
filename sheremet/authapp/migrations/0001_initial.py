# Generated by Django 4.1.2 on 2022-10-21 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('login', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=60)),
                ('role', models.CharField(max_length=40)),
                ('last_date', models.DateTimeField(blank=True, null=True)),
                ('is_admin', models.BooleanField(default=False, null=True)),
            ],
        ),
    ]
