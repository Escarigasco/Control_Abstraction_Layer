# Class for interface


class interface(object):

    def __init__(self, building, board_ID):
        self.building = building
        self.board = self.building.switch_board_list[board_ID]   # good practice to short names
        self.sensors_lists = {}  # redundant definition for intelligibility
        self.pumps_list = {}  # redundant definition for intelligibility

    def get_hydraulic_bay(self, switch_board, hydraulic_bay_ID):
        return switch_board.bays_list[hydraulic_bay_ID]

    def get_system_sensors(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity

        for bay in bays_list.keys():  # parsing dictionary keys
            print(bay)
            hydraulic_bay = bays_list[bay]
            bay_connectors_list = hydraulic_bay.connectors_list

            for connector in bay_connectors_list.keys():
                print(connector)
                bay_connector = bay_connectors_list[connector]
                connector_sensors_lists = bay_connector.connector_sensors_list
                lines_list = bay_connector.lines_list

                line_sensors_list = {}
                for line in lines_list.keys():
                        print(line)
                        connector_line = lines_list[line]
                        line_sensors_list.update(connector_line.line_sensors_list)  # add sensors list from each line

        self.sensors_lists = {**connector_sensors_lists, **line_sensors_list}
        for key in self.sensors_lists.keys():
            print(self.sensors_lists[key].get_name())

    def get_system_pumps(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity

        for bay in bays_list.keys():  # parsing dictionary keys
            print(bay)
            hydraulic_bay = bays_list[bay]
            bay_connectors_list = hydraulic_bay.connectors_list

            for connector in bay_connectors_list.keys():
                print(connector)
                bay_connector = bay_connectors_list[connector]
                lines_list = bay_connector.lines_list

                line_pumps_list = {}
                for line in lines_list.keys():
                        print(line)
                        connector_line = lines_list[line]
                        line_pumps_list.update(connector_line.pumps_list)  # add pumps list from each line

        self.pumps_list = line_pumps_list
        for key in self.pumps_list.keys():
            print(self.pumps_list[key].get_name())
