# Generated by Django 4.2.1 on 2023-06-03 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0012_appliedjob_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appliedjob',
            name='userprofile',
        ),
    ]
