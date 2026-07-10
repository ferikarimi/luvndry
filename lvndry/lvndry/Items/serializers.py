from rest_framework import serializers
from .models import (
    Services , Clothes , ExtraServices , Discount
)



"""
    این میکسین برای بررسی یکتایی فیلد 'نام' در زمان ساخت و ویرایش استفاده می شود
"""
class UniqueNameMixin:

    def validation_name (self , value):
        model = self.Meta.model

        if value in (None, ""):
            return value
        
        if self.instance:
            qs = model.objects.exclude(pk=self.instance.pk)
        else:
            qs = model.objects

        if qs.filter(name=value).exists():
            raise serializers.ValidationError(
                f"ERROR: {model.__name__} '{value}' already axists!!"
            )
        return value



"""
    این سریالایزر برای برای نمایش تمام 'خدمت' های موجود در دیتابیس استفاده می شود
"""
class AllServicesSerializer (serializers.ModelSerializer):
    class Meta :
        model = Services
        fields = '__all__'


"""
    این سریالایزر برای افزودن یک 'خدمت' جدید به دیتابیس استفاده می شود
    همچنین به کمک 'UniqueNameMixin' بررسی میشود که نام 'خدمت' جدید یکتا باشد 
"""
class ServicesAddSerializer (UniqueNameMixin , serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'


"""
    این سریالایزر برای ویرایش یک 'خدمت' استفاده می شود
    همچنین به کمک 'UniqueNameMixin' بررسی میشود که نام 'خدمت' جدید یکتا باشد 
"""
class ServicesEditSerializer (UniqueNameMixin , serializers.ModelSerializer):
    name = serializers.CharField(required=False , allow_blank=True)
    price_modifier = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = Services
        fields = '__all__'



"""
    این سریالایزر برای برای نمایش تمام 'لباس' های موجود در دیتابیس استفاده می شود
"""
class AllClothesSerializer (serializers.ModelSerializer):
    class Meta :
        model = Clothes
        fields = '__all__'


"""
    این سریالایزر برای افزودن یک 'لباس' جدید به دیتابیس استفاده می شود
    همچنین به کمک 'UniqueNameMixin' بررسی میشود که نام 'لباس' جدید یکتا باشد 
"""
class ClothesAddSerializer (UniqueNameMixin , serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = '__all__'


"""
    این سریالایزر برای ویرایش یک 'لباس' استفاده می شود
    همچنین به کمک 'UniqueNameMixin' بررسی میشود که نام 'لباس' جدید یکتا باشد 
"""
class ClothesEditSerializer (UniqueNameMixin , serializers.ModelSerializer):
    name = serializers.CharField(required=False , allow_blank=False)
    base_price = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = Clothes
        fields = '__all__'



"""
    این سریالایزر برای برای نمایش تمام 'خدمت اضافی' های موجود در دیتابیس استفاده می شود
"""
class AllExtraServicesSerializer (serializers.ModelSerializer):
    class Meta :
        model = ExtraServices
        fields = '__all__'


"""
    این سریالایزر برای افزودن یک 'خدمت اضافی' جدید به دیتابیس استفاده می شود
    همچنین به کمک 'UniqueNameMixin' بررسی میشود که نام 'خدمت اضافی' جدید یکتا باشد 
"""
class ExtraServicesAddSerializer (UniqueNameMixin , serializers.ModelSerializer):
    class Meta:
        model = ExtraServices
        fields = '__all__'


"""
    این سریالایزر برای ویرایش یک 'خدمت اضافی' استفاده می شود
    همچنین به کمک 'UniqueNameMixin' بررسی میشود که نام 'خدمت اضافی' جدید یکتا باشد 
"""
class ExtraServicesEditSerializer (UniqueNameMixin , serializers.ModelSerializer):
    name = serializers.CharField(required=False , allow_blank=False)
    extra_fee = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = ExtraServices
        fields = '__all__'



"""
    این سریالایزر برای برای نمایش تمام 'تخفیف' های موجود در دیتابیس استفاده می شود
"""
class AllDiscountSerializer (serializers.ModelSerializer):
    class Meta :
        model = Discount
        fields = '__all__'


"""
    این سریالایزر برای افزودن یک 'تخفیف' جدید به دیتابیس استفاده می شود
    همچنین به کمک 'UniqueNameMixin' بررسی میشود که نام 'تخفیف' جدید یکتا باشد 
"""
class DiscountAddSerializer (UniqueNameMixin , serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


"""
    این سریالایزر برای ویرایش یک 'تخفیف' استفاده می شود
    همچنین به کمک 'UniqueNameMixin' بررسی میشود که نام 'تخفیف' جدید یکتا باشد 
"""
class DiscountEditSerializer(UniqueNameMixin , serializers.ModelSerializer):
    name = serializers.CharField(required=False, allow_blank=True)
    percent = serializers.IntegerField(required=False)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = Discount
        fields = '__all__'