from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import logging
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from .models import (
    GalleryImage , MagazineArticle , Notification
)
from .serializers import (
    GalleryImageSerializer , MagazineArticleSerializer , NotificationSerializer
)


logger = logging.getLogger('cms')



"""
    این ویو برای نمایش تمام عکس های گالری و افزودن یک تصویر به گالری هست
    دسترسی فقط برای ادمین مجاز است
"""
class GalleryImageListCreate(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            images = GalleryImage.objects.all()
            serializer = GalleryImageSerializer(images, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"خطا در دریافت لیست تصاویر گالری توسط {request.user.username}: {e}", exc_info=True)
            return Response({"error": "خطا در دریافت اطلاعات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = GalleryImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"تصویر جدید '{serializer.data.get('title')}' توسط {request.user.username} ایجاد شد.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"ارسال داده نامعتبر برای افزودن تصویر توسط {request.user.username}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
    این ویو برای مشاهده، ویرایش (کامل یا جزئی) و حذف یک تصویر مشخص استفاده می‌شود
    دسترسی فقط برای ادمین مجاز است
"""
class GalleryImageDetail(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self ,pk):
        return get_object_or_404(GalleryImage , pk=pk)
    
    def get(self, request, pk):
        try:
            image = get_object_or_404(GalleryImage, pk=pk)
            serializer = GalleryImageSerializer(image)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"خطا در یافتن تصویر با شناسه {pk}: {e}", exc_info=True)
            return Response({"error": "تصویر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        image = self.get_object(pk)
        serializer = GalleryImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"تصویر {pk} توسط {request.user.username} به‌روزرسانی جزئی شد.")
            return Response(serializer.data)
        else:
            logger.warning(f"به‌روزرسانی نامعتبر تصویر {pk} توسط {request.user.username}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            image = self.get_object(pk)
            image.delete()
            logger.info(f"تصویر {pk} توسط {request.user.username} حذف شد.")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"خطا در حذف تصویر {pk} توسط {request.user.username}: {e}", exc_info=True)
            return Response({"error": "خطا در حذف تصویر"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



"""
    این ویو برای مشاهده(فعال، غیرفعال و همه)، ویرایش (کامل یا جزئی) و حذف مقاله ها استفاده می‌شود
    مقاله ها امکان حذف نرم "soft delete" را دارند
    با امکان فیلتر مقالات غیرفعال
    دسترسی فقط برای ادمین مجاز است
"""
class AdminMagazine(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            filter_type = request.query_params.get('inactive', None)

            if filter_type == 'true':
                articels = MagazineArticle.objects.filter(is_active=False).order_by('-id')
            elif filter_type == 'false':
                articels = MagazineArticle.objects.filter(is_active=True).order_by('-id')
            else:
                articels = MagazineArticle.objects.all().order_by('-id')

            serializer = MagazineArticleSerializer(
                articels, many=True, context={'request': request}
            )

            logger.info(f"دریافت لیست مقالات مجله توسط {request.user.username} انجام شد.")
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"خطا در دریافت لیست مقالات مجله توسط {request.user.username}: {e}",
                         exc_info=True)
            return Response({"error": "خطا در دریافت اطلاعات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = MagazineArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            logger.info(
                f"مقاله جدید با عنوان '{serializer.data.get('title')}' "
                f"توسط {request.user.username} ایجاد شد."
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.warning(
                f"ارسال داده نامعتبر برای ایجاد مقاله مجله توسط {request.user.username}"
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        pk = request.data.get('id')
        if not pk:
            logger.warning(f"بدون ارسال ID برای ویرایش مقاله توسط {request.user.username}")
            return Response({'error': 'Article ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            article = MagazineArticle.objects.get(pk=pk)
        except MagazineArticle.DoesNotExist:
            logger.warning(f"مقاله با شناسه {pk} برای ویرایش توسط {request.user.username} یافت نشد.")
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MagazineArticleSerializer(
            article, data=request.data, partial=True, context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            logger.info(f"مقاله {pk} توسط {request.user.username} ویرایش شد.")
            return Response(serializer.data)
        else:
            logger.warning(
                f"ارسال داده نامعتبر برای ویرایش مقاله {pk} توسط {request.user.username}"
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request.data.get('id')
        if not pk:
            logger.warning(f"درخواست حذف بدون ارسال ID توسط {request.user.username}")
            return Response({'error': 'Article ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            article = MagazineArticle.objects.get(pk=pk)
        except MagazineArticle.DoesNotExist:
            logger.warning(f"مقاله با شناسه {pk} برای حذف توسط {request.user.username} پیدا نشد.")
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

        article.is_active = False
        article.save()
        logger.info(f"مقاله {pk} توسط {request.user.username} به صورت نرم حذف (Soft Delete) شد.")
        return Response({'message': 'Article soft-deleted successfully'})



"""
    این ویو برای نمایش مقاله ها در صفحه عمومی سایت هست
    فقط مقاله های فعال نمایش داده می شود
"""
class Magazine(APIView):
    def get(self, request):
        articles = MagazineArticle.objects.filter(is_active=True).order_by('-id')
        serializer = MagazineArticleSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)



"""
    این ویو برای ساخت و مشاهده ی تمام نوتیف های سایت استفاده می شود
    دسترسی فقط برای ادمین مجاز است
"""
class NotificationListCreate(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            notifications = Notification.objects.all()
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"خطا در دریافت لیست نوتیفیکیشن‌ها توسط {request.user.username}: {e}", exc_info=True)
            return Response({"error": "خطا در دریافت اطلاعات"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(
                f"نوتیفیکیشن جدید با عنوان '{serializer.data.get('title')}' "
                f"توسط {request.user.username} ایجاد شد."
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"داده نامعتبر برای ایجاد نوتیفیکیشن توسط {request.user.username}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
    این ویو برای مدیریت کامل نوتیف های سایت استفاده می شود
    امکان ویرایش و حذف را دارد
    دسترسی فقط برای ادمین مجاز است
"""
class NotificationDetail(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Notification.objects.get(pk=pk)
        except Notification.DoesNotExist:
            logger.warning(f"نوتیفیکیشن با شناسه {pk} پیدا نشد.")
            return None

    def get(self, request, pk):
        notif = self.get_object(pk)
        if not notif:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        logger.info(f"نوتیفیکیشن {pk} توسط {request.user.username} مشاهده شد.")
        serializer = NotificationSerializer(notif)
        return Response(serializer.data)

    def patch(self, request, pk):
        notif = self.get_object(pk)
        if not notif:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationSerializer(notif, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(
                f"نوتیفیکیشن {pk} توسط {request.user.username} ویرایش شد."
            )
            return Response(serializer.data)
        else:
            logger.warning(
                f"داده نامعتبر برای ویرایش نوتیفیکیشن {pk} توسط {request.user.username}"
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        notif = self.get_object(pk)
        if not notif:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        notif.delete()
        logger.info(f"نوتیفیکیشن {pk} توسط {request.user.username} حذف شد.")
        return Response({"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)



"""
    این ویو برای بازگرداندن آخرین نوتیف فعال است
    در صفحه عمومی سایت استفاده می شود
"""
class ShowLastNotif(APIView):
    def get(self , request):
        notif = Notification.objects.filter(is_active=True).order_by('-created_at').first()
        if notif :
            serializer = NotificationSerializer(notif)
            return Response(serializer.data)
        return Response({"message: no active notifications"},status=status.HTTP_404_NOT_FOUND)