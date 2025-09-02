from rest_framework import serializers
from .models import Items




class AllItemsSerializer (serializers.ModelSerializer):
    class Meta :
        model = Items
        fields = '__all__'
    



class ItemAddSerializer (serializers.ModelSerializer):
    description = serializers.CharField(required=False , allow_blank=True)
    class Meta:
        model = Items
        fields = '__all__'

    def validate_name(self, value):
        if Items.objects.filter(name=value).exists() :
            raise serializers.ValidationError ("ERROR : item cannot added. this product already exist!")
        return value


class ItemEditSerializer (serializers.ModelSerializer):
    name = serializers.CharField(required=False , allow_blank=False)
    description = serializers.CharField(required=False, allow_blank=True)
    unit_price = serializers.DecimalField(required=False , max_digits=10 , decimal_places=0)
    class Meta:
        model = Items
        fields = '__all__'
    
    def validate_name(self, value):
        if not value :
            return value
        
        if self.instance is None and Items.objects.filter(name=value).exists():
            raise serializers.ValidationError("ERROR : item can not edited. this name already exists!") 

        if self.instance is not None and Items.objects.exclude(pk=self.instance.pk).filter(name=value).exists():
            raise serializers.ValidationError ("ERROR : item can not edited. this name already exist!")

        return value