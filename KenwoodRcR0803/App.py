'''
Description: Simple app to interact with HM-10 BLE module.
'''
import asyncio
import logging
import signal
from time import gmtime
from AzureIotDeviceAgent import AzureIotDeviceAgent

from KenwoodRemoteAgent import KenwoodRemoteAgent

logging.basicConfig(filename='/home/pi/MyHomeAgent/events.log', encoding='utf-8', format='%(asctime)s %(module)-20s %(message)s', level=logging.DEBUG)
logging.Formatter.converter = gmtime

device_name = "KR-V7080"
data_channel_uuid = "0000ffe1-0000-1000-8000-00805f9b34fb"
my_home_agent_name = "MyHomeAgent"
my_home_agent_connection_string = "my-home-agent-connection-string"

async def main():

    my_home_agent = None
    kenwood_remote_agent = None
    execution_is_over = asyncio.Future()

    async def abort_handler(signame):
        execution_is_over.set_result("Ctrl+C")
        logging.info("Cleaning up before exiting...")

        if kenwood_remote_agent is not None:
            await kenwood_remote_agent.stop()

        if my_home_agent is not None:
            await my_home_agent.disconnect()

    loop = asyncio.get_event_loop()
    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame),
                                lambda: asyncio.ensure_future(abort_handler(signame)))

    try:
        logging.info("Started...")
        kenwood_remote_agent = KenwoodRemoteAgent(device_name, data_channel_uuid, logging)
        await kenwood_remote_agent.run()

        my_home_agent = AzureIotDeviceAgent(my_home_agent_name, my_home_agent_connection_string, logging)
        await my_home_agent.connect()
        my_home_agent.add_client(kenwood_remote_agent)

        await execution_is_over
        asyncio.get_event_loop().stop()

    except Exception:
        if my_home_agent is not None:
            my_home_agent.disconnect()

        if kenwood_remote_agent is not None:
            await kenwood_remote_agent.stop()

        logging.error("Stopped!")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
