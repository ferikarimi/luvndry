from django.db import models



"""
    این مدل برای ذخیره سازی 'لباس' در دیتابیس هست
"""
class Clothes (models.Model):
    name = models.CharField(max_length=100)
    base_price = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "لباس‌ها"

    def __str__(self):
        return self.name
    

"""
    این مدل برای ذخیره سازی 'خدمت' در دیتابیس هست
"""
class Services (models.Model):
    name = models.CharField(max_length=100)
    price_modifier = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "خدمت"

    def __str__(self):
        return self.name


"""
    این مدل برای ذخیره سازی 'خدمت اضافی' در دیتابیس هست
"""
class ExtraServices (models.Model):
    name = models.CharField(max_length=100)
    extra_fee = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "خدمت اضافه"

    def __str__(self):
        return self.name


"""
    این مدل برای ذخیره سازی 'تخفیف' در دیتابیس هست
"""
class Discount (models.Model):
    name = models.CharField(max_length=100)
    percent = models.PositiveIntegerField("درصد تخفیف")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "تخفیف‌ها"

    def __str__(self):
        return f"name : {self.name} , percent : {self.percent}%"