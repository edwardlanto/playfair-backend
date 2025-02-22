# Generated by Django 4.2.1 on 2023-07-19 05:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_stripeintent'),
        ('candidate', '0027_appliedcontract_payment_intent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedcontract',
            name='payment_intent',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.stripeintent'),
        ),
    ]
