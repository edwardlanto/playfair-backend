# Generated by Django 4.2.1 on 2023-05-26 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playfairauth', '0003_alter_customusermodel_userid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='auth_provider',
            field=models.CharField(blank=True, default='email', max_length=50),
        ),
    ]
