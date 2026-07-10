from rest_framework import serializers
from Customers.models import Customers
from django.utils import timezone
import jdatetime
from .models import (
    Orders , OrderItems
)
from Items.models import (
    Clothes , Services , ExtraServices
)



"""
    از این میکسین برای تبدیل تاریخ میلادی به شمسی استفاده می شود
    ایام هفته به صورت فارسی نمایش داده می شود
"""
class DateJaliliMixin:
    WEEKDAY_FA = {
        "Saturday": "شنبه",
        "Sunday": "یک‌شنبه",
        "Monday": "دوشنبه",
        "Tuesday": "سه‌شنبه",
        "Wednesday": "چهارشنبه",
        "Thursday": "پنج‌شنبه",
        "Friday": "جمعه",
    }

    def to_jalili(self, date_obj, format="%Y/%m/%d (%A)"):
        if not date_obj:
            return None
        
        jdate = jdatetime.datetime.fromgregorian(datetime=date_obj)
        result = jdate.strftime(format)
        
        for en, fa in self.WEEKDAY_FA.items():
            result = result.replace(en, fa)
        
        return result



"""
    از این میکسین برای تخفیف خودکار برای افرادی که بیشتر از 10 بار مراجعه کرده اند استفاده می شود
    ده الی بیست سفارش شامل 5 درصد تخفیف می شود
    بیست الی سی سفارش شامل 10 درصد تخفیف می شود
    سی سفارش به بالا شامل 15 درصد تخفیف می شود
"""
class LoyaltyDiscountMixin:

    @staticmethod
    def get_loyalty_discount(customer):
        orders_count = customer.orders.count()

        if orders_count <= 10:
            loyalty_discount = 0
        elif orders_count <= 20:
            loyalty_discount = 3
        elif orders_count <= 30:
            loyalty_discount = 5
        else:
            loyalty_discount = 10

        return loyalty_discount



"""
    این سریالایزر جزئیات 'خدمت اضافی' را نمایش می دهد
"""
class ExtraServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraServices
        fields = ['id', 'name', 'extra_fee']



"""
    این سریالایزر جزئیات هر آیتم سفارش که شامل 'خدمت و نام خدمت' , 'لباس و نام لباس' و  'خدمت اضافی و نام خدمت اضافی' را نمایش می دهد
"""
class OrderItemSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name', read_only=True)
    cloth_name = serializers.CharField(source='cloth.name', read_only=True)
    extra_services = ExtraServicesSerializer(many=True, read_only=True)
    extra_services_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source='extra_services', 
        queryset=ExtraServices.objects.all()
    )

    class Meta:
        model = OrderItems
        fields = [
            "id", "service", "service_name", "cloth", "cloth_name",
            "extra_services", "extra_services_ids",
            "quantity", "unit_price", "total_price" , "is_express"
        ]
        read_only_fields = ["id", "unit_price", "total_price"]

    def get_extra_services_names(self, obj):
        return [e.name for e in obj.extra_services.all()]



