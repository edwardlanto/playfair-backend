# Generated by Django 4.2.1 on 2023-05-28 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='user',
        ),
    ]
