# Generated by Django 3.2.9 on 2021-12-23 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='attestation_period',
        ),
    ]
