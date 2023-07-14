from django.db import models
import datetime
from django.db import models
from playfairauth.models import CustomUserModel
from django.contrib.postgres.fields import ArrayField
from datetime import date
from ckeditor.fields import RichTextField
from company.models import Company
from job.models import Industry
import datetime
from django.utils import timezone
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
import uuid

class Type(models.TextChoices):
    buying = 'buying'
    selling = 'selling'

class Status(models.TextChoices):
    cancelled = 'cancelled'
    error = 'error'
    pending = 'pending'
    success = 'success'

class DeliveryType(models.TextChoices):
    digital = 'digital'
    physical = 'physical'

class Contract(models.Model):
    id = models.CharField(max_length = 50, default = uuid.uuid4, primary_key = True, editable = False)
    title = models.CharField(max_length=200, validators=[ MinLengthValidator(5, 'the field must contain at least 5 characters')])
    description = RichTextField(blank=True, validators=[ MinLengthValidator(50, 'the field must contain at least 50 characters')])
    # items = ArrayField(models.JSONField())
    delivery_type  = models.CharField(
        max_length=100,
        choices=DeliveryType.choices,
        default=DeliveryType.physical
    )
    currency = models.JSONField()
    industry = models.CharField(
        max_length=100,
        choices=Industry.choices,
        default=""
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default="pending"
    )
    amount = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    seller = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True, related_name="contract_seller")
    buyer = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True, related_name="contract_buyer")
    quantity = models.IntegerField(default=1)
    image = models.FileField(null=True, blank=True)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, null=True)
    schedule = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(default=timezone.now)
    type = models.CharField(
        max_length=100,
        choices=Type.choices,
        default=Type.buying
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    user_type = models.CharField(max_length=100, default="company")
    state = models.CharField(max_length=100, null=True)
    min_rate = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    max_rate = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    is_active = models.BooleanField(default=True)




    class Meta:
        db_table = "contract"
