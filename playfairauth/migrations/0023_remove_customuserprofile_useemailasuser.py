# Generated by Django 4.2.1 on 2023-05-31 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playfairauth', '0022_alter_customuserprofile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuserprofile',
            name='useEmailAsUser',
        ),
    ]
