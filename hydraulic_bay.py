# Bay Class
from bs4 import BeautifulSoup as Soup
from pipeline import pipeline
from bay_valve import bay_valve


class hydraulic_bay(object):
    'Class for switch board definition and properties'

    def __init__(self, switch_board_ID, ID, soup):
        self.switch_board_ID = switch_board_ID
        self.ID = ID
        self.pipes_in_list = {}
        self.pipes_out_list = {}
        self.valves = {}

        pipes_in = soup.find_all("pipe_in")
        pipes_out = soup.find_all("pipe_out")
        valves = soup.find_all("valve")

        for pipe in pipes_in:
            direction = "in"
            self.pipes_in_list[pipe["id"]] = pipeline(self.ID, pipe["id"], direction)

        for pipe in pipes_out:
            direction = "out"
            self.pipes_out_list[pipe["id"]] = pipeline(self.ID, pipe["id"], direction)

        for valve in valves:
            self.valves[valve["id"]] = bay_valve(self.ID, valve["id"])
            # self.bays_list[bay["id"]] = switch_board(bay["id"], bay)

    def get_name(self):
        return self.ID

    def __repr__(self):
        return "<Bay, id: {0}, connected to: {1}>".format(self.ID, self.switch_board_ID)

    def __str__(self):
        return "<Bay, id: {0}, connected to: {1}>".format(self.ID, self.switch_board_ID)
