# Generated by Django 4.2.1 on 2023-05-29 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_rename_job_city_job_city_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='isCommision',
            new_name='isCommission',
        ),
    ]
