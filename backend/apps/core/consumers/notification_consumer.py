import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.token = self.scope["query_string"].decode().split("token=")[-1] if "token=" in self.scope["query_string"].decode() else None

        if not self.token:
            await self.close(code=4001)
            return

        try:
            access_token = AccessToken(self.token)
            self.user = await database_sync_to_async(User.objects.get)(id=access_token["user_id"])
        except Exception:
            await self.close(code=4001)
            return

        self.user_group = f"user_{self.user.id}"
        self.tenant_group = f"tenant_{self.user.tenant_id}" if self.user.tenant_id else None

        await self.channel_layer.group_add(self.user_group, self.channel_name)
        if self.tenant_group:
            await self.channel_layer.group_add(self.tenant_group, self.channel_name)

        await self.accept()

        await self.send(text_data=json.dumps({
            "type": "connection_established",
            "message": "Connected to notification service",
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user_group, self.channel_name)
        if self.tenant_group:
            await self.channel_layer.group_discard(self.tenant_group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get("type") == "ping":
            await self.send(text_data=json.dumps({"type": "pong"}))

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "notification": event["notification"],
        }))

    async def security_alert(self, event):
        await self.send(text_data=json.dumps({
            "type": "security_alert",
            "alert": event["alert"],
        }))
