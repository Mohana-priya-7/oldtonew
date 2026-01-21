from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class Product(models.Model):
    name=models.CharField(max_length=100,unique=True)
    price=models.IntegerField()
    description=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name