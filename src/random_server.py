#from communicator_physical_layer import communicator_physical_layer
import random
import syslab
import time
import sys
_BUILDING_NAME = "716-h1"
_ACTIVE = 1
_ACTIVE_VALVE = 0.1
_INACTIVE = 0


class current_status_reader(object):

    def run_random(self, pumps, sensors, valves):
        min_operating = 0
        max_operating = 100
        for valve in valves.keys():
            random_gen = random.randint(min_operating, max_operating)
            if (random_gen > 10):
                valves[valve].set_status(_ACTIVE)
            else:
                valves[valve].set_status(_INACTIVE)

    def run_online(self, pumps, sensors, valves):
            interface = syslab.HeatSwitchBoard(_BUILDING_NAME)
            valves_for_physical_layer = {}

            valves_name_translator = {
                'Valve_2C4': "Bay_4L-Busbar_2R", 'Valve_1C4': "Bay_4L-Busbar_1R", 'Valve_1B4': "Bay_4H-Busbar_B", 'Valve_2H4': "Bay_4H-Busbar_2F", 'Valve_1H4': "Bay_4H-Busbar_1F", 'Valve_2B4': "Bay_4L-Busbar_B",
                'Valve_2C5': "Bay_5L-Busbar_1R", 'Valve_1C5': "Bay_5L-Busbar_2R", 'Valve_1B5': "Bay_5H-Busbar_B", 'Valve_2H5': "Bay_5H-Busbar_1F", 'Valve_1H5': "Bay_5H-Busbar_2F", 'Valve_2B5': "Bay_5L-Busbar_B",
                'Valve_2C6': "Bay_6L-Busbar_1R", 'Valve_1C6': "Bay_6L-Busbar_2R", 'Valve_1B6': "Bay_6H-Busbar_B", 'Valve_2H6': "Bay_6H-Busbar_1F", 'Valve_1H6': "Bay_6H-Busbar_2F", 'Valve_2B6': "Bay_6L-Busbar_B",
                'Valve_2H7': "Bay_7H-Busbar_1F", 'Valve_1H7': "Bay_7H-Busbar_2F", 'Valve_2C7': "Bay_7L-Busbar_1R", 'Valve_1C7': "Bay_7L-Busbar_2R",
                'Valve_2H8': "Bay_8H-Busbar_1F", 'Valve_1H8': "Bay_8H-Busbar_2F", 'Valve_2C8': "Bay_8L-Busbar_1R", 'Valve_1C8': "Bay_8L-Busbar_2R"}

            for valve in valves.keys():
                #time.sleep(0.1)
                opening = interface.getValvePosition(valves_name_translator[valve])
                valves_for_physical_layer[valves_name_translator[valve]] = _INACTIVE
                #print(valve)
                #print(opening.value)
                try:
                    if (opening.value > _ACTIVE_VALVE):
                        valves[valve].set_status(_ACTIVE)
                    else:
                        valves[valve].set_status(_INACTIVE)
                except Exception:
                    valves[valve].set_status(_INACTIVE)
