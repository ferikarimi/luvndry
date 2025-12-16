from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
from ckeditor_uploader.fields import RichTextUploadingField



"""
    این مدل برای عکس های گالری هست
    عکس ها زمان اپلود به فرمت webp تبدیل میشود
    با حذف کردن عکس از گالری ، عکس ها از پروژه پاک میشوند
"""
class GalleryImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='gallery/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "عکس‌های گالری"

    def __str__(self):
        return self.title or f"عکس شماره {self.id}"

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.lower().endswith(".webp"):
            img = Image.open(self.image)
            if img.mode != "RGB":
                img = img.convert("RGB")
            filename = os.path.splitext(self.image.name)[0] + ".webp"
            buffer = BytesIO()
            img.save(buffer, format="WEBP", quality=85)
            buffer.seek(0)
            self.image.save(filename, ContentFile(buffer.read()), save=False)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)


"""
    این مدل برای مقاله ها ساخته شده
    مقاله ها دارای 'تیتر' , 'خلاصه' و 'متن اصلی' هستند
    به کمک 'RichTextUploadingField' ما میتوانیم دسترسی کاملی به متن اصلی مقاله ها داشته باشیم
"""
class MagazineArticle(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان مقاله")
    summary = models.TextField(verbose_name="خلاصه مقاله")
    content = RichTextUploadingField(verbose_name="متن کامل مقاله")
    image = models.ImageField(upload_to='magazine_images/', verbose_name="عکس مقاله")
    is_active = models.BooleanField(default=True, verbose_name="فعال/غیرفعال")

    class Meta:
        verbose_name_plural = "مقاله ها"

    def __str__(self):
        return self.title



"""
    این مدل برای نوتیفیکیشن ها ساخته شده
    نوتیف ها دارای 'تیتر' , 'متن' هستند
"""
class Notification(models.Model):
    title=models.CharField(max_length=150 , verbose_name="عنوان")
    message=models.TextField(verbose_name="متن نوتیف")
    is_active=models.BooleanField(default=False , verbose_name="فعال؟")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "نوتیفیکیشن"
        verbose_name_plural = "نوتیفیکیشن‌ها"
        ordering = ['-created_at']