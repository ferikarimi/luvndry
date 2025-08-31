from django.db import models
# from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Customers (models.Model):
    class Meta:
        pass
    fullname = models.CharField(max_length=255 , null=True , blank=True)
    phone = PhoneNumberField(unique=True)
    address = models.CharField(max_length=255 , null=True , blank=True)
    code = models.PositiveIntegerField(unique=True , null=True , blank=True)

    def __str__(self):
        return f"{self.fullname}"



class Comments (models.Model):
    STATUS_CHOICE = [
        ('pending','pending'),
        ('approved','approved'),
        ('rejected','rejected')
    ]
    customer = models.ForeignKey(Customers , on_delete=models.CASCADE , related_name='comments')
    text = models.TextField()
    status = models.CharField(choices=STATUS_CHOICE , default='pending' , max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"comment by {self.customer.phone} : {self.status}."