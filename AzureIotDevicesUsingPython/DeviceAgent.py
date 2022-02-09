from azure.iot.device.aio import IoTHubDeviceClient

class DeviceAgent:
    def __init__(self, conn_str, agent_name, logging):
        self.agent_name = agent_name
        self.logging = logging

        self.device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    async def connect(self):
        await self.device_client.connect()

    async def disconnect(self):
        await self.device_client.disconnect()

    def is_connected(self):
        return self.device_client.connected
