'''
Description: Monitors button/switch connected to GPIO input 2 and 3.
'''
import asyncio
import sys
import signal

from ButtonMonitor import ButtonMonitor
from ButtonObserver import ButtonObserver
from AzureIotDeviceAgent import AzureIotDeviceAgent

async def main():

    my_home_agent = None
    observer = None
    my_home_agent_name = "MyHomeAgent"
    my_home_agent_connection_string = "my-home-agent-connection-string"

    execution_is_over = asyncio.Future()

    def abort_handler(*args):
        execution_is_over.set_result("Ctrl+C")
        if my_home_agent is not None:
            my_home_agent.disconnect() # Todo: this will result in "never awaited" error
        print("")
        print("Cleaning up before exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, abort_handler)

    try:
        observer = ButtonObserver()
        ButtonMonitor(2, "A", observer)  # Monitor button connected to input 2
        ButtonMonitor(3, "B", observer)  # Monitor button connected to input 3

        my_home_agent = AzureIotDeviceAgent(my_home_agent_name, my_home_agent_connection_string)
        await my_home_agent.connect()

        observer.set_agent(my_home_agent)
        my_home_agent.set_client(observer)

        exit_reason = await execution_is_over
        print('Exit reason detected: %r' % exit_reason)

    finally:
        pass

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
