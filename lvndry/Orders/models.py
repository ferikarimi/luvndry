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

    order_code = models.ForeignKey()
    customer_id = models.ForeignKey(Customers , on_delete=models.CASCADE)
    discount_amount = models.DecimalField(default=0)
    total_amount = models.DecimalField()
    final_amount = models.DecimalField()
    status = models.CharField(choices=STATUS_CHOICE_FIELDS ,default='Received')
    order_time = models.DateTimeField(auto_now_add=True)
    delivey_time = models.DateTimeField()


class OrderItems (models.Model):
    order_id = models.ForeignKey(Orders , on_delete=models.CASCADE)
    item_id = models.ForeignKey(Items , on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField()