# orders/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        # Notify when a new order is created
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "orders_notifications",  # This is the channel group name
            {
                "type": "order.notification",
                "message": f"New order created with ID {instance.id}!"
            }
        )
