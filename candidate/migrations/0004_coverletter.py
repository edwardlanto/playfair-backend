# Generated by Django 4.2.1 on 2023-05-31 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0011_alter_job_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('candidate', '0003_appliedjob'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoverLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coverLetter', models.CharField(max_length=3000, null=True)),
                ('resume', models.CharField(max_length=200)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
