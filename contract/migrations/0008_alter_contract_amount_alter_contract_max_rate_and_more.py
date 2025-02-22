# Generated by Django 4.2.1 on 2023-07-13 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0007_contract_lat_contract_long_alter_contract_max_rate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='max_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='min_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
    ]
