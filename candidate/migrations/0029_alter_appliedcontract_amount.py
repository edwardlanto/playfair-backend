# Generated by Django 4.2.1 on 2023-07-19 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0028_alter_appliedcontract_payment_intent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedcontract',
            name='amount',
            field=models.IntegerField(default=0.0, null=True),
        ),
    ]
