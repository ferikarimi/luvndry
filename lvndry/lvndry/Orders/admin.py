from django.contrib import admin
from .models import Orders, OrderItems
from django import forms



class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'
        labels = {
            'customer': 'مشتری',
            'discount_amount': 'درصد تخفیف',
            'total_amount': 'مبلغ کل (تومان)',
            'final_amount': 'مبلغ نهایی (تومان)',
            'status': 'وضعیت سفارش',
            'order_time': 'زمان ثبت سفارش',
            'delivery_time': 'تاریخ تحویل',
        }


class OrdersAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ('id', 'customer', 'status_fa', 'final_amount')
    list_filter = ('status',)
    search_fields = ('customer__name', 'customer__phone')
    readonly_fields = ['order_time']
    ordering = ('-order_time',)

    fieldsets = (
        ('اطلاعات مشتری', {'fields': ('customer',)}),
        ('جزئیات سفارش', {
            'fields': (
                'discount_amount', 'total_amount', 'final_amount',
                'status', 'order_time', 'delivery_time'
            )
        }),
    )

    def status_fa(self, obj):
        """نمایش فارسی وضعیت سفارش"""
        return dict(obj.STATUS_CHOICE_FIELDS).get(obj.status, obj.status)
    status_fa.short_description = "وضعیت سفارش"


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItems
        fields = '__all__'
        labels = {
            'order': 'سفارش',
            'service': 'خدمت',
            'cloth': 'لباس',
            'extra_services': 'خدمات اضافه',
            'quantity': 'تعداد',
            'unit_price': 'قیمت واحد',
            'total_price': 'قیمت کل',
            'is_express': 'اکسپرس',
        }


class OrderItemsAdmin(admin.ModelAdmin):
    form = OrderItemForm
    list_display = ('order', 'service', 'cloth', 'quantity', 'total_price', 'is_express')
    list_filter = ('is_express',)
    search_fields = ('order__customer__name', 'service__name', 'cloth__name')
    ordering = ('-order__order_time',)