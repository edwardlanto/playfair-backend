# Generated by Django 4.2.1 on 2023-05-26 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playfairauth', '0008_remove_customusermodel_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='account_type',
            field=models.CharField(default='candidate', max_length=100),
        ),
    ]
