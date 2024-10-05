# orders/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class OrderNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the notifications group
        await self.channel_layer.group_add("orders_notifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the notifications group
        await self.channel_layer.group_discard("orders_notifications", self.channel_name)

    # Receive message from group
    async def order_notification(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
