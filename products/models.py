from django.db import models
from datetime import datetime

class Product(models.Model):
    name = models.CharField(max_length=256, unique=True)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)
    description = models.CharField(max_length=512, default="-")

class FileUpload(models.Model):
    file = models.FileField(upload_to="uploads")
    created_at = models.DateTimeField(auto_now=True)