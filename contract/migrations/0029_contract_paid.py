# Generated by Django 4.2.1 on 2023-07-20 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0028_alter_contract_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]
