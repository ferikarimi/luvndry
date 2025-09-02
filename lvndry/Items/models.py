from django.db import models

# Create your models here.


class Items (models.Model) :

    name = models.CharField(max_length=255 , unique=True)
    description = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return self.name