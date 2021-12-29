'''
Description: A simple class to monitor button or switch via a GPIO input.
'''

from gpiozero import Button
import asyncio

class ButtonMonitor:
   def __init__(self, input_pin, name, observer):
      self.button = Button(input_pin)
      self.button_name = name
      self.observer = observer

      self.button.when_pressed = self.button_pressed

   async def button_pressed(self):
      if self.observer is None:
         pass  # No observer so do nothing
      else:
         # Create new asyncio loop
         loop = asyncio.new_event_loop()
         asyncio.set_event_loop(loop)
         future = asyncio.ensure_future(self.__execute_when_pressed__(self.button_name)) # Execute async method
         loop.run_until_complete(future)
         loop.close()

   async def __execute_when_pressed__(self, source):
      await self.observer.handle_button_pressed(source)