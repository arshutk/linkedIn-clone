from channels.generic.websocket import WebsocketConsumer

from channels.db import database_sync_to_async

import json

from channels.consumer import AsyncConsumer

from chat.models import Thread, Chat

from chat.serializers import ThreadSerializer, ChatSerializer

from network.models import Connection


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.sender = self.scope['url_route']['kwargs']['sender_id']
        self.receiver = self.scope['url_route']['kwargs']['receiver_id']
        
        # Write check for connection
        
        self.thread_id = await self.get_thread(self.sender, self.receiver)
        self.chat_room = f'thread_{self.thread_id}'
        
        chat = await self.get_chat(self.thread_id)
        
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )
        
        await self.send({
            'type': 'websocket.accept',
            })
        
        await self.send({
            'type': 'websocket.send',
            'text': chat
            })    
        
        
    async def websocket_receive(self, event):
        try:
            data = json.loads(event.get('text'))['text']
            
            if data:
                recent_message = await self.create_chat(self.sender, self.thread_id, data)
                await self.channel_layer.group_send(
                    self.chat_room,
                    {
                        'type': 'send_recent_message',
                        'text': recent_message
                    }
                )
            
            else:
                await self.send({
                'type': 'websocket.send',
                'text': 'No text containing message found.'
                })
            
        except:
            await self.send({
            'type': 'websocket.send',
            'text': 'Error, kindly send data in right format.'
            })

        
     
    
    async def websocket_disconnect(self, event):
        print('Disconnected :-<', event)  
    
    
    @database_sync_to_async
    def get_chat(self, thread_id):
        chat = Thread.objects.get(id = thread_id).messages
        serializer = ChatSerializer(chat, many = True, context = {'sender' : self.sender})
        return json.dumps({"messages" : serializer.data})
    
    @database_sync_to_async
    def create_chat(self, sender_id, thread_id, text):
        serializer = ChatSerializer(data = {'sender' : sender_id, 'thread' : thread_id, 'text' : text}, context = {'sender' : self.sender})
        if serializer.is_valid():
            serializer.save()
            # return json.dumps({"messsage" : serializer.data})
            return json.dumps(serializer.data)
            # return text
        return serializer.errors
    
    @database_sync_to_async
    def get_thread(self, sender_id, receiver_id):
        thread = Thread.objects.filter(first_member_id = sender_id, second_member_id = receiver_id) | \
                 Thread.objects.filter(first_member_id = receiver_id, second_member_id = sender_id)
        if thread.exists():
            return thread[0].id
        serializer = ThreadSerializer(data = {'first_member' : sender_id, 'second_member' : receiver_id})
        if serializer.is_valid():
            serializer.save()
            return serializer.data.id
        return serializer.errors
        
    async def send_recent_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
            })
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# # await self.send({
#             # 'type': 'websocket.send',
#             # 'text': json.loads(chat)
#             # 'text': json.dumps({1:1,2:2})
#             # })  
    
# # async def websocket_connect(self, event):
# #         print('Yup, all seems to be good !!', event)
        
# #         await self.send({
# #             'type': 'websocket.accept'
# #             })
        
# #         await asyncio.sleep(10)
        
#         # await self.send({
#         #     'type': 'websocket.close' 
#         #     })


# # class ChatConsumer(AsyncConsumer):
    
# #     async def websocket_connect(self, event):
# #         print('Yup, all seems to be good !!', event)
        
# #         await self.send({
# #             'type': 'websocket.accept'
# #             })
        
# #         sender = self.scope['url_route']['kwargs']['sender_id']
# #         receiver = self.scope['url_route']['kwargs']['receiver_id']
        
# #         chat = await self.get_chat(sender, receiver)
# #         # print(chat)
        
# #         await self.send({
# #             'type': 'websocket.send',
# #             'text': f'Hello {receiver} from {sender}' 
# #             })
         
#     # async def websocket_receive(self, event):
#     #     print('Here take your message', event)
#     #     # Here take your message {'type': 'websocket.receive', 'text': '{"text":"Muthafakka", "emoji":":--<"}'}
#     #     data = event.get('text')
#     #     if data:
#     #         data = json.loads(data)
        
#     #     sender = self.scope['url_route']['kwargs']['sender_id']
#     #     receiver = self.scope['url_route']['kwargs']['receiver_id']
        
#     #     await self.send({
#     #         'type': 'websocket.send',
#     #         'text': data['text']
#     #         })
        
    
#     # async def websocket_disconnect(self, event):
#     #     print('Disconnected :-<', event)
    
    
    
    
    
#     # @database_sync_to_async
#     # def get_chat(self, sender_id, receiver_id):
#     #     chat1 = Chat.objects.filter(receiver = receiver_id, sender = sender_id )
#     #     chat2 = Chat.objects.filter(receiver = sender_id, sender = receiver_id )
#     #     serializer = ChatSerializer(chat1 | chat2, many = True)
#     #     return serializer.data
    
    
#     # {'type': 'websocket', 'path': '/ws/chat/2/1/', 'raw_path': b'/ws/chat/2/1/', 
#     #  'headers': [(b'host', b'localhost:8000'), (b'user-agent', 
#     # b'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'), (b'accept', b'*/*'), (b'accept-language', b'en-US,en;q=0.5'), 
#     #              (b'accept-encoding', b'gzip, deflate'), (b'sec-websocket-version', b'13'), (b'origin', b'moz-extension://1932b244-4622-439d-92da-92f1211a658c'), 
#     #              (b'sec-websocket-extensions', b'permessage-deflate'), (b'sec-websocket-key', b'lJlL1iTPh3ICEYLtBkpvAg=='), (b'connection', b'keep-alive, Upgrade'),
#     #              (b'pragma', b'no-cache'), (b'cache-control', b'no-cache'), (b'upgrade', b'websocket')], 'query_string': b'', 
#     #  'client': ['127.0.0.1', 56412], 'server': ['127.0.0.1', 8000], 'subprotocols': [], 'asgi': {'version': '3.0'}, 
#     #  'cookies': {}, 'session': <django.utils.functional.LazyObject object at 0x000001A10A79BD60>, 
#     #  'user': <channels.auth.UserLazyObject object at 0x000001A10A79BEE0>, 'path_remaining': '', 
#     #  'url_route': {'args': (), 'kwargs': {'sender_id': 2, 'receiver_id': 1}}}