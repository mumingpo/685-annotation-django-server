# Generated by Django 3.0.3 on 2020-02-11 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs685', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='time_filled',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
