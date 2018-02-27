# Bay Class
from pipeline import pipeline
from bay_valve import bay_valve
from bay_connector import bay_connector


class hydraulic_bay(object):
    'Class for switch board definition and properties'

    def __init__(self, parent_ID, ID, bay):
        self.parent_ID = parent_ID
        self.ID = ID
        self.pipes_in_list = {}
        self.pipes_out_list = {}
        self.valves_list = {}
        self.bay = bay
        self.connectors_list = {}

        connector = self.bay.find("connector")  # find connectors
        valves = self.bay.find_all("valve")     # find valves

        if (self.bay["connected_device"] == "source"):
            output_line = "H"  # discrimination for the connector
            pipes_in = self.bay.find_all("pipe", busbar=["1C", "2C", "B"])   # find inlet pipes
            pipes_out = self.bay.find_all("pipe", busbar=["1H", "2H", "B"])  # find outlet pipes
            self.connectors_list[connector["id"]] = bay_connector(self.ID, connector["id"], connector, output_line)  # create connectors object

        elif (bay["connected_device"] == "sink"):
            output_line = "C"  # discrimination for the connector
            pipes_in = self.bay.find_all("pipe", busbar=["1H", "2H", "B"])   # find inlet pipes
            pipes_out = self.bay.find_all("pipe", busbar=["1C", "2C", "B"])  # find inlet pipes
            self.connectors_list[connector["id"]] = bay_connector(self.ID, connector["id"], connector, output_line)  # create connectors object

        for pipe in pipes_in:
            direction = "in"
            self.pipes_in_list[pipe["id"]] = pipeline(self.ID, pipe["id"], direction)  # creates pipes

        for pipe in pipes_out:
            direction = "out"
            self.pipes_out_list[pipe["id"]] = pipeline(self.ID, pipe["id"], direction)  # creates pipes

        for valve in valves:
            self.valves_list[valve["id"]] = bay_valve(self.ID, valve["id"], valve["connection"], valve["flow"])  # creates valves

    def get_parent(self):
        return self.parent_ID

    def get_name(self):
        return self.ID

    def __repr__(self):
        return "<Bay, id: {0}, connected to: {1}>".format(self.ID, self.switch_board_ID)

    def __str__(self):
        return "<Bay, id: {0}, connected to: {1}>".format(self.ID, self.switch_board_ID)
