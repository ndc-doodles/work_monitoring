import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = str(self.scope["user"].id)
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data.get("event")
        if event in ["offer", "answer", "candidate"]:
            # Broadcast signaling to other users
            await self.channel_layer.group_send(
                "chat",
                {
                    "type": "signal_message",
                    "message": data
                }
            )

    async def signal_message(self, event):
        message = event["message"]
        # Don't send to sender
        if str(self.scope["user"].id) != message.get("sender"):
            await self.send(text_data=json.dumps(message))
    