class AlarmMonitorAgent:
    def __init__(self, conn_str, agent_name, logging):
        self.conn_str = conn_str
        self.agent_name = agent_name
        self.logging = logging

    def start_work(self):
        self.logging.info("AlarmMonitorAgent Started...")