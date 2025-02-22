# Generated by Django 4.2.1 on 2023-08-04 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0030_alter_contract_industry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.CharField(choices=[('Available', 'Available'), ('Cancelled', 'Cancelled'), ('Error', 'Error'), ('Completed', 'Completed'), ('Paid', 'Paid'), ('In Progress', 'In Progress')], default='available', max_length=20),
        ),
    ]
