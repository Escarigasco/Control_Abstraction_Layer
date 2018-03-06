from switch_board_building import switch_board_building
from interface import interface
from object_tracker import object_tracker

#  from IPython.core.debugger import Tracer
#  Tracer()()


class logical_layer(object):
    'Component that output the control object'
    def __init__(self, buildingID, SwitchID):

        self.BuildingID = "Building716"
        self.Receiver = "First"
        self.SwitchID = "Switch_Board_1"

        self.building716 = switch_board_building(self.BuildingID)
        self.intf = interface(self.building716, self.SwitchID)

        self.system_sensors = self.intf.get_system_sensors()
        self.system_pumps = self.intf.get_system_pumps()
        self.system_valves = self.intf.get_system_valves()
        self.system_connectors = self.intf.get_system_connectors()
        self.system_lines = self.intf.get_system_lines()
        self.system_pipes = self.intf.get_system_pipes()
        self.system_connected_devices = self.intf.get_connected_devices()
        self.system_bays = self.intf.get_hydraulic_bays()
        self.system_busbars = self.intf.build_busbars(self.system_pipes)
        self.objtk = object_tracker(self.intf)

    def run(self, sensors, parameters, setpoints, sources):

        self.sensors_list = sensors
        self.parameters_list = parameters
        self.setpoints_list = setpoints
        self.sources_list = sources

        sensors_position = self.objtk.where_are_sensors(self.system_sensors)
        connected_device_position = self.objtk.where_are_connected_devices(self.system_connected_devices)
        lines_valve_connection = self.objtk.line_to_which_valve(self.system_valves, self.system_lines)

        # computational_unit = path_calculator() - it will define all the pipes entering the bays that

        # return networkx object

        # server = input_receiver()

        # user_inputs =  Server.get_commands()

        # classe = building716.interface(user_inputs)

        # components_involved = computational_unit.get_path(classe, user_inputs)

        # components_functions = computation_unit.get_functions(components_involved, classe, user_inputs)
