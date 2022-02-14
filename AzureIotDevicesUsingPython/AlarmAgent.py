import asyncio
import random
from datetime import datetime, timezone

from DeviceAgent import DeviceAgentState
from pb_AlarmStatus_pb2 import pb_AlarmStatus
from pb_Parcel_pb2 import pb_Parcel
from DeviceAgent import DeviceAgent

class AlarmAgent(DeviceAgent):
    def __init__(self, conn_str, agent_name, destination_name, logging):
        super(AlarmAgent, self).__init__(conn_str, agent_name, logging)
        self.destination_name = destination_name
        self.current_alarm_status = False
        self.new_alarm_status = False
        self.parcel_to_send = None

    def simulate_event(self):
        return bool(random.getrandbits(1))

    def pack_alarm_event(self):
        date_time_utc = datetime.now(timezone.utc)
        alarm_status = pb_AlarmStatus()
        alarm_status.alarm_active = self.current_alarm_status
        alarm_status.time_utc = "{}".format(date_time_utc.time())
        alarm_status.date_utc = "{}".format(date_time_utc.date())

        self.logging.info("*************************************************************************")
        self.logging.info("Packing event: Active: %r, time: %r, date: %r" % (alarm_status.alarm_active, alarm_status.time_utc, alarm_status.date_utc))
        self.logging.info("*************************************************************************")

        parcel = pb_Parcel()
        parcel.source.name = "Door Alarm"
        parcel.source.local_id = "1"
        parcel.source.domain_agent = self.agent_name
        parcel.source.domain = "Device Domain"
        parcel.destination.name = "Alarm Monitor"
        parcel.type = "pb_AlarmStatus"
        parcel.content = str(alarm_status.SerializeToString(), 'utf-8')
        self.parcel_to_send = str(parcel.SerializeToString(), 'utf-8')

    async def do_work(self):
        if self.state is DeviceAgentState.IDLE or self.state is DeviceAgentState.PROCESSING_DEVICE_TO_CLOUD_COMPLETED:
            self.new_alarm_status = self.simulate_event()

            if self.new_alarm_status == self.current_alarm_status:
                self.state = DeviceAgentState.IDLE
            else:
                self.current_alarm_status = self.new_alarm_status
                self.state = DeviceAgentState.NEW_EVENT_TO_PROCESS
            return

        if self.state is DeviceAgentState.NEW_EVENT_TO_PROCESS:
            self.pack_alarm_event()
            self.state = DeviceAgentState.PROCESSING_DEVICE_TO_CLOUD_STARTED
            return

        if self.state is DeviceAgentState.PROCESSING_DEVICE_TO_CLOUD_STARTED:
            await self.send_parcel(self.parcel_to_send)
            await asyncio.sleep(0.5) # Delayed for test
            self.parcel_to_send = None
            self.state = DeviceAgentState.PROCESSING_DEVICE_TO_CLOUD_COMPLETED
            return
