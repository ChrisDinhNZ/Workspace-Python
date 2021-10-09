import asyncio
import sys

from bleak import BleakScanner
from bleak.backends.bluezdbus.client import BleakClientBlueZDBus

device_name = "My Arduino"
switch_status_char_uuid = "8158b2fe-94e4-4ff5-a99d-9a7980e998d7"


def notification_handler(sender, data):
    print("Switch is active: {}".format(bool(data[0])))


async def run():
    client = None
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name and d.name.lower() == device_name.lower()
    )

    if device is None:
        print("{} not found".format(device_name))
        sys.exit()
    else:
        print("{} found".format(device))

    client = BleakClientBlueZDBus(device)

    while True:
        if not client.is_connected:
            try:
                if await client.connect():
                    print("Connected to {}".format(device_name))
                    await client.start_notify(switch_status_char_uuid, notification_handler)
            except:
                print("Connected to {} failed or lost".format(device_name))
                await asyncio.sleep(1)
                client = BleakClientBlueZDBus(device)
                print("Retrying...")
        else:
            await asyncio.sleep(1)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
