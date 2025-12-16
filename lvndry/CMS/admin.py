from django.contrib import admin
from .models import GalleryImage , MagazineArticle , Notification
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    ordering = ('-created_at',)

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'image', 'is_active'),
            'description': 'اطلاعات مربوط به هر عکس گالری'
        }),
        ('تاریخ ثبت', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'preview_image')

    def preview_image(self, obj):
        """نمایش تصویر بندانگشتی در پنل ادمین"""
        if obj.image:
            return f'<img src="{obj.image.url}" width="100" style="border-radius:8px;" />'
        return "بدون تصویر"

    preview_image.allow_tags = True
    preview_image.short_description = "پیش‌نمایش تصویر"




class MagazineArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('id','is_active')
    search_fields = ('title',)
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'content', 'is_active'),
            'description': 'اطلاعات مربوط به مقاله'
        }),
    )




class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'message')
    list_editable = ('is_active',)
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'message', 'is_active'),
            'description': 'اطلاعات مربوط به نوتیفیکیشن'
        }),
        ('تاریخ ثبت', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)