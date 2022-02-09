
from DeviceAgent import DeviceAgent

class AlarmAgent(DeviceAgent):
    def __init__(self, conn_str, agent_name, destination_name, logging):
        super(AlarmAgent, self).__init__(conn_str, agent_name, logging)
        self.destination_name = destination_name
