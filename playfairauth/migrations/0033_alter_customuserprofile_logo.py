# Generated by Django 4.2.1 on 2023-06-03 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playfairauth', '0032_alter_customuserprofile_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuserprofile',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
