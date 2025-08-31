from rest_framework import serializers
from .models import Customers , Comments
import jdatetime





class CustomerRegisterSerializer (serializers.ModelSerializer):
    class Meta :
        model = Customers
        fields = ['phone' , 'code']
        read_only_fields = ['code']


    def validate_phone (self , data):
        if Customers.objects.filter(phone=data["phone"]).exists() :
            raise serializers.ValidationError({"ERROR : this phone number already exists!"})
        return data
    
    def create(self, validated_data):
        last_customer = Customers.objects.order_by('-code').first()
        if last_customer and last_customer.code :
            new_code = last_customer.code + 1
        else:
            new_code = 100
        customer = Customers(**validated_data)
        customer.code = new_code
        customer.save
        return customer
    


class CustomerUpdateProfileSerializer (serializers.ModelSerializer):
    class Meta :
        model = Customers
        fields = ['phone' , 'fullname' , 'address']

    def validate_phone (self , value):
        customer = self.instance
        if Customers.objects.exclude(pk=customer.pk).filter(phone=value).exists():
            raise serializers.ValidationError ("ERROR : this phone number already exists!")
        return value
    
    def validate_fullname (self , value):
        if not value.strip():
            raise serializers.ValidationError ("ERROR : fullname cannot be empty!")
        return value
    
    def validate_address (self , value):
        if not value.strip():
            raise serializers.ValidationError ("ERROR : address cannot be empty!")
        return value
            
    

class CustomerInfoSerializer (serializers.ModelSerializer):
    class Meta :
        model = Customers
        fields = ['code','phone' , 'fullname' , 'address']
        read_only_fields = ['code','phone' , 'fullname' , 'address']



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
    

class CommentAdminSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField(read_only=True)

    class Meta :
        model = Comments
        fields = '__all__'


class CommentRecentlySerializer (serializers.ModelSerializer):
    created_at_jalili = serializers.SerializerMethodField()
    class Meta :
        model = Comments
        fields = ['customer','text','created_at','created_at_jalili']
        read_only_fields = ['created_at','created_at_jalili']


    def get_created_at_jalili (self , obj):
        if obj.created_at :
            jalili_data = jdatetime.datetime.fromgregorian(datetime=obj.created_at)
            return jalili_data.strftime('%Y/%m/%d - %H:%M')
        return None