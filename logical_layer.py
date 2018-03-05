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


        Parameter = "E"
        Sensor = "Sensor_1E1"
        Setpoint = "5"
        Source = "Source_1HP1"

    def run(self, sensors, parameters, setpoints, sources):

        self.sensors_list = sensors
        self.parameters_list = parameters
        self.setpoints_list = setpoints
        self.sources_list = sources
        print(self.sensors_list.keys())
        print(self.sensors_list.values())

        building716 = switch_board_building(self.BuildingID)
        intf = interface(building716, self.SwitchID)
        objtk = object_tracker(intf)

        system_sensors = intf.get_system_sensors()
        system_pumps = intf.get_system_pumps()
        system_valves = intf.get_system_valves()
        system_pipes = intf.get_system_pipes()
        system_connected_devices = intf.get_connected_devices()
        system_bays = intf.get_hydraulic_bays()

        sensors_position = objtk.where_are_sensors(system_sensors)
        connected_device_position = objtk.where_are_connected_devices(system_connected_devices)

        # computational_unit = path_calculator() - it will define all the pipes entering the bays that
        # print(sensors_position.keys())
        # print(sensors_position.values())
        # print(connected_device_position.keys())
        # print(connected_device_position.values())

        # return networkx object

        # server = input_receiver()

        # user_inputs =  Server.get_commands()

        # classe = building716.interface(user_inputs)

        # components_involved = computational_unit.get_path(classe, user_inputs)

    # components_functions = computation_unit.get_functions(components_involved, classe, user_inputs)
