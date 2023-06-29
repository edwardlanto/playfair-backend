from django.db import models
from datetime import *
import uuid

class Payment(models.Model):
    id = models.CharField(max_length = 50, default = uuid.uuid4, primary_key = True, editable = False)
