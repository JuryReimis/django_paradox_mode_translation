import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ProfileInfoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        username = self.scope.get('user').username
        await self.accept()
        await self.channel_layer.group_add(
            username,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def send(self, text_data=None, bytes_data=None, close=False):

        await super(ProfileInfoConsumer, self).send(text_data, bytes_data, close)

    async def message_update_invite_count(self, event):
        text_data = json.dumps({
            'new_count': event.get('new_count')
        })
        await self.send(text_data)
