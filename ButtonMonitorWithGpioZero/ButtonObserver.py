'''
Description: A simple class to handles button press event.
'''

import asyncio

from pb_Parcel_pb2 import pb_Parcel

class ButtonObserver:
   def __init__(self, agent = None):
      self.agent = agent

   def __pack_button_event__(self, assistance_requested):
      parcel = pb_Parcel()

      # We don't need to populate domain and domain agent, that will
      # be done by the domain agent.
      parcel.source.name = "My Pager"
      parcel.source.local_id = parcel.source.name

      # We only need to indicate destination endpoint name here.
      # Other info will be derived by backend services.
      parcel.destination.name = "MyMobile"

      parcel.type = "ASCII"

      # In this case, the content is just a string. However if content
      # were a protobuffer object, then we will need convert it to a string
      # as SerializeToString() returns a byte array.
      # e.g. parcel.content = str(content.SerializeToString(), 'utf-8')
      if assistance_requested:
         parcel.content = "Panic button activated"
      else:
         parcel.content = "Panic button cancelled"

      return parcel

   async def handle_button_pressed(self, source):
      if self.agent is None:
         return

      assistance_requested = False

      if source == "A":
         assistance_requested = True

      parcel = self.__pack_button_event__(assistance_requested)
      await self.agent.send_parcel(parcel)

   def set_agent(self, agent):
      self.agent = agent
