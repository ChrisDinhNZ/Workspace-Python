'''
Description: A helper class to interact with Azure IoT Hub.
'''

import asyncio

from azure.iot.device.aio import IoTHubDeviceClient

class AzureIotDeviceAgent:
   def __init__(self, name, connection_string, client = None):
      self.name= name
      self.device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
      self.client = client

   async def connect(self):
      await self.device_client.connect()

   async def disconnect(self):
      await self.device_client.disconnect()

   def set_client(self, client):
      self.client = client
