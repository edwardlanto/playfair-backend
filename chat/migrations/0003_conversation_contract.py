# Generated by Django 4.2.1 on 2023-07-05 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0002_alter_contract_city_alter_contract_country_and_more'),
        ('chat', '0002_alter_conversation_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='contract',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_message_user', to='contract.contract'),
        ),
    ]
