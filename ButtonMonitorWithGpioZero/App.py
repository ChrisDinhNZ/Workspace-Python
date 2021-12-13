'''
Description: Monitors button/switch connected to GPIO input 2 and 3.
'''
import asyncio
import sys
import signal

from ButtonMonitor import ButtonMonitor
from ButtonObserver import ButtonObserver

async def main():

    execution_is_over = asyncio.Future()

    def abort_handler(*args):
        execution_is_over.set_result("Ctrl+C")
        print("")
        print("Cleaning up before exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, abort_handler)

    try:
        observer = ButtonObserver()
        ButtonMonitor(2, "A", observer)  # Monitor button connected to input 2
        ButtonMonitor(3, "B", observer)  # Monitor button connected to input 3

        exit_reason = await execution_is_over
        print('Exit reason detected: %r' % exit_reason)

    finally:
        pass

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
