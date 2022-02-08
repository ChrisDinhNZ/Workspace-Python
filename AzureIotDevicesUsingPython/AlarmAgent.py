import asyncio
from azure.iot.device.aio import IoTHubDeviceClient

class AlarmAgent:
    def __init__(self, conn_str, agent_name, destination_name, logging):
        self.agent_name = agent_name
        self.destination_name = destination_name
        self.logging = logging

        self.device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    def start_work(self):
        self.logging.info("AlarmAgent Started...")
        asyncio.run(self.connect())

    async def connect(self):
        await self.device_client.connect()