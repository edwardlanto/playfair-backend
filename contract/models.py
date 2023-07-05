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
    offer = 'offer'
    transaction = 'transaction'
    milestone = 'Milestone'

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
    items = ArrayField(models.JSONField())
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
    amount = models.IntegerField(null=True)
    seller = models.OneToOneField(CustomUserModel, on_delete=models.SET_NULL, null=True, related_name="contract_seller")
    buyer = models.OneToOneField(CustomUserModel, on_delete=models.SET_NULL, null=True, related_name="contract_buyer")
    quantity = models.IntegerField(default=1)
    image = models.FileField(null=True, blank=True)
    schedule = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(default=timezone.now)
    type = models.CharField(
        max_length=100,
        choices=Type.choices,
        default=Type.transaction
    )
    quantity = models.IntegerField(default=1)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    min_rate = models.CharField(max_length=255, null=True, blank=True)
    max_rate = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "contract"
