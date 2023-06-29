# Generated by Django 4.2.1 on 2023-06-27 01:00

import ckeditor.fields
from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Gig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(5, 'the field must contain at least 5 characters')])),
                ('description', ckeditor.fields.RichTextField(blank=True, validators=[django.core.validators.MinLengthValidator(50, 'the field must contain at least 50 characters')])),
                ('items', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), size=None)),
                ('delivery_type', models.CharField(choices=[('digital', 'Digital'), ('physical', 'Physical')], default='physical', max_length=100)),
                ('currency', models.JSONField()),
                ('industry', models.CharField(choices=[('Accounting', 'Accounting'), ('Advertising', 'Advertising'), ('Agriculture', 'Agriculture'), ('Architecture', 'Architecture'), ('Arts', 'Arts'), ('Automative', 'Automative'), ('Banking', 'Banking'), ('Biotechnology', 'Biotechnology'), ('Business', 'Business'), ('Business Development', 'Businessdevelopment'), ('Chemical', 'Chemical'), ('Construction', 'Construction'), ('Consulting', 'Consulting'), ('Consumer Services', 'Consumerservices'), ('Customer Service', 'Customerservice'), ('Data Entry', 'Dataentry'), ('Design', 'Design'), ('Education', 'Education'), ('Energy', 'Energy'), ('Engineering', 'Engineering'), ('Entertainment', 'Entertainment'), ('Environmental', 'Environmental'), ('Event Planning', 'Eventplanning'), ('Fashion', 'Fashion'), ('Finance', 'Finance'), ('Food Services', 'Foodservices'), ('Gaming', 'Gaming'), ('Government', 'Government'), ('Graphics', 'Graphics'), ('Health & Beauty', 'Healthbeauty'), ('Healthcare', 'Healthcare'), ('Hospitality', 'Hospitality'), ('Human Resources', 'Humanresources'), ('Information Technology', 'Informationtechnology'), ('Insurance', 'Insurance'), ('Interior Design', 'Interiordesign'), ('Investment', 'Investment'), ('Journalism', 'Journalism'), ('Legal', 'Legal'), ('Legal Services', 'Legalservices'), ('Logistics', 'Logistics'), ('Manufacturing', 'Manufacturing'), ('Marketing', 'Marketing'), ('Media', 'Media'), ('Military', 'Military'), ('Music', 'Music'), ('Nonprofit', 'Nonprofit'), ('Operations', 'Operations'), ('Pharmaceutical', 'Pharmaceutical'), ('Photography', 'Photography'), ('Product Management', 'Productmanagement'), ('Project Management', 'Projectmanagement'), ('Public Health', 'Publichealth'), ('Public Relations', 'Publicrelations'), ('Quality Assurance', 'Qualityassurance'), ('Real Estate', 'Realestate'), ('Research', 'Research'), ('Restaurant', 'Restaurant'), ('Retail', 'Retail'), ('Sales', 'Sales'), ('Science', 'Science'), ('Security', 'Security'), ('Social Services', 'Socialservices'), ('Software', 'Software'), ('Sports', 'Sports'), ('Supply Chain', 'Supplychain'), ('Telecommunications', 'Telecommunications'), ('Tourism', 'Tourism'), ('Training', 'Training'), ('Transportation', 'Transportation'), ('Travel', 'Travel'), ('Utilities', 'Utilities'), ('Video', 'Video'), ('Wealth Management', 'Wealthmanagement'), ('Writing & Translation', 'Writingtranslation')], default='', max_length=100)),
                ('amount', models.IntegerField(null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('schedule', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('type', models.CharField(choices=[('offer', 'Offer'), ('transaction', 'Transaction'), ('Milestone', 'Milestone')], default='transaction', max_length=100)),
                ('quantity', models.IntegerField(default=1)),
                ('city', models.JSONField(blank=True, null=True)),
                ('country', models.JSONField(blank=True, null=True)),
                ('state', models.JSONField(blank=True, null=True)),
                ('min_rate', models.CharField(blank=True, max_length=255, null=True)),
                ('max_rate', models.CharField(blank=True, max_length=255, null=True)),
                ('buyer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gig_buyer', to=settings.AUTH_USER_MODEL)),
                ('seller', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gig_seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
