from switch_board_building import switch_board_building
from interface import interface
from object_tracker import object_tracker
# from path_builder import path_builder as pb
# from durable_rules import dr_path_builder as pb
from test_rules import trigger
from rule_engine import rule_engine
#  from IPython.core.debugger import Tracer
#  Tracer()()


class logical_layer(object):
    'Component that output the control object'
    def __init__(self, buildingID, SwitchID):
        self.buildingID = buildingID
        self.SwitchID = SwitchID

        self.building_config = switch_board_building(self.buildingID)
        self.intf = interface(self.building_config, self.SwitchID)

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
        # self.my_path_builder = pb(self.system_valves, self.system_sensors)

    def run(self, sensors, parameters, setpoints, sources, controlled_device, control_strategy):

        self.used_sensors = sensors
        self.parameters = parameters
        self.setpoints = setpoints
        self.used_sources = sources
        self.controlled_device = controlled_device
        self.control_strategy = control_strategy
        system_input = {"sensor": self.used_sensors, "parameter": self.parameters,
                        "setpoint": self.setpoints, "sources": self.used_sources,
                        "control_strategy": self.control_strategy, "controlled_device": self.controlled_device}

        sensors_position = self.objtk.where_are_sensors(self.system_sensors)
        connected_device_position = self.objtk.where_are_connected_devices(self.system_connected_devices)
        lines_valve_connection = self.objtk.line_to_which_valve(self.system_valves, self.system_lines)
        print(lines_valve_connection)
        # self.my_path_builder = trigger(self.system_sensors, self.system_connected_devices, self.input)
        test = rule_engine(self.system_sensors, self.system_pumps, self.system_valves, self.system_connected_devices, self.system_bays, self.system_busbars, system_input, sensors_position, lines_valve_connection)


if __name__ == "__main__":
    test = logical_layer("Building716", "Switch_Board_1")
    sensors = "Sensor_1E8"
    parameters = "Energy"
    setpoints = 50
    sources = "Source_1HP5"
    controlled_device = "Pump_1H5"
    control_strategy = "flow"
    test.run(sensors, parameters, setpoints, sources, controlled_device, control_strategy)
