# Generated by Django 4.2.1 on 2023-07-19 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0025_alter_contract_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='currency',
            field=models.JSONField(null=True),
        ),
    ]
