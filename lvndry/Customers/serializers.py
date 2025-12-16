from rest_framework import serializers
import jdatetime
from .models import (
    Customers , Comments
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
    این سریالایزر برای ثبت نام یک مشتری جدید در سایت استفاده می شود
    مشتری ها یک کد یکتا دارند که از 1000 شروع میشود
"""
class CustomerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ['phone', 'fullname', 'address', 'code']
        read_only_fields = ['code']

    def create(self, validated_data):
        last_customer = Customers.objects.order_by('-code').first()
        new_code = last_customer.code + 1 if last_customer and last_customer.code else 100
        customer = Customers.objects.create(code=new_code, **validated_data)
        return customer


"""
    این سریالایزر برای اپدیت کردن اطلاعات یک مشتری استفاده میشود
    هنگام اپدیت کردن ، شماره تلفن مشتری چک میشود تا همواره شماره تلفن منحصر به فرد باشد
"""
class CustomerUpdateProfileSerializer (serializers.ModelSerializer):
    class Meta :
        model = Customers
        fields = ['code','phone' , 'fullname' , 'address']
        read_only_fields = ['code']
        
    def validate_phone(self, value):
        customer = getattr(self, 'instance', None)
        if customer is not None:
            if Customers.objects.exclude(pk=customer.pk).filter(phone=value).exists():
                raise serializers.ValidationError("ERROR : this phone number already exists!")
        return value

            
"""
    این سریالایزر برای پیدا کردن یک مشتری خاص استفاده میشود
    این سریالایزر امکان ویرایش اطلاعات مشتری را نمیدهد
"""    
class CustomerInfoSerializer (serializers.ModelSerializer):

    class Meta :
        model = Customers
        fields = ['code','phone' , 'fullname' , 'address']
        read_only_fields = ['code','phone' , 'fullname' , 'address']


"""
    این سریالایزر برای ساخت کامنت توسط مشتری استفاده میشود
    اگر مشتری از خدمات ما استفاده نکرده باشد ، نمیتواند نظری ثبت کند
    نظر ها بعد از تایید توسط ادمین سایت ، نمایش داده می شوند
"""
class CommentCreateSerializer (serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)

    class Meta:
        model = Comments
        fields = ['phone','text']

    def create(self, validated_data):
        phone = validated_data.pop("phone")
        try:
            customer = Customers.objects.get(phone=phone)
        except Customers.DoesNotExist :
            raise serializers.ValidationError({"ERROR : You must have used our services to be able to comment."})
        comment = Comments.objects.create(customer=customer , **validated_data)
        return comment


"""
    این سریالایزر برای نمایش کامنت ها برای ادمین سایت استفاده می شود
"""
class CommentAdminSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)
    customer_phone = serializers.SerializerMethodField()

    class Meta :
        model = Comments
        fields = '__all__'

    def get_customer_phone(self, obj):
        phone_str = str(obj.customer.phone)
        return phone_str


"""
    این سریالایزر برای نمایش محدودی از کامنت ها در صفحه عمومی سایت استفاده می شود
    شماره ها به صورت ناشناس نمایش داده می شود
    تاریخ انتشار کامنت ها به صورت شمسی نمایش داده می شود
"""
class CommentRecentlySerializer (DateJaliliMixin , serializers.ModelSerializer):
    created_at_jalili = serializers.SerializerMethodField()
    hidden_phone = serializers.SerializerMethodField()
    class Meta :
        model = Comments
        fields = ['customer','text','created_at','created_at_jalili','hidden_phone']
        read_only_fields = ['created_at','created_at_jalili','hidden_phone']

    def get_hidden_phone (self , obj):   
        phone = str(obj.customer.phone)
        new_phone = phone[:4] + '*' * (len(phone) - 7) + phone[-3:]
        return new_phone

    def get_created_at_jalili(self, obj):
        return self.to_jalili(obj.created_at)



"""
    این سریالایزر برای نمایش تمام مشتری های سایت استفاده می شود
    شماره های مشتری ها بدون کد کشور نمایش داده می شود
"""
class AllCustomersSerializer (serializers.ModelSerializer):
    phone = serializers.SerializerMethodField()

    class Meta :
        model = Customers
        fields = ['id','code','phone','fullname','address']

    def get_phone(self, obj):
        phone = str(obj.phone)
        return phone