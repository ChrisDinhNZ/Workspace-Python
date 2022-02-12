from azure.iot.device.aio import IoTHubDeviceClient
from enum import Enum

class DeviceAgentState(Enum):
    UNKNOWN = 1
    IDLE = 2
    NEW_EVENT_TO_PROCESS = 3
    PROCESSING_DEVICE_TO_CLOUD_STARTED = 4
    PROCESSING_DEVICE_TO_CLOUD_COMPLETED = 5

class DeviceAgent:
    def __init__(self, conn_str, agent_name, logging):
        self.agent_name = agent_name
        self.logging = logging

        self.device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
        self.state = DeviceAgentState.IDLE

    async def connect(self):
        await self.device_client.connect()

    async def disconnect(self):
        await self.device_client.disconnect()

    def is_connected(self):
        return self.device_client.connected

    async def send_parcel(self, parcel):
        await self.device_client.send_message(parcel)
