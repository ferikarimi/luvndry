from rest_framework import serializers
from .models import Orders , OrderItems
from Items.models import Clothes , Services
from Customers.models import Customers
from django.utils import timezone
from django.db.models import Sum









class OrderItemSerializer (serializers.ModelSerializer):

    service_name = serializers.PrimaryKeyRelatedField(source='service.name', read_only=True)
    cloth_name = serializers.PrimaryKeyRelatedField(source='cloth.name', read_only=True)

    class Meta :
        model = OrderItems
        fields = ["id","service","service_name", "cloth","cloth_name", "quantity", "unit_price","total_price"]
        read_only_fields = ["id","unit_price","total_price"]













class OrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.fullname', read_only=True)
    customer_phone = serializers.CharField(source='customer.phone', read_only=True)
    items = OrderItemSerializer(many=True, source='order_items', read_only=True)

    class Meta:
        model = Orders
        fields = ["id", "customer_name", "customer_phone",
                  "status", "order_time", "delivery_time",
                  "discount_amount", "total_amount", "final_amount",
                  "items"]











class OrderCreateSerializer (serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)
    items = OrderItemSerializer(many=True , write_only=True)
    fullname = serializers.CharField(write_only=True , required=False , allow_blank=True)

    class Meta :
        model = Orders
        fields = ['phone' , 'items' ,'fullname' , 'discount_amount', 'status', 'delivery_time']
    
    def validate_discount_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Discount cannot be negative.")
        return value

    def validate_final_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("The final amount cannot be negative.")
        return value

    def validate_status(self, value):
        allowed = [choice[0] for choice in Orders.STATUS_CHOICE_FIELDS]
        if value not in allowed:
            raise serializers.ValidationError(f"Status must be one of {allowed}.")
        return value

    def validate(self, attrs):
        if attrs.get('final_amount', 0) < 0:
            raise serializers.ValidationError("The final amount cannot be negative.")
        return attrs
    
    def create(self, validated_data):
        phone = validated_data.pop("phone")
        items_data = validated_data.pop("items")
        fullname = validated_data.pop("fullname" , "").strip()

        customer , created = Customers.objects.get_or_create(phone=phone)

        if created :
            last_customer = Customers.objects.order_by('-code').first()
            if last_customer and last_customer.code :
                new_code = last_customer.code + 1

            else:
                new_code = 100
            customer.code = new_code
            if fullname :
                customer.fullname = fullname
            customer.save()
        
        else :
            customer.update_name(fullname)
        
        total_amount = sum([
            i['quantity'] * (i['service'].base_price + i['cloth'].price_modifier)
            for i in items_data
        ])


        final_amount = total_amount - validated_data.get('discount_amount', 0) 
        order = Orders.objects.create(
            customer=customer ,
            total_amount=total_amount ,
            final_amount=final_amount ,
            **validated_data
            )

        for item in items_data :
            service = item['service']
            cloth = item['cloth']
            quantity =item['quantity']

            OrderItems.objects.create(
                order=order ,
                service=service ,
                cloth=cloth ,
                quantity=quantity ,
                unit_price = service.base_price + cloth.price_modifier
            )
        
        return order













class OrderUpdateSerializer (serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Orders.STATUS_CHOICE_FIELDS , required=False)
    delivery_time = serializers.DateField(required=False)

    class Meta :
        model = Orders
        fields = ['status' , 'delivery_time', 'discount_amount']














class OrderTrackingSerializer (serializers.Serializer):
    phone = serializers.CharField(write_only=True)

    customer_name = serializers.CharField(source='customer.fullname' , read_only=True)
    customer_phone = serializers.CharField(source='customer.phone' , read_only=True)

    @staticmethod
    def normalize_phone (phone):
        phone = phone.strip()
        if phone.startswith("0"):
            return "+98" + phone[1:]
        return phone
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        phone = self.normalize_phone(phone)

        try :
            customer = Customers.objects.get(phone=phone)
        except Customers.DoesNotExist :
            raise serializers.ValidationError({"ERROR : phone does not exist!"})
        
        customer_last_order = Orders.objects.filter(customer_id=customer).order_by('-order_time').first()
        if not customer_last_order :
            raise serializers.ValidationError ({"ERROR : this customer has not order!"})
        self.instance = customer_last_order
        return attrs
    
    def to_representation(self, instance):
        try :
            return {"status" : instance.status }
        except AttributeError :
            return {"status : unknown"}
        







class OrderListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.fullname", read_only=True)
    customer_phone = serializers.CharField(source="customer.phone", read_only=True)

    class Meta:
        model = Orders
        fields = ["id", "customer_name", "customer_phone", "status", "final_amount", "delivery_time"]










class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ["status"]

    def validate_status(self, value):
        allowed = [choice[0] for choice in Orders.STATUS_CHOICE_FIELDS]
        if value not in allowed:
            raise serializers.ValidationError(f"Status must be one of {allowed}.")
        return value
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status',instance.status)

        if instance.status == "Delivered" and not instance.delivery_time :
            instance.delivery_time = timezone.now()

        instance.save()
        return instance