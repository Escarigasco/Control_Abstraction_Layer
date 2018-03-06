# Valve Class


class bay_valve:
    'Class for Valve definition and properties'

    def __init__(self, parent_ID, ID, connection, flow):
        self.parent_ID = parent_ID
        self.ID = ID
        self.connection = connection
        self.flow = flow

    def get_name(self):
        return self.ID

    def get_flow(self):
        return self.flow

    def get_parent(self):
        return self.parent_ID

    def get_position(self):
        return self.position  # this needs to be real time read

    def __repr__(self):
        return "<Valve, id: {0}>".format(self.ID)

    def __str__(self):
        return "<Valve, id: {0}>".format(self.ID)
