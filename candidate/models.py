from django.db import models
from job.models import Job
from ckeditor.fields import RichTextField
from company.models import Company
import uuid
class SavedJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null = True)
    saved = models.BooleanField(default=True, auto_created=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True)

class SavedCompany(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null = True)
    saved = models.BooleanField(default=True, auto_created=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

class Candidate(models.Model):
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null = True)

class AppliedJob(models.Model):
    id = models.CharField(max_length = 50, default = uuid.uuid4, primary_key = True, editable = False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null = True)
    resume = models.CharField(max_length=3000)
    appliedAt = models.DateTimeField(auto_now_add=True, null=True)
    coverLetter = RichTextField(blank=True, null=True)
    is_approved = models.BooleanField(null=True, default=False)
    is_active = models.BooleanField(null=True, default=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    # userprofile = models.JSONField(null=True, blank=True)

class CoverLetter(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null = True)
    coverLetter = models.CharField(max_length=3000, null=True)
    resume = models.CharField(max_length=200)