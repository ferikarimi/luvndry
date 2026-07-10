from django.db.models import Count


BRONZE_MIN = 10
SILVER_MIN = 20
GOLD_MIN = 30

def get_customer_level (order_count):
    
    if order_count >= GOLD_MIN :
        return "gold"
        
    elif order_count >= SILVER_MIN :
        return "silver"
        
    elif order_count >= BRONZE_MIN :
        return "bronze"
        
    return "normal"
    
    
    
LEVEL_MAP = {
    "bronze": "برنزی",
    "silver": "نقره‌ای",
    "gold": "طلایی",
}

def filter_customer_level(queryset, level):
    if level in LEVEL_MAP:
        return queryset.filter(level__name=LEVEL_MAP[level])
    return queryset