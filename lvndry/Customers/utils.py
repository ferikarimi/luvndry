LEVEL_MAP = {
    "bronze": "برنزی",
    "silver": "نقره‌ای",
    "gold": "طلایی",
}

def filter_customer_level(queryset, level):
    if level in LEVEL_MAP:
        return queryset.filter(level__name=LEVEL_MAP[level])
    return queryset