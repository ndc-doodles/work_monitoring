from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.email = self.scope["url_route"]["kwargs"]["email"]
        self.room_group_name = f"user_{self.email}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        target = data.get("target")
        await self.channel_layer.group_send(
            f"user_{target}",
            {"type": "chat.message", "data": data}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event["data"]))
