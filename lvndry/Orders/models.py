from django.db import models
from Customers.models import Customers
from Items.models import (
    Services , Clothes , ExtraServices
)



"""
    از این مدل برای ذخیره ی سفارش ها در دیتابیس استفاده می شود
"""
class Orders (models.Model):

    STATUS_CHOICE_FIELDS = [
        ('In progress', 'ورود به دنیای پاکیزگی آویژه'),
        ('Completed', 'پاکیزگی آماده درخشیدن است'),
        ('Delivered', 'بازگشت پاکیزگی به آغوش صاحبش'),
    ]

    customer = models.ForeignKey(Customers , on_delete=models.CASCADE , related_name="orders")
    discount_amount = models.IntegerField(default=0)
    total_amount = models.IntegerField()
    final_amount = models.IntegerField()
    status = models.CharField(choices=STATUS_CHOICE_FIELDS ,default='In progress',max_length=15)
    order_time = models.DateTimeField(auto_now_add=True)
    delivery_time = models.DateField(null=True , blank=True)

    class Meta:
        verbose_name_plural = "سفارش‌ها"

    def __str__(self):
        return f"order #{self.id} - {self.customer.phone}"



"""
    این مدل برای ذخیره ی اطلاعات یک سفارش در دیتابیس استفاده می شود
    هر سفارش شامل 'خدمت ، لباس ، خدمت اضافی و تخفیف هست'

"""
class OrderItems (models.Model):
    order = models.ForeignKey(Orders , on_delete=models.CASCADE , related_name="order_items")
    service = models.ForeignKey(Services , on_delete=models.PROTECT)
    cloth = models.ForeignKey(Clothes , on_delete=models.PROTECT)
    extra_services = models.ManyToManyField(ExtraServices , blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.IntegerField()
    total_price = models.IntegerField()
    is_express = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "آیتم‌های سفارش"

    def __str__(self):
        return f"order item {self.id} - {self.service.name} / {self.cloth.name}"