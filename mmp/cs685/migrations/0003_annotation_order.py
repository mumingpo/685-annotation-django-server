# Generated by Django 3.0.3 on 2020-02-13 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs685', '0002_annotation_time_filled'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='order',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]