from django.db import models
from job.models import Job
from contract.models import Contract
from ckeditor.fields import RichTextField
from company.models import Company
from playfairauth.models import Contractor
from playfairauth.models import CustomUserModel
import uuid

class Status(models.TextChoices):
    approved = 'approved'
    declined = 'declined'
    pending = 'pending'

class SavedJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null = True)
    saved = models.BooleanField(default=True, auto_created=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

class SavedContract(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null = True)
    saved = models.BooleanField(default=True, auto_created=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

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

class AppliedContract(models.Model):
    id = models.CharField(max_length = 50, default = uuid.uuid4, primary_key = True, editable = False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    poster = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null = True)
    contractor = models.ForeignKey(Contractor, on_delete=models.SET_NULL, null = True)
    coverLetter = RichTextField(blank=True, null=True) 
    applied_date = models.DateTimeField(auto_now_add=True, null=True)
    is_approved = models.BooleanField(default=None, null=True)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.CASCADE, null=True, related_name="applied_contract_user")
    is_active = models.BooleanField(null=True, default=True)

    class Meta:
        db_table = "applied_contract"

class CoverLetter(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null = True)
    coverLetter = models.CharField(max_length=3000, null=True)
    resume = models.CharField(max_length=200)