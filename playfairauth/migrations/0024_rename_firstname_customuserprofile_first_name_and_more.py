# Generated by Django 4.2.1 on 2023-05-31 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playfairauth', '0023_remove_customuserprofile_useemailasuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuserprofile',
            old_name='firstName',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='customuserprofile',
            old_name='lastName',
            new_name='last_name',
        ),
    ]
