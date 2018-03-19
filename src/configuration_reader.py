from switch_board_building import switch_board_building
from interface import interface
from object_tracker import object_tracker
from class_server import simple_data


class configuration_reader(object):

    def __init__(self, BuildingID, SwitchID):
        self.BuildingID = BuildingID
        self.SwitchID = SwitchID
        self.building716 = switch_board_building(self.BuildingID)
        self.config_reader = interface(self.building716, self.SwitchID)
        self.objtk = object_tracker(self.config_reader)


        self.system_bays =
        self.system_pumps = self.config_reader.get_system_pumps()
        self.system_valves = self.config_reader.get_system_valves()
        self.system_valves = self.config_reader.get_system_valves()
        self.system_connectors = self.config_reader.get_system_connectors()
        self.system_lines = self.config_reader.get_system_lines()
        self.system_pipes = self.config_reader.get_system_pipes()
        self.system_connected_devices = self.config_reader.get_connected_devices()
        self.system_bays = self.config_reader.get_hydraulic_bays()
        self.system_busbars = self.config_reader.build_busbars(self.system_pipes)
