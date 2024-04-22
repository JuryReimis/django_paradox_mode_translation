import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        chat_url = self.scope['url_route'].get('kwargs', {}).get('chat_url')
        await self.accept()
        print('connect', chat_url)
        if chat_url:
            await self.channel_layer.group_add(
                group=chat_url,
                channel=self.channel_name
            )
        else:
            await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        await super(ChatConsumer, self).receive(text_data, bytes_data)

    async def send(self, text_data=None, bytes_data=None, close=False):
        await super(ChatConsumer, self).send(text_data, bytes_data, close)

    async def message_send_chat(self, event):
        text_data = json.dumps({
            'author': event.get('author'),
            'body': event.get('body'),
            'pub_date': event.get('pub_date')
        })
        await self.send(text_data)
