from django.db import models
# from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Customers (models.Model):
    class Meta:
        pass
    fullname = models.CharField(max_length=255)
    phone = PhoneNumberField(unique=True)
    address = models.CharField(255 , null=True , blank=True)
