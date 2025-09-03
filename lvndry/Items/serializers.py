from rest_framework import serializers
from .models import Services , Clothes




class AllServicesSerializer (serializers.ModelSerializer):
    class Meta :
        model = Services
        fields = '__all__'


class AllClothesSerializer (serializers.ModelSerializer):
    class Meta :
        model = Clothes
        fields = '__all__'


class ServicesAddSerializer (serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

    def validate_name(self, value):
        if Services.objects.filter(name=value).exists() :
            raise serializers.ValidationError (f"ERROR : Services {value} cannot added. this services already exist!")
        return value


class ServicesEditSerializer (serializers.ModelSerializer):
    name = serializers.CharField(required=False , allow_blank=False)
    base_price = serializers.IntegerField(required=False)

    class Meta:
        model = Services
        fields = '__all__'
    
    def validate_name(self, value):
        if not value :
            return value
        
        if self.instance is not None:
            if Services.objects.exclude(pk=self.instance.pk).filter(name=value).exists():
                raise serializers.ValidationError(
                    f"ERROR: Service '{value}' cannot be edited. This name already exists!"
                )
        else:
            if Services.objects.filter(name=value).exists():
                raise serializers.ValidationError(
                    f"ERROR: Service '{value}' cannot be created. This name already exists!"
                )
        return value


class ClothesAddSerializer (serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = '__all__'

    def validate_name(self, value):
        if Clothes.objects.filter(name=value).exists() :
            raise serializers.ValidationError (f"ERROR : Clothes '{value}' cannot added. this cloth already exist!")
        return value


class ClothesEditSerializer (serializers.ModelSerializer):
    name = serializers.CharField(required=False , allow_blank=False)
    price_modifier = serializers.IntegerField(required=False)

    class Meta:
        model = Clothes
        fields = '__all__'
    
    def validate_name(self, value):
        if not value :
            return value
        
        if self.instance is not None:
            if Clothes.objects.exclude(pk=self.instance.pk).filter(name=value).exists():
                raise serializers.ValidationError(
                    f"ERROR: Cloth '{value}' cannot be edited. This name already exists!"
                )
        else:
            if Clothes.objects.filter(name=value).exists():
                raise serializers.ValidationError(
                    f"ERROR: Cloth '{value}' cannot be created. This name already exists!"
                )
        return value