# Sensor


class system_sensor:

    def __init__(self, parent_ID, ID, controlled_variable, device_embedded, position):
        self.parent_ID = parent_ID  # this could be anything - bb, bay, connector, pipe
        self.ID = ID
        self.variable = controlled_variable  # Temp, Flow, etc..
        self.device_embedded = device_embedded  # if it belongs to larger sensor
        self.position = position  # is in the pipe or in the connector or anywhere else - redundant with parent_ID?

        # print(self.ID)
    def set_bay(self, bay_ID):
        self.bay_ID = bay_ID

    def get_parent(self):
        return self.parent_ID

    def get_name(self):
        return self.ID

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def __repr__(self):
        return "{0}".format(self.ID)

    def __str__(self):
        return "{0}".format(self.ID)
