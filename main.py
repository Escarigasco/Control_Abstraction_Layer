
from switch_board_building import switch_board_building
from interface import interface
#  from IPython.core.debugger import Tracer
#  Tracer()()


BuildingID = "Building716"
Receiver = "First"


building716 = switch_board_building(BuildingID)

intf = interface(building716)

Bay_1 = intf.get_hydraulic_bay(intf.get_switch_board("Switch_Board_1"), "Bay_5")

# server = input_receiver()

# computational_unit = path_calculator()

# user_inputs =  Server.get_commands()

# classe = building716.interface(user_inputs)

# components_involved = computational_unit.get_path(classe, user_inputs)

# components_functions = computation_unit.get_functions(components_involved, classe, user_inputs)
