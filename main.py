
from switch_board_building import switch_board_building
from interface import interface
from object_tracker import object_tracker
#  from IPython.core.debugger import Tracer
#  Tracer()()


BuildingID = "Building716"
Receiver = "First"
SwitchID = "Switch_Board_1"
Parameter = "E"
Sensor = "Sensor_1E1"
Setpoint = "5"
Source = "Source_1HP1"

building716 = switch_board_building(BuildingID)

intf = interface(building716, SwitchID)
objtk = object_tracker(intf)
system_sensors = intf.get_system_sensors()
system_pumps = intf.get_system_pumps()
system_valves = intf.get_system_valves()
system_pipes = intf.get_system_pipes()
sensors_position = objtk.where_are_sensors(system_sensors)

print(sensors_position.keys())
print(sensors_position.values())


# server = input_receiver()

# computational_unit = path_calculator()

# user_inputs =  Server.get_commands()

# classe = building716.interface(user_inputs)

# components_involved = computational_unit.get_path(classe, user_inputs)

# components_functions = computation_unit.get_functions(components_involved, classe, user_inputs)
