# Generated by Django 4.2.1 on 2023-07-14 05:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0012_contract_company'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('candidate', '0016_rename_createdat_savedjob_created_date_savedcontract'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppliedContract',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('applied_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_approved', models.BooleanField(default=False, null=True)),
                ('is_active', models.BooleanField(default=True, null=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contract.contract')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
