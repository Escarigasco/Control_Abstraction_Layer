# Class for interface


class interface(object):

    def __init__(self, building, board_ID):
        self.building = building
        self.board = self.building.switch_board_list[board_ID]   # good practice to short names
        self.sensors_lists = {}  # redundant definition for intelligibility
        self.pumps_list = {}  # redundant definition for intelligibility
        self.pipes_list = {}

    def get_hydraulic_bay(self, switch_board, hydraulic_bay_ID):
        return switch_board.bays_list[hydraulic_bay_ID]

    def get_system_sensors(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity

        for bay in bays_list.keys():  # parsing dictionary keys
            hydraulic_bay = bays_list[bay]
            bay_connectors_list = hydraulic_bay.connectors_list

            for connector in bay_connectors_list.keys():
                bay_connector = bay_connectors_list[connector]
                connector_sensors_lists = bay_connector.connector_sensors_list
                lines_list = bay_connector.lines_list

                line_sensors_list = {}
                for line in lines_list.keys():
                        connector_line = lines_list[line]
                        line_sensors_list.update(connector_line.line_sensors_list)  # add sensors list from each line

        self.sensors_lists = {**connector_sensors_lists, **line_sensors_list}

        return self.sensors_lists

    def get_system_pumps(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity

        for bay in bays_list.keys():  # parsing dictionary keys
            hydraulic_bay = bays_list[bay]
            bay_connectors_list = hydraulic_bay.connectors_list

            for connector in bay_connectors_list.keys():
                bay_connector = bay_connectors_list[connector]
                lines_list = bay_connector.lines_list

                line_pumps_list = {}
                for line in lines_list.keys():
                        connector_line = lines_list[line]
                        line_pumps_list.update(connector_line.pumps_list)  # add pumps list from each line

        self.pumps_list = line_pumps_list
        return self.pumps_list

    def get_system_valves(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity

        bay_valves_list = {}
        for bay in bays_list.keys():  # parsing dictionary keys
            hydraulic_bay = bays_list[bay]
            bay_valves_list.update(hydraulic_bay.valves_list)

        self.bay_valves_list = bay_valves_list
        return self.bay_valves_list

    def get_system_pipes(self):
        bays_list = self.board.bays_list  # ridefinition of variable for clarity

        pipes_in_list = {}   # ridefinition of variable for clarity
        pipes_out_list = {}

        for bay in bays_list.keys():  # parsing dictionary keys
            hydraulic_bay = bays_list[bay]
            pipes_in_list.update(hydraulic_bay.pipes_in_list)
            pipes_out_list.update(hydraulic_bay.pipes_out_list)

        self.pipes_in_list = pipes_in_list
        self.pipes_out_list = pipes_out_list
        self.pipes_list["in"] = self.pipes_in_list
        self.pipes_list["out"] = self.pipes_out_list

        return self.pipes_list

    def get_all_parents(self):  # return a list of all possible superstructure within a swithcboard
        bays_list = self.board.bays_list

        bay_connectors_list = {}
        for bay in bays_list.keys():
            hydraulic_bay = bays_list[bay]
            bay_connectors_list.update(hydraulic_bay.connectors_list)  # computing burden
            list_for_iteration = hydraulic_bay.connectors_list

            connector_lines_list = {}
            for connector in list_for_iteration.keys():
                bay_connector = list_for_iteration[connector]
                connector_lines_list.update(bay_connector.lines_list)

        parents_list = {**bays_list, **bay_connectors_list, **connector_lines_list}
        return parents_list
