# Generated by Django 4.2.1 on 2023-05-28 08:15

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('playfairauth', '0015_customusermodel_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customusermodel',
            name='company',
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('industry', models.CharField(default='Software', max_length=100)),
                ('phone', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('address', models.CharField(max_length=100, null=True)),
                ('country', models.JSONField(null=True)),
                ('city', models.JSONField(null=True)),
                ('state', models.JSONField(null=True)),
                ('foundedIn', models.CharField(default=2023, max_length=100, null=True)),
                ('website', models.CharField(default=None, max_length=100, null=True)),
                ('lat', models.DecimalField(decimal_places=8, max_digits=15, null=True)),
                ('long', models.DecimalField(decimal_places=8, max_digits=15, null=True)),
                ('size', models.CharField(default=1, max_length=100)),
                ('jobCount', models.IntegerField(default=0)),
                ('facebook', models.CharField(blank=True, max_length=100, null=True)),
                ('twitter', models.CharField(blank=True, max_length=100, null=True)),
                ('linkedIn', models.CharField(blank=True, max_length=100, null=True)),
                ('instagram', models.CharField(blank=True, max_length=100, null=True)),
                ('rating', models.CharField(max_length=5, null=True)),
                ('logo', models.FileField(null=True, upload_to='')),
                ('createdAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
