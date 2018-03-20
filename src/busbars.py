# Class for busbars


class busbar(object):

    def __init__(self, circuit_ID, system_pipes, status):
        self.system_pipes = system_pipes
        self.circuit_ID = circuit_ID
        self.status = status

    def get_status():
        return self.status

    def get_pipes(self):
        return self.system_pipes

    def get_name(self):
        return self.circuit_ID

    def __repr__(self):
        return "id: {0}".format(self.circuit_ID)

    def __str__(self):
        return "id:{0}>".format(self.circuit_ID)
