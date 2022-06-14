'''
Description: Simple app to interact with HM-10 BLE module.
'''
import asyncio
import logging
import signal
import sys
from time import gmtime
from turtle import delay

from KenwoodRemoteAgent import KenwoodRemoteAgent

logging.basicConfig(filename='/home/pi/MyHomeAgent/events.log', encoding='utf-8', format='%(asctime)s %(module)-20s %(message)s', level=logging.DEBUG)
logging.Formatter.converter = gmtime

device_name = "RC-R0803"
data_channel_uuid = "0000ffe1-0000-1000-8000-00805f9b34fb"

async def main():

    kenwood_remote_agent = None
    execution_is_over = asyncio.Future()

    async def abort_handler(signame):
        execution_is_over.set_result("Ctrl+C")
        logging.info("Cleaning up before exiting...")

        if kenwood_remote_agent is not None:
            await kenwood_remote_agent.stop()

    loop = asyncio.get_event_loop()
    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame),
                                lambda: asyncio.ensure_future(abort_handler(signame)))

    try:
        logging.info("Started...")
        kenwood_remote_agent = KenwoodRemoteAgent(device_name, data_channel_uuid, logging)
        await kenwood_remote_agent.run()

        # Send command to toggle power on/off
        await kenwood_remote_agent.send_command("power#")
        await asyncio.sleep(3)
        # Send an unknown command
        await kenwood_remote_agent.send_command("Blah blah#")

        await execution_is_over
        asyncio.get_event_loop().stop()

    except Exception:
        logging.error("Stopped!")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
