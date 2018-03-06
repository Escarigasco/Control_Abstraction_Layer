# Switch Board Building Class
from switch_board import switch_board
from bs4 import BeautifulSoup as Soup


class switch_board_building(object):
    'Class for switch board building definition and properties'

    def __init__(self, ID):  # inizialition with only ID
        self.ID = ID

        self.switch_board_list = {}  # create dic of switch board
        # handler = open(self.ID + ".xml").read()  # read xml
        handler = open("file.xml").read()
        soup = Soup(handler, 'lxml')

        boards = soup.find_all("switch_board")
        for board in boards:
            self.switch_board_list[board["id"]] = switch_board(self.ID, board["id"], board)

    def get_name(self):
        return self.ID


if __name__ == "__main__":
    test = switch_board_building("Building716")
