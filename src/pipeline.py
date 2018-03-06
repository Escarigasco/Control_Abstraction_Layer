# Pipeline Class
from bay_valve import bay_valve


class pipeline(object):
    'Class for Pipeline definition and properties'

    def __init__(self, parent_ID, ID, pipe, busbar, direction):
        self.parent_ID = parent_ID
        self.ID = ID
        self.pipe = pipe
        self.direction = direction
        self.valves_list = {}
        self.busbar = busbar

        valves = self.pipe.find_all("valve")     # find valves

        for valve in valves:
            self.valves_list[valve["id"]] = bay_valve(self.ID, valve["id"], valve["connection"], valve["flow"])  # creates valves

    def get_name(self):
        return self.ID

    def get_busbar_connection(self):
        return self.busbar

    def __repr__(self):
        return "<Pipe, id: {0}>".format(self.ID)

    def __str__(self):
        return "<Pipe, id: {0}>".format(self.ID)
