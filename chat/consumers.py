import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, Message
from students.models import Student

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group = f"chat_{self.room_id}"

        # Join room
        await self.channel_layer.group_add(
            self.room_group,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender']

        # Save message in DB
        await self.save_message(sender_id, message)

        # Broadcast message
        await self.channel_layer.group_send(
            self.room_group,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender_id,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"]
        }))

    @database_sync_to_async
    def save_message(self, sender_id, message):
        sender = Student.objects.get(uid=sender_id)
        room = ChatRoom.objects.get(uid=self.room_id)
        return Message.objects.create(room=room, sender=sender, text=message)
