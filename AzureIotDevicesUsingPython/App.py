'''
Description: An example of 2 "devices" communicating via Azure IoT Hub
'''
import asyncio
import os
import logging
import sys
from time import gmtime
import time

from AlarmAgent import AlarmAgent
from AlarmMonitorAgent import AlarmMonitorAgent

REQUIRED_DEVICES = 2

root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('events.log', 'w', 'utf-8')
formatter = logging.Formatter('%(asctime)s %(message)s')
formatter.converter = gmtime
handler.setFormatter(formatter)
root_logger.addHandler(handler)

def all_devices_are_connected(devices):
    return len(devices) == REQUIRED_DEVICES

async def disconnect_devices(devices):
    coroutines = []
    for device in devices:
        coroutines.append(device.disconnect())
    await asyncio.gather(*coroutines)

async def main():

    alarm_agent = None
    alarm_monitor_agent = None

    connected_devices = []

    try:
        logging.info("*** App Started...")

        # Get neccessary application configs
        alarm_agent_conn_str = os.getenv("AlarmAgentConnectionString")
        alarm_monitor_agent_conn_str = os.getenv("AlarmMonitorAgentConnectionString")
        alarm_agent_name = os.getenv("AlarmAgentName")
        alarm_monitor_agent_name = os.getenv("AlarmMonitorAgentName")

        # Connect our devices to IoT hub
        alarm_agent = AlarmAgent(alarm_agent_conn_str, alarm_agent_name, alarm_monitor_agent_name, logging)
        alarm_monitor_agent = AlarmMonitorAgent(alarm_monitor_agent_conn_str, alarm_monitor_agent_name, logging)
        await asyncio.gather(alarm_agent.connect(), alarm_monitor_agent.connect())

        if alarm_agent.is_connected():
            connected_devices.append(alarm_agent)

        if alarm_monitor_agent.is_connected():
            connected_devices.append(alarm_monitor_agent)

        if all_devices_are_connected(connected_devices) is False:
            await disconnect_devices(connected_devices)
            logging.error("Failed to connect necessary devices.")
            sys.exit()

        logging.info("All devices are connected.")
        start_time = time.time()

        while True:
            await alarm_agent.do_work()

            # Let alarm agent runs for 5 sec
            if (time.time() - start_time) > 5:
                break

        # Give alarm monitor some time before cleaning up connections.
        await asyncio.sleep(5)
        await disconnect_devices(connected_devices)

        logging.info("App Stopped!")
    except Exception:
        logging.error(Exception.with_traceback())

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
