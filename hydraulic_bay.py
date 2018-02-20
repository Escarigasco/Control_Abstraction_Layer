# Bay Class
from bs4 import BeautifulSoup as Soup
from pipeline import pipeline
from bay_valve import bay_valve
from connector import connector


class hydraulic_bay(object):
    'Class for switch board definition and properties'

    def __init__(self, switch_board_ID, ID, bay):
        self.switch_board_ID = switch_board_ID
        self.ID = ID
        self.pipes_in_list = {}
        self.pipes_out_list = {}
        self.valves = {}
        self.bay = bay

        if (self.bay["connected_device"] == "source"):
            print("I am here")
            pipes_in = bay.find_all("pipe", type=["C", "B"])
            pipes_out = bay.find_all("pipe", type=["H", "B"])
        elif (bay["connected_device"] == "sink"):
            print("I am here")
            pipes_in = bay.find_all("pipe", type=["H", "B"])
            pipes_out = bay.find_all("pipe", type=["C", "B"])

        valves = bay.find_all("valve")

        for pipe in pipes_in:
            direction = "in"
            self.pipes_in_list[pipe["id"]] = pipeline(self.ID, pipe["id"], direction)
            print(pipe)

        for pipe in pipes_out:
            direction = "out"
            self.pipes_out_list[pipe["id"]] = pipeline(self.ID, pipe["id"], direction)

        for valve in valves:
            self.valves[valve["id"]] = bay_valve(self.ID, valve["id"])
            # self.bays_list[bay["id"]] = switch_board(bay["id"], bay)

        self.down_connection = connector(bay)

    def get_name(self):
        return self.ID

    def __repr__(self):
        return "<Bay, id: {0}, connected to: {1}>".format(self.ID, self.switch_board_ID)

    def __str__(self):
        return "<Bay, id: {0}, connected to: {1}>".format(self.ID, self.switch_board_ID)
