from django.db import models
import re
from django.core.exceptions import ValidationError



"""
    از این فانکشن برای ذخیره ی شماره تلفن های مشتری ها به صورت 09123456789 استفاده می شود
"""
def validate_iran_phone(value):
    if not re.match(r"^09\d{9}$" , value):
        raise ValidationError("شماره تلفن معتبر نیست!")



"""
    این جدول برای سطح بندی مشتری ها است
"""
class CustomerLevel (models.Model):
    name = models.CharField(max_length=50)
    discount_percent = models.PositiveIntegerField()
    
    class Meta:
        verbose_name_plural = "سطح مشتریان"
    def __str__(self):
        return self.name



"""
    این مدل برای مشتری های سایت ساخته شده
    مشتری ها بر اساس شماره تلفن های منحصر به فرد شناخته می شوند
"""
class Customers (models.Model):

    fullname = models.CharField(max_length=255 , null=True , blank=True)
    phone = models.CharField(unique=True , max_length=11 , validators=[validate_iran_phone])
    address = models.CharField(max_length=255 , null=True , blank=True)
    level = models.ForeignKey(CustomerLevel , on_delete=models.PROTECT , related_name="customers" , null=True , blank=True)
    code = models.PositiveIntegerField(unique=True , null=True , blank=True)

    class Meta:
        verbose_name_plural = "مشتریان"

    def __str__(self):
        return f"{self.fullname}"







"""
    این مدل برای کامنت های مشتری های سایت ساخته شده
    هر مشتری میتواند چندین کامنت داشته باشد
"""
class Comments (models.Model):
    STATUS_CHOICE = [
        ('pending','در انتظار بررسی'),
        ('approved','تأیید شده'),
        ('rejected','رد شده')
    ]
    customer = models.ForeignKey(Customers , on_delete=models.CASCADE , related_name='comments')
    text = models.TextField()
    status = models.CharField(choices=STATUS_CHOICE , default='pending' , max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"comment by {self.customer.phone} : {self.status}."