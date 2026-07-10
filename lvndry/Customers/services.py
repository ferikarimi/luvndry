from Orders.models import Orders
from .models import CustomerLevel

def update_customer_level(customer):

    order_count = customer.orders.filter(
        status="Delivered"
    ).count()

    if order_count > 20:
        level_name = "طلایی"

    elif order_count > 15:
        level_name = "نقره‌ای"

    elif order_count > 10:
        level_name = "برنزی"

    else:
        customer.level = None
        customer.save(update_fields=["level"])
        return

    try:
        level = CustomerLevel.objects.get(name=level_name)
    except CustomerLevel.DoesNotExist:
        return

    if customer.level_id != level.id:
        customer.level = level
        customer.save(update_fields=["level"])