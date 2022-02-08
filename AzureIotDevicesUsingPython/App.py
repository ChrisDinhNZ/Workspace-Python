'''
Description: An example of 2 "devices" communicating via Azure IoT Hub
'''
import asyncio
import os
import sys
import signal
import logging
import threading
from time import gmtime

from AlarmAgent import AlarmAgent
from AlarmMonitorAgent import AlarmMonitorAgent

logging.basicConfig(filename='events.log', encoding='utf-8', format='%(asctime)s %(message)s', level=logging.DEBUG)
logging.Formatter.converter = gmtime

async def main():

    execution_is_over = asyncio.Future()

    def abort_handler(*args):
        execution_is_over.set_result("Ctrl+C")
        logging.info('App Stopped.')
        sys.exit(0)

    signal.signal(signal.SIGINT, abort_handler)

    try:
        logging.info("App Started...")

        # Read necessary configuration data from environment variables
        alarm_agent_conn_str = os.getenv("AlarmAgentConnectionString")
        alarm_monitor_agent_conn_str = os.getenv("AlarmMonitorAgentConnectionString")
        alarm_agent_name = os.getenv("SourceName")
        alarm_monitor_agent_name = os.getenv("DestinationName")

        logging.info('SourceName: %r' % alarm_agent_name)

        # Get Alarm Agent up and running
        alarm_agent = AlarmAgent(alarm_agent_conn_str, alarm_agent_name, alarm_monitor_agent_name, logging)
        alarm_agent_worker = threading.Thread(target=alarm_agent.start_work)
        alarm_agent_worker.daemon = True
        alarm_agent_worker.start()

        # Get Alarm Monitor Agent up and running
        alarm_monitor_agent = AlarmMonitorAgent(alarm_monitor_agent_conn_str, alarm_monitor_agent_name, logging)
        alarm_monitor_agent_worker = threading.Thread(target=alarm_monitor_agent.start_work)
        alarm_monitor_agent_worker.daemon = True
        alarm_monitor_agent_worker.start()

        exit_reason = await execution_is_over

    except Exception:
        logging.error(Exception.with_traceback())

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
