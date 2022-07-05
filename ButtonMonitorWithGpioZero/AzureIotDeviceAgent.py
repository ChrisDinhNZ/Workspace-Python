'''
Description: A helper class to interact with Azure IoT Hub.
'''

from pb_Parcel_pb2 import pb_Parcel
from azure.iot.device.aio import IoTHubDeviceClient

class AzureIotDeviceAgent:
   def __init__(self, name, connection_string, client = None):
      self.name= name
      self.device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
      self.client = client

   async def connect(self):
      if self.device_client.connected:
         return

      await self.device_client.connect()

   async def disconnect(self):
      if not self.device_client.connected:
         return

      await self.device_client.disconnect()

   def set_client(self, client):
      self.client = client

   async def send_parcel(self, parcel: pb_Parcel):
      if not self.device_client.connected:
         return

      # Populate source domain and domain agent
      parcel.source.domain_agent = self.name
      parcel.source.domain = "Device Domain"
      parcel = parcel.SerializeToString()

      # Note that parcel here is serialised to a byte array, not UTF8 string.
      await self.device_client.send_message(parcel)
