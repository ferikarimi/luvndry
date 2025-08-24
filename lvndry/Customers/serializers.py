from rest_framework import serializers
from .models import Customers








class CustomerRegisterSerializer (serializers.ModelSerializer):
    class Meta :
        model = Customers
        fields = ['phone']


    def validate_phone (self , data):
        if Customers.objects.filter(phone=data["phone"]).exists() :
            raise serializers.ValidationError({"ERROR : this phone number already exists!"})
        return data
    
    def create(self, validated_data):
        customer = Customers(**validated_data)
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