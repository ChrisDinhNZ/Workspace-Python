from pb_AlarmStatus_pb2 import pb_AlarmStatus
from pb_Parcel_pb2 import pb_Parcel
from DeviceAgent import DeviceAgent
from azure.iot.device import MethodResponse
from google.protobuf import json_format

class AlarmMonitorAgent(DeviceAgent):
    def __init__(self, conn_str, agent_name, logging):
        super(AlarmMonitorAgent, self).__init__(conn_str, agent_name, logging)
        self.device_client.on_method_request_received = self.method_request_handler

    async def method_request_handler(self, method_request):
        status_code = 200
        payload = {"result": True, "data": "parcel handled"}

        if method_request.name != "ProcessMessage":
            status_code = 404
            payload = {"result": False, "data": "unknown method request"}

        parcel = json_format.ParseDict(method_request.payload, pb_Parcel(), True)

        if parcel is None or parcel.type != "pb_AlarmStatus":
            status_code = 400
            payload = {"result": False, "data": "bad parcel received"}
        else:
            alarm_status = pb_AlarmStatus()
            alarm_status.ParseFromString(bytes(parcel.content, 'utf-8'))
            self.logging.info("****************************************************************************")
            self.logging.info("Alarm status received from: %r" % (parcel.source.name))
            self.logging.info("alarm_active: %r, time_utc: %r, date_utc: %r" % (alarm_status.alarm_active, alarm_status.time_utc, alarm_status.date_utc))
            self.logging.info("****************************************************************************")

        method_response = MethodResponse.create_from_method_request(method_request, status_code, payload)
        await self.device_client.send_method_response(method_response)
