# Generated by Django 4.2.1 on 2023-05-31 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0009_delete_candidatessavedjobs'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CandidatesApplied',
        ),
    ]
