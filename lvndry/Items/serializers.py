from rest_framework import serializers
from .models import Items



class ItemAddSerializer (serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'

    def validate_name(self, value):
        if Items.objects.get(namr=value):
            raise serializers.ValidationError ("ERROR : item can not added. this product already exist!")
        return value


class ItemEditSerializer (serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'
    
    def validate_name(self, value):
        if self.instance is None and Items.objects.filter(name=value).exists():
            raise serializers.ValidationError("ERROR : item can not edited. this name already exists!") 

        if self.instance is not None and Items.objects.exclude(pk=self.instance.pk).filter(name=value).exists():
            raise serializers.ValidationError ("ERROR : item can not edited. this name already exist!")

        return value