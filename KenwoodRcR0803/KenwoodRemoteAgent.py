'''
Description: A helper class to simulate a Kenwood RC-R0803 remote over BlE.
'''


import asyncio
from bleak import BleakScanner
from bleak.backends.bluezdbus.client import BleakClientBlueZDBus

class KenwoodRemoteAgent:
    def __init__(self, device_name, data_channel_uuid, logger):
        self.device_name = device_name
        self.data_channel_uuid = data_channel_uuid
        self.logger = logger
        self.device_found = False
        self.device_connected = False
        self.client = None

    async def run(self):
        while not self.device_found:
            device = await BleakScanner.find_device_by_filter(
                lambda d, ad: d.name and d.name.lower() == self.device_name.lower()
            )

            if device is None:
                self.logger.info("{} not found".format(self.device_name))
                await asyncio.sleep(1)
            else:
                self.logger.info("{} found".format(device))
                self.device_found = True

        self.client = BleakClientBlueZDBus(device)

        while not self.device_connected:
            try:
                if await self.client.connect():
                    self.device_connected = True
                    self.logger.info("Connected to {}".format(self.device_name))
            except:
                self.logger.info("Connected to {} failed".format(self.device_name))

            if not self.device_connected:
                await asyncio.sleep(1)
                self.logger.info("Retrying...")

    async def send_command(self, command: str):
        await self.client.write_gatt_char(self.data_channel_uuid, command.encode('UTF-8'))

    async def stop(self):
        if not self.device_connected:
            return

        try:
            if await self.client.disconnect():
                self.device_connected = False
                self.logger.info("Disconnected from {}".format(self.device_name))
        except:
            self.logger.info("Disconnected from {} failed".format(self.device_name))
