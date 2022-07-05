'''
Description: A helper class to interact with Azure IoT Hub.
'''

import logging
from pb_Parcel_pb2 import pb_Parcel
from azure.iot.device.aio import IoTHubDeviceClient
from google.protobuf import json_format
from azure.iot.device import MethodResponse

class AzureIotDeviceAgent:
    def __init__(self, name: str, connection_string: str, logger: logging):
        self.name= name
        self.device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
        self.device_client.on_method_request_received = self.method_request_handler
        self.logger = logger
        self.clients = []

    async def connect(self):
        if self.device_client.connected:
            return

        await self.device_client.connect()
        self.logger.info("{} connected".format(self.name))

    async def disconnect(self):
        if not self.device_client.connected:
            return

        await self.device_client.disconnect()
        self.logger.info("{} disconnected".format(self.name))

    # Add handler for incoming parcels
    def add_client(self, client):
        self.clients.append(client)

    async def send_parcel(self, parcel: pb_Parcel):
        if not self.device_client.connected:
            self.logger.error("{} not connected".format(self.name))
            return

        # Populate source domain and domain agent
        parcel.source.domain_agent = self.name
        parcel.source.domain = "Device Domain"
        parcel = parcel.SerializeToString()

        # Note that parcel here is serialised to a byte array, not UTF8 string.
        await self.device_client.send_message(parcel)

    async def method_request_handler(self, method_request):
        status_code = 200
        payload = {"result": True, "data": "parcel handled"}

        if method_request.name != "ProcessMessage":
            status_code = 404
            payload = {"result": False, "data": "unknown method request"}

        parcel = json_format.ParseDict(method_request.payload, pb_Parcel(), True)

        if parcel is None:
            status_code = 400
            payload = {"result": False, "data": "no parcel received"}
        else:
            handler_found = False
            for client in self.clients:
                if client.name == parcel.destination.name:
                    handler_found = True
                    await client.process_parcel(parcel)
                    break
            if not handler_found:
                status_code = 503
                payload = {"result": False, "data": "no parcel handler"}

        method_response = MethodResponse.create_from_method_request(method_request, status_code, payload)
        await self.device_client.send_method_response(method_response)
