'''
Description: A simple class to handles button press event.
'''

import asyncio

class ButtonObserver:
   def __init__(self, agent = None):
      self.agent = agent

   async def handle_button_pressed(self, source):
      if self.agent is None:
         return

      if source == "A":
         self.agent.send_parcel("Button %r pressed" % source)
      else:
         self.agent.send_parcel("Button %r pressed" % source)

   def set_agent(self, agent):
      self.agent = agent
