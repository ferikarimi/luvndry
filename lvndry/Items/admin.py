from django.contrib import admin
from django import forms
from .models import Clothes, Services, ExtraServices, Discount


class ClothesForm(forms.ModelForm):
    class Meta:
        model = Clothes
        fields = '__all__'
        labels = {
            'name': 'نام لباس',
            'base_price': 'قیمت پایه (تومان)',
            'is_active': 'فعال است؟',

        }

class ClothesAdmin(admin.ModelAdmin):
    form = ClothesForm
    list_display = ('name', 'base_price')
    search_fields = ('name',)
    ordering = ('name',)
    fieldsets = (
        ('مشخصات لباس', {'fields': ('name', 'base_price' , 'is_active')}),
    )


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = '__all__'
        labels = {
            'name': 'نام خدمت',
            'price_modifier': 'ضریب قیمت',
            'is_active': 'فعال است؟',
        }

class ServicesAdmin(admin.ModelAdmin):
    form = ServicesForm
    list_display = ('name', 'price_modifier')
    search_fields = ('name',)
    ordering = ('name',)
    fieldsets = (
        ('مشخصات خدمت', {'fields': ('name', 'price_modifier' , 'is_active')}),
    )

class ExtraServicesForm(forms.ModelForm):
    class Meta:
        model = ExtraServices
        fields = '__all__'
        labels = {
            'name': 'نام خدمت اضافه',
            'extra_fee': 'هزینه‌ی اضافی (تومان)',
            'is_active': 'فعال است؟',

        }

class ExtraServicesAdmin(admin.ModelAdmin):
    form = ExtraServicesForm
    list_display = ('name', 'extra_fee')
    search_fields = ('name',)
    ordering = ('name',)
    fieldsets = (
        ('مشخصات خدمت اضافه', {'fields': ('name', 'extra_fee' , 'is_active')}),
    )


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = '__all__'
        labels = {
            'name': 'عنوان تخفیف',
            'percent': 'درصد تخفیف (%)',
            'is_active': 'فعال است؟',

        }

class DiscountAdmin(admin.ModelAdmin):
    form = DiscountForm
    list_display = ('name', 'percent')
    search_fields = ('name',)
    ordering = ('-percent',)
    fieldsets = (
        ('مشخصات تخفیف', {'fields': ('name', 'percent' , 'is_active')}),
    )
