# Generated by Django 4.2.1 on 2023-07-14 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0028_alter_company_founded_in'),
        ('contract', '0011_contract_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='company.company'),
        ),
    ]
