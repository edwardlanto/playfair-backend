# Generated by Django 4.2.1 on 2023-05-31 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('playfairauth', '0021_rename_isagevisible_customuserprofile_is_age_visible_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuserprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL),
        ),
    ]
