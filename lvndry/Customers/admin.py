from django.contrib import admin
from .models import Customers, Comments


class CustomersAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'phone', 'code')
    search_fields = ('fullname', 'phone', 'code')
    ordering = ('fullname',)
    fieldsets = (
        ('اطلاعات مشتری', {
            'fields': ('fullname', 'phone', 'code', 'address')
        }),
    )
    readonly_fields = ()


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__fullname', 'customer__phone', 'text')
    ordering = ('-created_at',)
    list_editable = ('status',)
    readonly_fields = ('created_at',)