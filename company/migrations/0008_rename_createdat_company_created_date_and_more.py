# Generated by Django 4.2.1 on 2023-05-29 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_savedcompanies_logo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='createdAt',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='foundedIn',
            new_name='founded_in',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='jobCount',
            new_name='job_count',
        ),
        migrations.AddField(
            model_name='company',
            name='is_active',
            field=models.BooleanField(auto_created=True, default=True),
        ),
    ]
