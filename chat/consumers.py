from channels.consumer import AsyncConsumer
import json
from channels.db import database_sync_to_async
from channels.exceptions import StopConsumer
from chat.models import *



class MyChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        self.group_name = self.scope['url_route']['kwargs']['room_name']
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.send({
            "type":"websocket.accept"
        })

    async def websocket_receive(self,event):
        data = json.loads(event['text'])
        print(self.scope['user'],'user**********')
        group =  await database_sync_to_async(ChatRoom.objects.get)(name=self.group_name)
        if self.scope['user'].is_authenticated:
            chat = ChatMessage(sender_id=self.scope['user'].id,room=group,message=data['message'])
            await database_sync_to_async(chat.save)()
            data['user'] = self.scope['user'].username
            await self.channel_layer.group_send(self.group_name, {
                'type': 'chat.message',
                'message': json.dumps(data)
                }) 
        else:   
            await self.send({
                "type": "websocket.send",
                 "text": json.dumps({'msg': 'Please login to send message'})
                 })
            
    async def chat_message(self,event):
        message = event['message']
        await self.send({
            "type":"websocket.send",
            "text":event['message']
        })

    async def websocket_disconnect(self,event):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        raise StopConsumer()