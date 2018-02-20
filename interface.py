# Class for interface


class interface(object):

    def __init__(self, building):
        self.building = building

    def get_switch_board(self, board_ID):
        return self.building.switch_board_list[board_ID]

    def get_hydraulic_bay(self, switch_board, hydraulic_bay_ID):
        return switch_board.bays_list[hydraulic_bay_ID]
