import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import WaterLevel

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send_last_data()

    @database_sync_to_async
    def get_last_data(self):
        return WaterLevel.objects.last()

    async def send_last_data(self):
        data = await self.get_last_data()
        if data:
            await self.send(json.dumps({
                'distance': data.distance,
                'ph': data.ph_value,
                'tds': data.tds_value,
                'timestamp': data.timestamp.isoformat(),
            }))