# Generated by Django 3.2.9 on 2021-12-28 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='division',
            name='standard_size',
        ),
    ]
