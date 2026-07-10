from rest_framework import serializers
from .models import (
    GalleryImage , MagazineArticle , Notification
    )


"""
    برای ارسال و دریافت عکس ها بین دیتابیس و فرانت‌اند استفاده می‌شوند
    تبدیل داده‌های مدل GalleryImage به JSON و برعکس.
"""
class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'title', 'image', 'is_active', 'created_at']


"""
    برای ارسال و دریافت مقاله ها بین دیتابیس و فرانت‌اند استفاده می‌شوند
    تبدیل داده‌های مدل MagazineArticle به JSON و برعکس.
"""
class MagazineArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MagazineArticle
        fields = ['id', 'title', 'summary', 'content', 'image', 'is_active']



"""
    این سریالایزر برای ارسال و دریافت نوتیف ها بین دیتابیس و فرانت‌اند استفاده می شود 
"""
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"