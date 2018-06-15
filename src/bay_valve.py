# Valve Class
from random import choice

class bay_valve(object):
    'Class for Valve definition and properties'

    def __init__(self, parent_ID, ID, connection, flow, direction, connected_dev, status=None, opening_score=0):
        self.parent_ID = parent_ID
        self.ID = ID
        self.connection = connection
        self.flow = flow
        self.flow_direction = direction
        self.location = connected_dev
        self.object_type = "Valve"

        #self.opening_threshold = 0.1
        self.opening_threshold = 20
        if status is None:
            status = choice([1, 1, 1])
        self.status = status

    def score_calculator(self, value):
        self.opening_score = value

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
            self.status = status
            #print(self.ID, self.status)

    def get_status(self):
        return self.status

    def __repr__(self):
        return "-{0}-".format(self.ID)

    def __str__(self):
        return "-{0}-".format(self.ID)
