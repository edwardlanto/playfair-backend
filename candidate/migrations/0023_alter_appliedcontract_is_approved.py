# Generated by Django 4.2.1 on 2023-07-17 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate', '0022_alter_appliedcontract_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedcontract',
            name='is_approved',
            field=models.CharField(choices=[('approved', 'Approved'), ('declined', 'Declined'), ('pending', 'Pending')], default='pending', max_length=100),
        ),
    ]
