from django.db import models
from datetime import *
import uuid
from django.db import models
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from phone_field import PhoneField
from django.db.models.signals import post_save, pre_save
from ckeditor.fields import RichTextField
import datetime

class Company(models.Model):
    id = models.CharField(max_length = 50, default = uuid.uuid4, primary_key = True, editable = False)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, null=True)
    description = RichTextField(blank=True, null=True)
    email = models.EmailField(null=True, unique=True, error_messages={'unique': u"This email has already been registered."})
    industry = models.CharField(max_length=100, default=None, null=True)
    phone = models.CharField(max_length=20, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    country_code = models.CharField(max_length=6, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    founded_in = models.IntegerField(default=2023, null=True)
    website = models.CharField(max_length=100, null=True, default=None)
    lat = models.DecimalField(max_digits=15, decimal_places=8, null=True)
    long = models.DecimalField(max_digits=15, decimal_places=8, null=True)
    size = models.CharField(max_length=100, default=1)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.CASCADE, null=True)
    job_count = models.IntegerField(default=0)
    facebook = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    linkedIn= models.CharField(max_length=100, null=True, blank=True)
    instagram= models.CharField(max_length=100, null=True, blank=True)
    rating = models.CharField(max_length=5, null=True)
    logo = models.FileField(null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True, auto_created=True)
    is_complete = models.BooleanField(default = False)
    stripe_account = models.CharField(max_length=100, null=True, blank=True)
    stripe_bank_token = models.CharField(max_length=100, null=True, blank=True)
    stripe_person = models.CharField(max_length=50, null=True, blank=True)
    stripe_id_front = models.CharField(max_length=50, null=True, blank=True)
    stripe_id_back = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.name
    

class Logo(models.Model):
    user = models.OneToOneField('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null=True)
    logo = models.FileField(null=True)

class SavedCompanies(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null = True)
    saved = models.BooleanField(default=True, auto_created=True)

@receiver(models.signals.post_delete, sender=Company)
def remove_file_from_s3(sender, instance, using, **kwargs):
    instance.logo.delete(save=False)

@receiver(models.signals.post_save, sender=Logo)
def remove_file_from_s3_if_null(sender, instance, using, **kwargs):
    print("instance", instance.logo)

@receiver(post_save, sender=Company)
def save_company(sender, instance, created, **kwargs):
    company = instance
    
    if company.logo == None:
        company.logo.delete()
    