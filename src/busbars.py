# Class for busbars
_FIRST_OF_THE_CLASS = 0


class busbar(object):

    def __init__(self, circuit_ID, system_pipes):
        self.system_pipes = system_pipes
        self.circuit_ID = circuit_ID
        self.set_flow_and_type()

    def set_flow_and_type(self):
        self.type = self.system_pipes[_FIRST_OF_THE_CLASS].type
        valve_name = self.system_pipes[_FIRST_OF_THE_CLASS].valves_list.keys()
        for name in valve_name:
            self.flow = self.system_pipes[_FIRST_OF_THE_CLASS].valves_list[name].get_flow()

    def get_pipes(self):
        return self.system_pipes

    def get_name(self):
        return self.circuit_ID

    def __repr__(self):
        return "id: {0}".format(self.circuit_ID)

    def __str__(self):
        return "id:{0}>".format(self.circuit_ID)
