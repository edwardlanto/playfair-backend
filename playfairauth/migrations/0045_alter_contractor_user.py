# Generated by Django 4.2.1 on 2023-07-14 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playfairauth', '0044_contractor_stripe_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractor',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contractor', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
