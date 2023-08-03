from django.db import models
from django.db import models
from playfairauth.models import CustomUserModel
from ckeditor.fields import RichTextField
from company.models import Company
from job.models import Industry
from django.utils import timezone
from django.core.validators import (
    MinLengthValidator,
)
import uuid
from django.contrib.postgres.fields import ArrayField
class Type(models.TextChoices):
    buying = 'buying'
    selling = 'selling'

class Status(models.TextChoices):
    available = 'Available'
    cancelled = 'Cancelled'
    error = 'Error'
    pending = 'Pending'
    completed = 'Completed'
    paid = 'Paid'
    in_progress = 'In Progress'

class DeliveryType(models.TextChoices):
    digital = 'digital'
    physical = 'physical'

class Contract(models.Model):
    id = models.CharField(max_length = 50, default = uuid.uuid4, primary_key = True, editable = False)
    title = models.CharField(max_length=200, validators=[ MinLengthValidator(5, 'the field must contain at least 5 characters')])
    description = RichTextField(blank=True, validators=[ MinLengthValidator(50, 'the field must contain at least 50 characters')])
    candidates = ArrayField(models.JSONField(null=True), blank=True, null=True)
    delivery_type  = models.CharField(
        max_length=100,
        choices=DeliveryType.choices,
        default=DeliveryType.physical
    )
    currency = models.JSONField(null=True)
    industry = models.CharField(
        max_length=100,
        choices=Industry.choices,
        default="Construction"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default="pending"
    )
    paid = models.BooleanField(default=False)
    amount = models.DecimalField(decimal_places=2, max_digits=9, null=True, blank=True)
    poster = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True, related_name="contract_poster", blank=True)
    contractor = models.ForeignKey(CustomUserModel, on_delete=models.SET_NULL, null=True, related_name="contract_contractor", blank=True)
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
