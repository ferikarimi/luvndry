from django.db import models
from Customers.models import Customers
from Items.models import Services , Clothes



class Orders (models.Model):

    STATUS_CHOICE_FIELDS = [
        ('Received', 'Received') ,
        ('In progress', 'In progress') ,
        ('Completed'  , 'Completed' ) ,
        ('Delivered'  , 'Delivered' )
    ]

    customer = models.ForeignKey(Customers , on_delete=models.CASCADE , related_name="orders")
    discount_amount = models.IntegerField(default=0)
    total_amount = models.IntegerField()
    final_amount = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICE_FIELDS ,default='Received',max_length=15)
    order_time = models.DateTimeField(auto_now_add=True)
    delivery_time = models.DateField(null=True , blank=True)

    def __str__(self):
        return f"order #{self.id} - {self.customer.phone}"
    
    def calculate_final_amount (self):
        self.final_amount = self.total_amount - self.discount_amount
        self.save()


class OrderItems (models.Model):
    order = models.ForeignKey(Orders , on_delete=models.CASCADE , related_name="order_items")
    service = models.ForeignKey(Services , on_delete=models.PROTECT)
    cloth = models.ForeignKey(Clothes , on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.IntegerField()

    def save(self, *args , **kwargs) :
        self.unit_price = self.service.base_price + self.cloth.price_modifier
        super().save(*args , **kwargs)