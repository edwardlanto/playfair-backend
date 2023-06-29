from django.db import models
from company.models import Company
import datetime

class Message(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey('playfairauth.CustomUserModel', on_delete=models.SET_NULL, null = True)
    message = models.CharField(null=True, default=None)
    time_stamp = models.DateTimeField(auto_now_add=True, null=True)