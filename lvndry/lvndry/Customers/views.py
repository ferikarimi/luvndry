from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
import logging
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from .models import (
    Customers , Comments
)
from .serializers import (
    CustomerUpdateProfileSerializer , CustomerRegisterSerializer , CustomerInfoSerializer , CommentCreateSerializer , CommentAdminSerializer , CommentRecentlySerializer , AllCustomersSerializer
)



logger = logging.getLogger('customers')



"""
    این ویو برای ثبت نام یک مشتری جدید در سایت استفاده می شود
    دسترسی فقط برای ادمین مجاز است
"""
class CustomerRegister(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        logger.info(f"درخواست ثبت‌نام مشتری جدید توسط {request.user if request.user.is_authenticated else 'کاربر ناشناس'}")
        serializer = CustomerRegisterSerializer(data=request.data)

        if serializer.is_valid():
            customer = serializer.save()
            logger.info(f"مشتری جدید با کد {customer.code} ثبت شد.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning(f"داده نامعتبر در ثبت‌نام مشتری: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
    این ویو برای گرفتن یک مشتری خاص با کد مشتری و ویرایش کردن اطلاعات آن استفاده می شود
    دسترسی فقط برای ادمین مجاز است
"""
class CustomerUpdateProfile(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            logger.warning("درخواست مشاهده پروفایل بدون ارسال کد مشتری.")
            return Response({"error": "code is required."}, status=status.HTTP_400_BAD_REQUEST)

        customer = get_object_or_404(Customers, code=code)
        logger.info(f"پروفایل مشتری با کد {code} واکشی شد.")
        serializer = CustomerUpdateProfileSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        data = request.data.copy()
        code = data.pop('code', None)
        if not code:
            logger.warning("درخواست به‌روزرسانی پروفایل بدون ارسال کد مشتری.")
            return Response({"error": "code is required."}, status=status.HTTP_400_BAD_REQUEST)

        customer = get_object_or_404(Customers, code=code)
        serializer = CustomerUpdateProfileSerializer(customer, data=data, partial=True)
        if not serializer.is_valid():
            logger.warning(f"داده نامعتبر در به‌روزرسانی پروفایل مشتری {code}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        logger.info(f"پروفایل مشتری {code} با موفقیت به‌روزرسانی شد.")
        return Response(serializer.data, status=status.HTTP_200_OK)



"""
    این ویو برای حذف یک مشتری از دیتابیس استفاده می شود
    دسترسی فقط برای ادمین مجاز است
"""
class CustomerDelete(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, code):
        logger.warning(f"درخواست حذف مشتری با کد {code} توسط {request.user if request.user.is_authenticated else 'کاربر ناشناس'}")
        customer = get_object_or_404(Customers, code=code)
        customer.delete()
        logger.info(f"مشتری با کد {code} با موفقیت حذف شد.")
        return Response({"message": "Customer deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



"""
    این ویو برای ثبت یک کامنت جدید توسط یک مشتری است
    اگر مشتری از خدمات ما استفاده نکرده باشد ، نمیتواند نظری ثبت کند
"""
class CustomerCommentsCreate(APIView):

    def post(self, request):
        logger.info(f"درخواست ثبت کامنت جدید توسط {request.user if request.user.is_authenticated else 'کاربر ناشناس'}")
        serializer = CommentCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            logger.info("کامنت جدید با موفقیت ثبت شد و در انتظار تأیید است.")
            return Response(
                {"MESSAGE": "Your comment has been submitted and will be displayed after approval."},
                status=status.HTTP_201_CREATED
            )

        logger.warning(f"داده نامعتبر در ثبت کامنت: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
    ادمین به کمک این ویو میتواند وضعیت کامنت ها را تغییر دهد
    کامنت هایی که تایید شده باشد روی سایت نمایش داده می شوند
    دسترسی فقط برای ادمین مجاز است
"""
class AdminCommentStatus(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        logger.info(f"ادمین {request.user.username if request.user.is_authenticated else 'ناشناس'} درخواست تغییر وضعیت کامنت با شناسه {pk} را ارسال کرد.")
        try:
            comment = Comments.objects.get(id=pk)
        except Comments.DoesNotExist:
            logger.warning(f"کامنت با شناسه {pk} یافت نشد.")
            return Response({"error": "comment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentAdminSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"وضعیت کامنت {pk} با موفقیت به‌روزرسانی شد.")
            return Response(serializer.data, status=status.HTTP_200_OK)

        logger.warning(f"داده نامعتبر برای ویرایش کامنت {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
    پانزده نظر اخیر که ثبت شده و توسط ادمین تایید شده اند، روی سایت نمایش داده می شوند
"""
class CommentRecently(APIView):
    def get(self, request):
        recent_comments = Comments.objects.filter(status='approved').order_by('-created_at')[:15]
        serializer = CommentRecentlySerializer(recent_comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



"""
    این ویو برای پیدا کردن مشتری بر اساس "کد مشتری" ، "شماره تلفن مشتری" و "نام مشتری" است
    جستجو بر اساس 'fullname' و 'phone' و 'code' جزئی است:
    دسترسی فقط برای ادمین مجاز است
"""
class AllCustomers(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        search_query = request.GET.get('search', '').strip()
        customers = Customers.objects.all().order_by('id')

        if search_query:
            customers = customers.filter(
                Q(fullname__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(code__icontains=search_query)
            )
            logger.debug(f"تعداد مشتریان مطابق با فیلتر '{search_query}': {customers.count()}")

        paginator = PageNumberPagination()
        paginator.page_size = 12
        result_page = paginator.paginate_queryset(customers, request)
        serializer = AllCustomersSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



"""
    این کلاس برای صفحه بندی کردن کامت ها است
"""
class CommentPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'  
    max_page_size = 60



"""
    این ویو برای نمایش تمام کامنت ها برای ادمین است
    دسترسی فقط برای ادمین مجاز است
"""
class AdminCommentList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        logger.info(f"ادمین {request.user.username if request.user.is_authenticated else 'ناشناس'} درخواست مشاهده‌ی لیست همه‌ی کامنت‌ها را ارسال کرد.")
        comments = Comments.objects.all().order_by('-created_at')
        paginator = CommentPagination()
        result_page = paginator.paginate_queryset(comments, request)
        serializer = CommentAdminSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



"""
    این ویو برای نمایش تعداد مشتری های سطح برنزی، نقره ای و طلایی است
"""
class CustomerLevel(APIView):
    def get(self , request):
        bronze = silver = gold = 0

        for customer in Customers.objects.all():
            order_count = customer.orders.count()

            if 10 <= order_count < 20 :
                bronze += 1
            elif 20 <= order_count < 30 :
                silver += 1
            elif 30 <= order_count :
                gold += 1

        data = {
            "bronze":bronze,
            "silver":silver,
            "gold":gold
        }
        return Response(data)