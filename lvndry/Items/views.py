from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from rest_framework.permissions import IsAdminUser 
from .models import (
    Clothes , Services , ExtraServices , Discount
)
from .serializers import (
    AllClothesSerializer , AllServicesSerializer , ServicesAddSerializer , AllExtraServicesSerializer , ServicesEditSerializer , ClothesAddSerializer , ClothesEditSerializer  , ExtraServicesAddSerializer , ExtraServicesEditSerializer , AllDiscountSerializer , DiscountAddSerializer , DiscountEditSerializer
)


logger = logging.getLogger('items')



"""
    این ویو برای دریافت ، ساخت ، ویرایش و حذف کردن 'خدمت' استفاده میشود
    دسترسی فقط برای ادمین مجاز است
    حذف 'خدمت' به صورت نرم (غیرفعال‌سازی) انجام می شود
"""
class ServicesManagment(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, id=None):
        if id:
            logger.info(f"درخواست مشاهده خدمت با شناسه {id} توسط {request.user.username if request.user.is_authenticated else 'کاربر ناشناس'}")
            try:
                service = Services.objects.get(id=id)
                serializer = AllServicesSerializer(service)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Services.DoesNotExist:
                logger.warning(f"خدمت با شناسه {id} یافت نشد.")
                return Response({"error": "Service not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        logger.info(f"درخواست ایجاد خدمت جدید توسط {request.user.username if request.user.is_authenticated else 'کاربر ناشناس'}")
        serializer = ServicesAddSerializer(data=request.data)
        if serializer.is_valid():
            service = serializer.save()
            logger.info(f"خدمت جدید '{service.name}' ایجاد شد.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"داده نامعتبر در ایجاد خدمت: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        if not id:
            logger.warning("درخواست به‌روزرسانی خدمت بدون ارسال شناسه.")
            return Response({"error": "Service ID is required for update."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = Services.objects.get(id=id)
        except Services.DoesNotExist:
            logger.warning(f"خدمت با شناسه {id} یافت نشد.")
            return Response({"error": "Service not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ServicesEditSerializer(service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"خدمت '{service.name}' با شناسه {id} با موفقیت ویرایش شد.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        logger.warning(f"داده نامعتبر در ویرایش خدمت {id}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            logger.warning("درخواست حذف خدمت بدون ارسال شناسه.")
            return Response({"error": "Service ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            service = Services.objects.get(id=id)
            service.is_active = False
            service.save()
            logger.info(f"خدمت '{service.name}' با شناسه {id} غیرفعال شد (حذف نرم).")
            return Response({"message": f"Service '{service.name}' deleted successfully."}, status=status.HTTP_200_OK)
        
        except Services.DoesNotExist:
            logger.warning(f"خدمت با شناسه {id} یافت نشد.")
            return Response({"error": "Service not found."}, status=status.HTTP_404_NOT_FOUND)



"""
    این ویو برای دریافت ، ساخت ، ویرایش و حذف کردن 'لباس' استفاده میشود
    دسترسی فقط برای ادمین مجاز است
    حذف 'لباس' به صورت نرم (غیرفعال‌سازی) انجام می شود
"""
class ClothesManagment(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, id=None):
        if id:
            logger.info(f"درخواست مشاهده لباس با شناسه {id} توسط {request.user.username if request.user.is_authenticated else 'کاربر ناشناس'}")
            try:
                clothes = Clothes.objects.get(id=id)
                serializer = AllClothesSerializer(clothes)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            except Clothes.DoesNotExist:
                logger.warning(f"لباس با شناسه {id} یافت نشد.")
                return Response({"error": "Cloth not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        logger.info(f"درخواست ایجاد لباس جدید توسط {request.user.username if request.user.is_authenticated else 'کاربر ناشناس'}")
        serializer = ClothesAddSerializer(data=request.data)
        if serializer.is_valid():
            clothes = serializer.save()
            logger.info(f"لباس جدید '{clothes.name}' ایجاد شد.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"داده نامعتبر در ایجاد لباس: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        if not id:
            logger.warning("درخواست به‌روزرسانی لباس بدون ارسال شناسه.")
            return Response({"error": "Cloth ID is required for update."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            clothes = Clothes.objects.get(id=id)
        except Clothes.DoesNotExist:
            logger.warning(f"لباس با شناسه {id} یافت نشد.")
            return Response({"error": "Cloth not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClothesEditSerializer(clothes, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"لباس '{clothes.name}' با شناسه {id} با موفقیت ویرایش شد.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        logger.warning(f"داده نامعتبر در ویرایش لباس {id}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            logger.warning("درخواست حذف لباس بدون ارسال شناسه.")
            return Response({"error": "Cloth ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            clothes = Clothes.objects.get(id=id)
            clothes.is_active = False
            clothes.save()
            logger.info(f"لباس '{clothes.name}' با شناسه {id} غیرفعال شد (حذف نرم).")
            return Response({"message": f"Cloth '{clothes.name}' deleted successfully."}, status=status.HTTP_200_OK)
        
        except Clothes.DoesNotExist:
            logger.warning(f"لباس با شناسه {id} یافت نشد.")
            return Response({"error": "Cloth not found."}, status=status.HTTP_404_NOT_FOUND)



"""
    این ویو برای دریافت ، ساخت ، ویرایش و حذف کردن 'خدمات اضافی' استفاده میشود
    دسترسی فقط برای ادمین مجاز است
    حذف 'خدمات اضافی' به صورت نرم (غیرفعال‌سازی) انجام می شود
"""
class ExtraServicesManagment(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, id=None):
        if id:
            logger.info(f"درخواست مشاهده خدمت اضافی با شناسه {id} توسط {request.user.username if request.user.is_authenticated else 'کاربر ناشناس'}")
            try:
                extra_service = ExtraServices.objects.get(id=id)
                serializer = AllExtraServicesSerializer(extra_service)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            except ExtraServices.DoesNotExist:
                logger.warning(f"خدمت اضافی با شناسه {id} یافت نشد.")
                return Response({"error": "Extra Service not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        logger.info(f"درخواست ایجاد خدمت اضافی جدید توسط {request.user.username if request.user.is_authenticated else 'کاربر ناشناس'}")
        serializer = ExtraServicesAddSerializer(data=request.data)
        if serializer.is_valid():
            extra_service = serializer.save()
            logger.info(f"خدمت اضافی جدید '{extra_service.name}' ایجاد شد.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"داده نامعتبر در ایجاد خدمت اضافی: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        if not id:
            logger.warning("درخواست به‌روزرسانی خدمت اضافی بدون ارسال شناسه.")
            return Response({"error": "Extra Service ID is required for update."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            extra_service = ExtraServices.objects.get(id=id)
        except ExtraServices.DoesNotExist:
            logger.warning(f"خدمت اضافی با شناسه {id} یافت نشد.")
            return Response({"error": "Extra Service not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExtraServicesEditSerializer(extra_service, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"خدمت اضافی '{extra_service.name}' با شناسه {id} با موفقیت ویرایش شد.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        logger.warning(f"داده نامعتبر در ویرایش خدمت اضافی {id}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            logger.warning("درخواست حذف خدمت اضافی بدون ارسال شناسه.")
            return Response({"error": "Extra Service ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            extra_service = ExtraServices.objects.get(id=id)
            extra_service.is_active = False
            extra_service.save()
            logger.info(f"خدمت اضافی '{extra_service.name}' با شناسه {id} غیرفعال شد (حذف نرم).")
            return Response({"message": f"Extra Service '{extra_service.name}' deleted successfully."}, status=status.HTTP_200_OK)
        
        except ExtraServices.DoesNotExist:
            logger.warning(f"خدمت اضافی با شناسه {id} یافت نشد.")
            return Response({"error": "Extra Service not found."}, status=status.HTTP_404_NOT_FOUND)



"""
    این ویو برای دریافت ، ساخت ، ویرایش و حذف کردن 'تخفیف' استفاده میشود
    دسترسی فقط برای ادمین مجاز است
    حذف 'تخفیف' به صورت نرم (غیرفعال‌سازی) انجام می شود
"""
class DiscountManagment(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, id=None):
        if id:
            logger.info(f"درخواست مشاهده تخفیف با شناسه {id} توسط {request.user.username if request.user.is_authenticated else 'کاربر ناشناس'}")
            try:
                discount = Discount.objects.get(id=id)
                serializer = AllDiscountSerializer(discount)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            except Discount.DoesNotExist:
                logger.warning(f"تخفیف با شناسه {id} یافت نشد.")
                return Response({"error": "Discount not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        logger.info(f"درخواست ایجاد تخفیف جدید توسط {request.user.username if request.user.is_authenticated else 'کاربر ناشناس'}")
        serializer = DiscountAddSerializer(data=request.data)
        if serializer.is_valid():
            discount = serializer.save()
            logger.info(f"تخفیف جدید '{discount.name}' ایجاد شد.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"داده نامعتبر در ایجاد تخفیف: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        if not id:
            logger.warning("درخواست به‌روزرسانی تخفیف بدون ارسال شناسه.")
            return Response({"error": "Discount ID is required for update."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            discount = Discount.objects.get(id=id)
        except Discount.DoesNotExist:
            logger.warning(f"تخفیف با شناسه {id} یافت نشد.")
            return Response({"error": "Discount not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DiscountEditSerializer(discount, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"تخفیف '{discount.name}' با شناسه {id} با موفقیت ویرایش شد.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        logger.warning(f"داده نامعتبر در ویرایش تخفیف {id}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            logger.warning("درخواست حذف تخفیف بدون ارسال شناسه.")
            return Response({"error": "Discount ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            discount = Discount.objects.get(id=id)
            discount.is_active = False
            discount.save()
            logger.info(f"تخفیف '{discount.name}' با شناسه {id} غیرفعال شد (حذف نرم).")
            return Response({"message": f"Discount '{discount.name}' deleted successfully."}, status=status.HTTP_200_OK)
        
        except Discount.DoesNotExist:
            logger.warning(f"تخفیف با شناسه {id} یافت نشد.")
            return Response({"error": "Discount not found."}, status=status.HTTP_404_NOT_FOUND)



"""
    این ویو برای واکشی داده های مورد نیاز برای صفحه ی ثبت سفارش است
    تمام "لباس ها" ، "خدمات" ، "خدمات اضافی" و "تخفیف ها" را نمایش میدهد
    دسترسی فقط برای ادمین مجاز است
"""
class OrderPageData (APIView):
    permission_classes = [IsAdminUser]

    def get (self , request):
        all_services = Services.objects.filter(is_active=True).order_by('id')
        all_clothes = Clothes.objects.filter(is_active=True).order_by('id')
        all_extraservices = ExtraServices.objects.filter(is_active=True).order_by('id')
        all_discount = Discount.objects.filter(is_active=True).order_by('id')

        return Response ({
            "services": AllServicesSerializer(all_services , many=True).data ,
            "clothes": AllClothesSerializer(all_clothes , many=True).data ,
            "extraservice": AllExtraServicesSerializer(all_extraservices , many=True).data ,
            "discount": AllDiscountSerializer(all_discount , many=True).data ,
        }, status=status.HTTP_200_OK)



"""
    برای مشاهده آیتم‌های غیرفعال (حذف نرم) در سیستم استفاده می شود
    سرویس‌ها ، لباس‌ها ، خدمات اضافی و تخفیف‌های غیر فعال را برمی‌گرداند
    دسترسی فقط برای ادمین مجاز است
"""
class DeletedItems(APIView):
    permission_classes = [IsAdminUser]

    def get (self , request):
        deleted_services = Services.objects.filter(is_active=False)
        deleted_clothes = Clothes.objects.filter(is_active=False)
        deleted_extraservices = ExtraServices.objects.filter(is_active=False)
        deleted_discount = Discount.objects.filter(is_active=False)

        return Response({
            "services": AllServicesSerializer(deleted_services, many=True).data,
            "extras": AllExtraServicesSerializer(deleted_extraservices, many=True).data,
            "clothes": AllClothesSerializer(deleted_clothes, many=True).data,
            "discounts": AllDiscountSerializer(deleted_discount, many=True).data,
        }, status=status.HTTP_200_OK)