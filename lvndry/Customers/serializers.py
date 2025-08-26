from rest_framework import serializers
from .models import Customers , Comments








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
        fields = ['phone']

    def validate_phone (self , value):
        customer = self.instance
        if Customers.objects.exclude(pk=customer.pk).filter(phone=value).exists():
            raise serializers.ValidationError ("ERROR : this phone number already exists!")
        return value
    

class CustomerInfoSerializer (serializers.ModelSerializer):
    class Meta :
        model = Customers
        fields = ['code','phone']
        read_only_fields = ['code','phone']



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