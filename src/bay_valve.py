# Valve Class


class bay_valve:
    'Class for Valve definition and properties'

    def __init__(self, parent_ID, ID, connection, flow, direction):
        self.parent_ID = parent_ID
        self.ID = ID
        self.connection = connection
        self.flow = flow
        self.flow_direction = direction
        self.opening_threshold = 0.1

    def get_flow_direction(self):
        return self.flow_direction

    def get_name(self):
        return self.ID

    def get_flow(self):
        return self.flow

    def get_connection(self):
        return self.connection

    def get_parent(self):
        return self.parent_ID

    def set_status(self, status):
        if (status > self.opening_threshold):
            self.status = 1
        else:
            self.status = 0
        print(self.ID, self.status)

    def get_status(self):
        return self.status

    def __repr__(self):
        return "{0}".format(self.ID)

    def __str__(self):
        return "{0}".format(self.ID)
