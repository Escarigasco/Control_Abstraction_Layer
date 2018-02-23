# Switch Board Class
from bs4 import BeautifulSoup as Soup
from hydraulic_bay import hydraulic_bay


class switch_board(object):
    'Class for switch board definition and properties'

    def __init__(self, building_ID, ID, board):

        self.building_ID = building_ID
        self.ID = ID
        self.bays_list = {}
        self.board = board

        bays = self.board.find_all("bay")

        for bay in bays:
            self.bays_list[bay["id"]] = hydraulic_bay(self.ID, bay["id"], bay)
            print(self.ID)
            print(self.bays_list)

    def get_name(self):
        return self.ID

    def __repr__(self):
        return "<Switch Board, id: {0}>".format(self.ID)

    def __str__(self):
        return "<Switch Board, id: {0}>".format(self.ID)