"""
    این سریالایزر تمام جزئیات یک سفارش را نمایش می دهد
    از جمله اطلاعات مشتری ، آیتم های سفارش ، مبالغ و وضعیت سفارش
    تاریخ ثبت سفارش را به صورت شمسی نمایش می دهد
"""
class OrderDetailSerializer(DateJaliliMixin , serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    customer_code = serializers.CharField(source='customer.code', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)
    items = OrderItemSerializer(source='order_items', many=True, read_only=True)
    order_date = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ['id','customer_name','customer_code','customer_phone','discount_amount','total_amount','final_amount','status','order_time','delivery_time','order_date','items',
        ]

    def get_order_date(self, obj):
        return self.to_jalili(obj.order_time)



"""
    این سریالایزر برای ایجاد سفارش‌های جدید در سیستم استفاده می‌شود
    وظایف اصلی آن عبارتند از:

    1. دریافت اطلاعات ورودی:
        - phone: شماره مشتری (برای شناسایی یا ایجاد مشتری جدید)
        - fullname و address: نام و آدرس مشتری (اختیاری)
        - items: لیست آیتم‌های سفارش شامل سرویس، لباس، تعداد، خدمات اضافی و سرعت انجام سفارش
        - discount_amount: تخفیف اعمال شده توسط مدیر
        - status: وضعیت سفارش
        - delivery_time: زمان تحویل سفارش

    2. اعتبارسنجی داده‌ها:
        - تخفیف نمی‌تواند منفی باشد
        - وضعیت سفارش باید یکی از وضعیت‌های تعریف شده در Orders.STATUS_CHOICE_FIELDS باشد

    3. مدیریت مشتری:
        - بررسی وجود مشتری با شماره تلفن داده شده
        - اگر مشتری جدید باشد، ایجاد مشتری با کد یکتا و ذخیره نام و آدرس در صورت وجود
        - اگر مشتری موجود باشد، به‌روزرسانی نام و آدرس در صورت داده شدن

    4. محاسبه تخفیف وفاداری:
        - بر اساس تعداد سفارش‌های قبلی مشتری، درصدی تخفیف وفاداری اختصاص داده می‌شود:
            * 0 سفارش تا 10: 0%
            * 11 تا 20 سفارش: 5%
            * 21 تا 30 سفارش: 10%
            * بالای 30 سفارش: 15%

    5. ایجاد سفارش و آیتم‌ها:
        - محاسبه قیمت هر آیتم با توجه به سرویس، لباس، خدمات اضافی و انتخاب express
        - جمع کل قیمت سفارش محاسبه می‌شود
        - اعمال تخفیف مدیر و تخفیف وفاداری برای محاسبه مبلغ نهایی

    6. خروجی:
        - سفارش ساخته شده با مقادیر total_amount و final_amount بروزرسانی و بازگردانده می‌شود
"""
class OrderCreateSerializer(LoyaltyDiscountMixin , serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)
    items = OrderItemSerializer(many=True, write_only=True)
    fullname = serializers.CharField(write_only=True, required=False, allow_blank=True)
    address = serializers.CharField(write_only=True, required=False, allow_blank=True)

    fullname_display = serializers.CharField(source='customer.fullname', read_only=True)

    class Meta:
        model = Orders
        fields = ['id','phone','items','fullname','address','fullname_display','discount_amount','status','delivery_time']

    def validate_discount_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Discount cannot be negative.")
        return value

    def validate_status(self, value):
        allowed = [choice[0] for choice in Orders.STATUS_CHOICE_FIELDS]
        if value not in allowed:
            raise serializers.ValidationError(f"Status must be one of {allowed}.")
        return value

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        phone = validated_data.pop("phone")
        fullname = validated_data.pop("fullname", "").strip()
        address = validated_data.pop("address", "").strip()
        items_data = validated_data.pop("items", [])


        customer, created = Customers.objects.get_or_create(phone=phone)

        if created:
            last_customer = Customers.objects.order_by('-code').first()
            if last_customer and last_customer.code:
                new_code = last_customer.code + 1
            else:
                new_code = 100

            customer.code = new_code
            if fullname:
                customer.fullname = fullname
            if address:
                customer.address = address

            customer.save()

        else:
            if fullname:
                customer.fullname = fullname

            if address:
                customer.address = address

            customer.save()

        loyalty_discount = self.get_loyalty_discount(customer)

        order = Orders.objects.create(
            customer=customer,
            discount_amount=validated_data.get('discount_amount', 0),
            total_amount=0,
            final_amount=0,
            status=validated_data.get('status', 'In progress'),
            delivery_time=validated_data.get('delivery_time')
        )

        total_amount = 0

        for item in items_data:
            service = item.get('service')
            cloth = item.get('cloth')
            quantity = item.get('quantity', 1)
            is_express = item.get('is_express', False)
            extra_services = item.get('extra_services', [])
            extras_list = []

            if isinstance(service, int):
                service_obj = Services.objects.get(pk=service)
            else:
                service_obj = service

            if isinstance(cloth, int):
                cloth_obj = Clothes.objects.get(pk=cloth)
            else:
                cloth_obj = cloth

            if extra_services and not hasattr(extra_services[0], '__dict__'):
                extras_list = list(ExtraServices.objects.filter(id__in=extra_services))
            else:
                extras_list = list(extra_services)

            extra_total = sum(es.extra_fee for es in extras_list)

            unit_price = (cloth_obj.base_price * service_obj.price_modifier) + extra_total

            if is_express:
                express_fee = int(unit_price * 0.30)
                unit_price += express_fee

            total_price = unit_price * quantity
            total_amount += total_price

            order_item = OrderItems.objects.create(
                order=order,
                service=service_obj,
                cloth=cloth_obj,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                is_express=is_express
            )

            if extras_list:
                order_item.extra_services.set(extras_list)


        manager_discount_factor = 1 - (order.discount_amount / 100)

        loyalty_discount_factor = 1 - (loyalty_discount / 100)

        final_amount = total_amount * manager_discount_factor * loyalty_discount_factor

        order.total_amount = total_amount
        order.final_amount = int(final_amount)
        order.save()

        return order



"""
    این سریالایزر برای بررسی و نمایش سریع اطلاعات مشتری ثبت نام شده، استفاده می شود
"""
class CheckCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customers
        fields = ['fullname', 'address', 'phone', 'code']



"""
    از این سریالایزر برای بررسی وضعیت اخرین سفارش مشتری استفاده می شود
    فقط تو صفحه ی عمومی سایت استفاده می شود
"""
class OrderTrackingSerializer(serializers.Serializer):
    phone = serializers.CharField(write_only=True)
    last_order_status = serializers.CharField(read_only=True)

    def validate(self, attrs):
        phone = attrs.get('phone')

        try:
            customer = Customers.objects.get(phone=phone)
        except Customers.DoesNotExist:
            raise serializers.ValidationError({"ERROR": "شماره تلفن وارد شده وجود ندارد."})

        last_order = Orders.objects.filter(customer=customer).order_by('-order_time').first()
        if not last_order:
            raise serializers.ValidationError({"ERROR": "شما هنوز سفارشی ثبت نکرده‌اید."})

        self.instance = last_order
        return attrs

    def to_representation(self, instance):
        status_dict = dict(Orders.STATUS_CHOICE_FIELDS)

        return {
            "last_order_status": status_dict.get(instance.status, "نامشخص"),
        }



"""
    این سریالایزر برای نمایش اطلاعات مشتری استفاده می شود
    تعداد "کل سفارشات" و "سفارش های انجام شده" مشتری نیز محاسبه می شود
"""
class CustomerSerializer(serializers.ModelSerializer):
    order_count = serializers.SerializerMethodField()
    delivered_order_count = serializers.SerializerMethodField()

    class Meta:
        model = Customers
        fields = ['id', 'code','fullname', 'phone', 'address' ,'order_count','delivered_order_count']
    
    def get_order_count (self , obj):
        return obj.orders.count()
    
    def get_delivered_order_count(self , obj):
        return obj.orders.filter(status="Delivered").count()


"""
    این سریالایزر برای نمایش تمام اطلاعات سفارش استفاده می شود
    تاریخ ثبت سفارش و دریافت سفارش به صورت شمسی نمایش داده می شود
"""
class OrderSerializer(DateJaliliMixin , serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    is_delivered = serializers.SerializerMethodField()
    order_time_jalali = serializers.SerializerMethodField()
    delivery_time_jalali = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Orders
        fields = ['id', 'customer_id','discount_amount', 'total_amount', 'final_amount', 'status', 'order_time', 'delivery_time', 'order_items' ,'is_delivered', 'order_time_jalali', 'delivery_time_jalali' ,'status_display']

    def get_is_delivered (self , obj):
        return obj.status == 'In progress'

    def get_order_time_jalali(self, obj):
        return self.to_jalili(obj.order_time)

    def get_delivery_time_jalali(self, obj):
        return self.to_jalili(obj.delivery_time)



"""
    این سریالایزر برای تغییر وضعیت سفارش استفاده می شود
    وضعیت سفارش 'تحویل داده شده' را نمیتوان تغییر داد
    زمان تحویل به صورت شمسی نمایش داده می شود
    هنگام تغییر وضعیت سفارش به 'تحویل داده شده' ، زمان به صورت خودکار ثبت می شود
"""
class OrderStatusUpdateSerializer(DateJaliliMixin , serializers.ModelSerializer):
    delivery_time_jalili = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Orders
        fields = ["status" , "delivery_time_jalili"]

    def validate_status(self, value):
        allowed = [choice[0] for choice in Orders.STATUS_CHOICE_FIELDS]
        if value not in allowed:
            raise serializers.ValidationError(f"Status must be one of {allowed}.")
        
        if self.instance.status == 'Delivered':
            raise serializers.ValidationError("نمیتوان وضعیت سفارش تحویل داده شده (بازگشت پاکیزگی به آغوش صاحبش) را تغییر داد")
        return value
    
    def update(self, instance, validated_data):
        new_status = validated_data.get('status', instance.status)

        if new_status == 'Delivered' and not instance.delivery_time :
            instance.delivery_time = timezone.now()
        
        instance.status = new_status
        instance.save()
        return instance
    
    def get_delivery_time_jalili(self , obj):
        return self.to_jalili(obj.delivery_time)



"""
    این سریالایزر اطلاعات مشتری از جمله : نام ، کد و تلفن را نمایش می دهد
    نام خدمت و لباس ، تعداد ، قیمت واحد ، قیمت کل و عجله ای بودن سفارش را نمایش می دهد
"""
class AllActiveOrdersListSerializer(serializers.ModelSerializer , DateJaliliMixin):
    order_id = serializers.IntegerField(source='order.id', read_only=True)
    customer_code = serializers.CharField(source='order.customer.code', read_only=True)
    customer_name = serializers.CharField(source='order.customer.fullname', read_only=True)
    customer_phone = serializers.CharField(source='order.customer.phone' ,read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    cloth_name = serializers.CharField(source='cloth.name', read_only=True)
    is_express = serializers.BooleanField(read_only=True)
    status = serializers.CharField(source='order.status', read_only=True)
    status_display = serializers.CharField(source='order.get_status_display', read_only=True)
    final_amount = serializers.SerializerMethodField()
    order_date = serializers.SerializerMethodField()

    class Meta:
        model = OrderItems
        fields = ["id", "order_id", "customer_code","customer_name", "customer_phone","service_name", "cloth_name","quantity", "unit_price", "final_amount" ,"total_price","is_express" , "status" , "status_display" , "order_date"]
    
    def get_final_amount(self , obj):
        return obj.order.final_amount
    
    def get_order_date(self, obj):
        return self.to_jalili(obj.order.order_time)



"""
    این سریالایزر برای مدیریت و به روزرسانی ایتم های یک سفارش استفاده می شود
    قیمت کل آیتم بر اساس تعداد و قیمت واحد محاسبه می شود
    امکان ویرایش خدمت ، لباس ، تعداد و خدمت اضافی وجود دارد
"""
class OrderItemUpdateSerializer(serializers.ModelSerializer):
    extra_services_detail = ExtraServicesSerializer(source='extra_services', many=True, read_only=True)
    extra_services = serializers.PrimaryKeyRelatedField(
        queryset=ExtraServices.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = OrderItems
        fields = ['id', 'service', 'cloth', 'extra_services', 'extra_services_detail', 'quantity', 'unit_price', 'total_price']
        extra_kwargs = {
            'id': {'required': False},
            'total_price': {'read_only': True}
        }

    def validate(self, data):
        quantity = data.get('quantity', getattr(self.instance, 'quantity', 1))
        unit_price = data.get('unit_price', getattr(self.instance, 'unit_price', 0))
        data['total_price'] = quantity * unit_price
        return data



"""
    از این سریالایزر برای ویرایش کل سفارش استفاده می شود
    از جمله اپدیت وضعیت ، تخفیف ، آیتم ها و محاسبه مبلغ نهایی
    همنچنین اطلاعات مشتری هم به صورت read_only نمایش داده می شود
"""
class OrderUpdateSerializer(DateJaliliMixin , LoyaltyDiscountMixin , serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Orders.STATUS_CHOICE_FIELDS, required=False)
    order_items = OrderItemUpdateSerializer(many=True, required=False)
    customer_code = serializers.IntegerField(source="customer.code", read_only=True)
    customer_name = serializers.CharField(source="customer.fullname", read_only=True)
    customer_phone = serializers.SerializerMethodField()
    order_date_shamsi = serializers.SerializerMethodField()
    
    class Meta:
        model = Orders
        fields = [
            'id', 'customer_code', 'customer_name', 'customer_phone',
            'status', 'discount_amount', 'total_amount', 'final_amount',
            'order_items', 'order_date_shamsi',
        ]
        read_only_fields = ['final_amount']

    def get_customer_phone(self, obj):
        return obj.customer.phone if obj.customer else None

    def get_order_date_shamsi(self, obj):
        return self.to_jalili(obj.order_time)
    
    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if order_items_data is not None:
            instance.order_items.all().delete()

            total_amount = 0
            customer = instance.customer
            
            loyalty_discount = self.get_loyalty_discount(customer)

            for item_data in order_items_data:
                extra_services = item_data.pop('extra_services', [])

                service = item_data['service']
                if isinstance(service, int):
                    service = Services.objects.get(id=service)

                cloth = item_data['cloth']
                if isinstance(cloth, int):
                    cloth = Clothes.objects.get(id=cloth)

                quantity = item_data.get('quantity', 1)
                is_express = item_data.get('is_express', False)

                extra_objs = []
                if extra_services:
                    extra_ids = [es.id if isinstance(es, ExtraServices) else es for es in extra_services]
                    extra_objs = ExtraServices.objects.filter(id__in=extra_ids)

                extra_total = sum(es.extra_fee for es in extra_objs) if extra_objs else 0

                unit_price = (cloth.base_price * service.price_modifier) + extra_total
                if is_express:
                    unit_price += int(unit_price * 0.30)
                total_price = unit_price * quantity
                total_amount += total_price

                order_item = OrderItems.objects.create(
                    order=instance,
                    service=service,
                    cloth=cloth,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price,
                    is_express=is_express
                )

                if extra_objs:
                    order_item.extra_services.set(extra_objs)

            manager_discount_factor = 1 - (instance.discount_amount / 100)
            loyalty_discount_factor = 1 - (loyalty_discount / 100)
            final_amount = total_amount * manager_discount_factor * loyalty_discount_factor

            instance.total_amount = total_amount
            instance.final_amount = int(final_amount)
            instance.save()

        return instance