# Generated by Django 4.2.1 on 2023-05-28 22:43

import ckeditor.fields
import datetime
from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0005_alter_company_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobCategory_title', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobCategory_title', models.CharField(max_length=200, null=True)),
                ('jobCategory_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('isRemote', models.BooleanField(auto_created=True, default=False)),
                ('isActive', models.BooleanField(auto_created=True, default=True)),
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=50, primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=200, null=True)),
                ('appliedCount', models.CharField(blank=True, default=0, max_length=200, null=True)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('candidates', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(null=True), blank=True, size=None)),
                ('featured', models.BooleanField(default=False)),
                ('isCommision', models.BooleanField(default=False)),
                ('expiredAt', models.DateField(default=datetime.date.today)),
                ('address', models.CharField(max_length=100, null=True)),
                ('job_country', models.JSONField(null=True)),
                ('job_facebook', models.CharField(blank=True, max_length=100, null=True)),
                ('job_twitter', models.CharField(blank=True, max_length=100, null=True)),
                ('job_state', models.JSONField(null=True)),
                ('jobType', django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(), size=None)),
                ('education', models.CharField(choices=[('Bachelors', 'Bachelors'), ('Masters', 'Masters'), ('Phd', 'Phd')], default='Bachelors', max_length=100)),
                ('job_city', models.JSONField(null=True)),
                ('industry', models.CharField(choices=[('Business', 'Business'), ('Programming', 'Programming'), ('Finance', 'Finance'), ('Education/Training', 'Education'), ('Telecommunication', 'Telecommunication'), ('Agriculture', 'Agriculture'), ('Graphics', 'Graphics'), ('Digital Marketing', 'Digitalmarketing'), ('Design', 'Design'), ('Video', 'Video'), ('Animation', 'Animation'), ('Audio', 'Audio'), ('Photography', 'Photography'), ('Writing', 'Writing'), ('Human Resources', 'Humanresources'), ('Legal', 'Legal'), ('Security', 'Security'), ('Health & Beauty', 'Healthybeauty')], default='Business', max_length=100)),
                ('experience', models.CharField(choices=[('No Experience', 'No Experience'), ('1 Year', 'One Year'), ('2 Years', 'Two Year'), ('3 Years', 'Three Year'), ('4 Years', 'Four Year'), ('5 Years+', 'Five Year Plus')], default='No Experience', max_length=100)),
                ('minSalary', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)])),
                ('maxSalary', models.IntegerField(default=1, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)])),
                ('positions', models.IntegerField(default=1)),
                ('responsibilities', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('skills', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('long', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('createdAt', models.DateField(auto_now_add=True, null=True)),
                ('startAt', models.DateField(default=datetime.date.today, null=True)),
                ('weeklyHours', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company', to='company.company')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CandidatesSavedJobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved', models.BooleanField(auto_created=True, default=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CandidatesCoverLetter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coverLetter', models.CharField(max_length=3000, null=True)),
                ('resume', models.CharField(max_length=200)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CandidatesApplied',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume', models.CharField(max_length=3000)),
                ('appliedAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('coverLetter', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('isApproved', models.BooleanField(null=True)),
                ('isActive', models.BooleanField(default=True, null=True)),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.job')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
