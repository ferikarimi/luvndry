from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import OrderItems  # اگر سیگنال در فایل signals.py جدا باشه

@receiver(m2m_changed, sender=OrderItems.extra_services.through)
def update_prices(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        extra_total = sum(es.extra_fee for es in instance.extra_services.all())
        instance.unit_price = (instance.cloth.base_price * instance.service.price_modifier) + extra_total
        instance.total_price = instance.unit_price * instance.quantity
        instance.save(update_fields=['unit_price', 'total_price'])
