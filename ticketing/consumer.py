# customer.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the ticket ID from the URL and add the user to the ticket's communication group
        ticket_id = self.scope['url_route']['kwargs']['pk']
        self.ticket_group_name = f'ticket_{ticket_id}'
        await self.channel_layer.group_add(self.ticket_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Remove the user from the ticket's communication group
        await self.channel_layer.group_discard(self.ticket_group_name, self.channel_name)

    async def receive(self, text_data):
        # Process the received message
        message = json.loads(text_data)['message']
        # Implement your logic here to handle the incoming message and perform appropriate actions
        
        # Broadcast the message to the ticket's communication group
        await self.channel_layer.group_send(
            self.ticket_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    async def chat_message(self, event):
        # Send the message to the WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
