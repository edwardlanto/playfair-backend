# Generated by Django 4.2.1 on 2023-07-21 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0018_job_work_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='work_status',
            field=models.CharField(default='Full-Time', max_length=20),
        ),
    ]
