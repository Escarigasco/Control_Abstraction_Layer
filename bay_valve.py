# Valve Class


class bay_valve:
    'Class for Valve definition and properties'

    def __init__(self, bay_ID, ID, connection, flow):
        self.bay_ID = bay_ID
        self.ID = ID
        self.connection = connection
        self.flow = flow

    def get_name(self):
        return self.ID

    def set_position(self, setpoint):
        self.position = setpoint

    def get_position(self):
        return self.position  # this needs to be real time read

    def __repr__(self):
        return "<Valve, id: {0}>".format(self.ID)

    def __str__(self):
        return "<Valve, id: {0}>".format(self.ID)
