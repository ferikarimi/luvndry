from django.db import models
from Customers.models import Customers
from Items.models import Items



class Orders (models.Model):

    STATUS_CHOICE_FIELDS = [
        ('Received', 'Received') ,
        ('In progress', 'In progress') ,
        ('Completed'  , 'Completed' ) ,
        ('Delivered'  , 'Delivered' )
    ]

    # order_code = models.ForeignKey()
    customer_id = models.ForeignKey(Customers , on_delete=models.CASCADE)
    discount_amount = models.IntegerField(default=0)
    total_amount = models.IntegerField()
    final_amount = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICE_FIELDS ,default='Received',max_length=15)
    order_time = models.DateTimeField(auto_now_add=True)
    delivey_time = models.DateTimeField(null=True , blank=True)


class OrderItems (models.Model):
    order = models.ForeignKey(Orders , on_delete=models.CASCADE , related_name="order_items")
    item = models.ForeignKey(Items , on_delete=models.PROTECT)
    cloth_name = models.CharField (max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.IntegerField()