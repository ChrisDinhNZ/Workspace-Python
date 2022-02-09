from DeviceAgent import DeviceAgent

class AlarmMonitorAgent(DeviceAgent):
    def __init__(self, conn_str, agent_name, logging):
        super(AlarmMonitorAgent, self).__init__(conn_str, agent_name, logging)
