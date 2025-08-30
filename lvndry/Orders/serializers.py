from rest_framework import serializers
from .models import Orders , OrderItems
from Items.models import Items
from Customers.models import Customers









#     # def validate_quantity (self , value):
#     #     if value < 1 :
#     #         raise serializers.ValidationError("The number of items must be less than 1.")
#     #     return value
    
#     # def validate_unit_price (self , value):
#     #     if value < 0 :
#     #         raise serializers.ValidationError ("Unit price cannot be negative.")
#     #     return value
    
#     # def validate_item_id (self , value):
#     #     if not Items.objects.filter(id=value.id).exists():
#     #         raise serializers.ValidationError ("The selected item does not exist.")
#     #     return value


# class OrderSerializer (serializers.ModelSerializer):
    
#     order_items = OrderItemSerializer(many=True)
#     class Meta :
#         model = Orders
#         fields = '__all__'

#     def create(self, validated_data):
#         order_items_data = validated_data.pop('order_items')
#         order = Orders.objects.create(**validated_data)
#         total_amount = 0

#         for item_data in order_items_data :
#             items = item_data.pop('items')
#             quantity = item_data.get('quantity',1)
#             unit_price = sum([i.unit_price for i in items])
#             order_item = OrderItems.objects.create(order_id=order ,unit_price=unit_price , quantity=quantity)

#             order_item.items.set(items)
#             total_amount += unit_price * quantity
#         order.total_amount = total_amount
#         order.final_amount = total_amount - order.discount_amount
#         order.save()
#         return order








# class OrderEditSerializer (serializers.ModelSerializer):
#     class Meta :
#         model = Orders
#         fields = '__all__'




class OrderItemSerializer (serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Items.objects.all())
    class Meta :
        model = OrderItems
        fields = ["item", "cloth_name", "quantity", "unit_price"]



class OrderCreateSerializer (serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)
    items = OrderItemSerializer(many=True , write_only=True)
    class Meta :
        model = Orders
        fields = '__all__'
    
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
        customer , created = Customers.objects.get_or_create(phone=phone)
        if created :
            last_customer = Customers.objects.order_by('-code').first()
            if last_customer and last_customer.code :
                new_code = last_customer.code + 1

            else:
                new_code = 100
            customer.code = new_code
            customer.save()
        
        order = Orders.objects.create(customer_id = customer , **validated_data)

        for item in items_data :
            OrderItems.objects.create(order_id = order , **item)
        
        return order
    
class OrderUpdateSerializer (serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Orders.STATUS_CHOICE_FIELDS , required=False)
    delivery_time = serializers.DateTimeField(required=False)

    class Meta :
        model = Orders
        fields = ['status', 'delivey_time', 'discount_amount']