from django.db import models



class Clothes (models.Model):
    name = models.CharField(max_length=100)
    price_modifier = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class Services (models.Model):
    name = models.CharField(max_length=100)
    base_price = models.IntegerField()

    def __str__(self):
        return self.name