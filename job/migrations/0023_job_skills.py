# Generated by Django 4.2.1 on 2023-08-28 06:39

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0022_remove_job_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='skills',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
