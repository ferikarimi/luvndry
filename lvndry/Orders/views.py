import logging
from django.db.models import Count , Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Orders, OrderItems
from Customers.models import Customers
from django.db.models import Case, When, Value, IntegerField
from rest_framework.pagination import PageNumberPagination
from datetime import date
import jdatetime
from django.db.models import Sum
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .serializers import (
    OrderUpdateSerializer, OrderCreateSerializer, OrderTrackingSerializer, OrderStatusUpdateSerializer,
    OrderSerializer, CustomerSerializer,
    AllActiveOrdersListSerializer, OrderDetailSerializer , CheckCustomerSerializer
)


logger = logging.getLogger('Orders')



"""
    از این ویو برای ثبت سفارش جدید استفاده می شود
    دسترسی فقط برای ادمین مجاز است
"""
class OrderCreate(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        logger.info(f"[User: {request.user.username}] [Action: Create Order]")

        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("[Order] سفارش جدید با موفقیت ایجاد شد.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f"[Order] داده نامعتبر هنگام ایجاد سفارش: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



"""
    این ویو برای بررسی اطلاعات مشتری بر اساس شماره تلفن استفاده می شود
    اگر مشتری وجود داشته باشد ، اطلاعات مشتری نمایش داده می شود
    اگر مشتری وجود نداشته باشد ، بدون هیچ خطایی اطلاع میدهد که مشتری ثبت نشده است
    دسترسی فقط برای ادمین مجاز است
"""
class CheckCustomer(APIView):
    permission_classes = [IsAdminUser]

    # def get(self, request):
    #     phone = request.query_params.get("phone")

    #     if not phone:
    #         return Response({"detail": "Phone is required."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         customer = Customers.objects.get(phone=phone)
    #     except Customers.DoesNotExist:
    #         return Response({"exists": False}, status=status.HTTP_200_OK)

    #     data = CheckCustomerSerializer(customer).data

    #     return Response({"exists": True, "customer": data})

    def get(self, request):
        phone = request.query_params.get("phone")

        if not phone:
            return Response({"detail": "Phone is required."}, status=400)

        try:
            customer = Customers.objects.get(phone=phone)

            serializer = CheckCustomerSerializer(customer)

            return Response({
                "exists": True,
                "customer": serializer.data
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
        
        
        
        
        
        
        

"""
    از این ویو برای نمایش اعداد در داخل صفحه ی عمومی سایت توی قسمت 'باشگاه مشتریان' استفاده می شود
"""
class Stats(APIView):
    def get(self, request):
        start_days = 0
        start_orders = 38342
        start_items = 89796

        reference_date = date(2010, 1, 1)
        days_passed = (date.today() - reference_date).days
        total_days = start_days + (days_passed //6 ) * 6

        orders_count = Orders.objects.count()
        total_orders = start_orders + (orders_count // 11 ) * 11 

        items_count = OrderItems.objects.aggregate(total=Sum("quantity"))["total"] or 0
        total_items = start_items + (items_count //11) * 11
        
        return Response({
            "days": total_days,
            "orders": total_orders,
            "items": total_items,
        })



"""
    از این ویو برای بررسی وضعیت اخرین سفارش مشتری در صفحه ی عمومی استفاده می شود
"""
class OrderTracking (APIView):
    def post (self , request):
        serializer = OrderTrackingSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data , status=status.HTTP_200_OK)
        return Response (serializer.errors , status=status.HTTP_400_BAD_REQUEST)



"""
    از این ویو برای نمایش تمام سفارشات یک مشتری خاص استفاده می شود
    همچنین تمام اطلاعات مشتری نمایش داده می شود
    دسترسی فقط برای ادمین مجاز است
"""
class CustomerOrders(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, id):
        try:
            customer = Customers.objects.get(id=id)
        except Customers.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        orders = Orders.objects.filter(customer=customer) \
            .prefetch_related('order_items__service', 'order_items__cloth', 'order_items__extra_services') \
            .annotate(
                delivered_order=Case(
                    When(status="Delivered", then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ).order_by("-delivered_order", "-order_time")
  

        orders_serialized = OrderSerializer(orders, many=True).data
        customer_serialized = CustomerSerializer(customer).data

        return Response({
            'customer': customer_serialized,
            'orders': orders_serialized
        }, status=status.HTTP_200_OK)



"""
    این ویو تمام اطلاعات سفارش و آیتم های آن و خدمات اضافی و اطلاعات مشتری را نمایش می دهد
    دسترسی فقط برای ادمین مجاز است
"""
class OrderDetail(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, pk):
        try:
            order = Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            return Response({'error': 'سفارش یافت نشد'}, status=404)

        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=200)



"""
    این ویو تمام سفارشاتی که تحویل داده نشده اند را نشان می دهد
    امکان جست و جو از طریق کد مشتری ، نام مشتری ، شماره سفارش و تاریخ ثبت سفارش وجود دارد
    نتایج به صورت 30 تایی فرستاده می شود
    امکان فیلتر کردن بر اساس 'عجله ای' بودن ، وجود دارد
    دسترسی فقط برای ادمین مجاز است
"""
class AllActiveOrdersList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        delivered = request.GET.get("delivered")
        
        if delivered and delivered.lower() in ["true","1"] :
            queryset = Orders.objects.filter(status="Delivered").order_by("-order_time")
        
        else :
            queryset = Orders.objects.filter(status__in=["In progress","Completed"])
        
        
        
        queryset = queryset.select_related("customer","customer__level").annotate(delivered_orders_count=Count("customer__orders",filter=Q(customer__orders__status="Delivered")))

        is_express = request.GET.get('is_express')
        if is_express and is_express.lower() in ['true', '1']:
            queryset = queryset.filter(order_items__is_express=True)

        customer_code = request.GET.get('customer_code', '').strip()
        customer_name = request.GET.get('customer_name', '').strip()
        order_id = request.GET.get('order_id', '').strip()
        order_date = request.GET.get('order_date', '').strip()

        if customer_code:
            queryset = queryset.filter(customer__code__icontains=customer_code)
        if customer_name:
            queryset = queryset.filter(customer__fullname__icontains=customer_name)
        if order_id:
            queryset = queryset.filter(id=order_id)
        if order_date:
            try:
                g_date = jdatetime.datetime.strptime(order_date, "%Y/%m/%d").togregorian().date()
                queryset = queryset.filter(order_time__date=g_date)
            except Exception:
                queryset = queryset.filter(order_time__date=order_date)

        queryset = queryset.prefetch_related('order_items', 'order_items__service', 'order_items__cloth', 'order_items__extra_services')

        if delivered and delivered.lower() in ["true" , "1"] :
            queryset = queryset.order_by("-order_time")[:50]
        else :
            queryset = queryset.order_by("-order_time")
            
        paginator = PageNumberPagination()

        if delivered and delivered.lower() in ["true" , "1"] :
            paginator.page_size = 25
        else :
            paginator.page_size = 30
            
            
            
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = AllActiveOrdersListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



"""
    از این ویو برای مدیریت سفارش ها استفاده می شود
    جزئیات یک سفارش دریافت می شود و میتوان آن را ویرایش جزئی کرد
    میتوان یک سفارش را حذف کرد
    دسترسی فقط برای ادمین مجاز است
"""
class OrderManagment(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            return None

    def get(self, request, pk):
        logger.info(f"[User: {request.user.username}] [Action: Retrieve Order] ID: {pk}")
        order = self.get_object(pk)
        if not order:
            logger.warning(f"[Order] سفارش {pk} یافت نشد.")
            return Response({"error": f"Order '{pk}' not found!"}, status=404)
        serializer = OrderUpdateSerializer(order)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        logger.info(f"[User: {request.user.username}] [Action: Update Order] ID: {pk}")
        order = self.get_object(pk)
        if not order:
            logger.warning(f"[Order] سفارش {pk} یافت نشد.")
            return Response({"error": f"Order '{pk}' not found!"}, status=404)

        serializer = OrderUpdateSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"[Order] سفارش {pk} با موفقیت بروزرسانی شد.")
            return Response(serializer.data, status=200)
        else:
            logger.warning(f"[Order] داده نامعتبر برای ویرایش سفارش {pk}: {serializer.errors}")
            return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        logger.warning(f"[User: {request.user.username}] [Action: Delete Order] ID: {pk}")
        order = self.get_object(pk)
        if not order:
            logger.error(f"[Order] حذف سفارش {pk} ناموفق. سفارش یافت نشد.")
            return Response({"error": "Order not found"}, status=404)

        order.delete()
        logger.info(f"[Order] سفارش {pk} حذف شد.")
        return Response({"message": "Order deleted successfully"}, status=200)



"""
    این ویو برای تغییر وضعیت سفارش استفاده می شود
    دسترسی فقط برای ادمین مجاز است
"""
class OrderStatusUpdate(APIView):
    permission_classes = [IsAdminUser]
    
    def patch(self, request, pk):
        logger.info(f"[User: {request.user.username}] [Action: Update Status] OrderID: {pk}")
        try:
            order = Orders.objects.get(pk=pk)
        except Orders.DoesNotExist:
            logger.warning(f"[Order] سفارش {pk} یافت نشد برای بروزرسانی وضعیت.")
            return Response({"error": f"Order {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"[Order] وضعیت سفارش {pk} با موفقیت تغییر یافت.")
            return Response({"message": f"Order {pk} status updated.", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            logger.warning(f"[Order] خطا در بروزرسانی وضعیت سفارش {pk}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)