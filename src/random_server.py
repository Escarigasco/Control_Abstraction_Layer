from name_translator import name_translator
import random
import syslab
import time
import sys


_ACTIVE = 1
_ACTIVE_VALVE = 0.1
_INACTIVE_VALVE = 0
_VALVE_STATUS = "valve_status"
_DESCRIPTION = "description"


class current_status_reader(object):
    def __init__(self, comms, system_pumps, system_sensors, system_valves):
        self.comms = comms
        self.system_valves = system_valves
        self.translator = name_translator()

    def run_random(self):
        min_operating = 0
        max_operating = 100
        for valve in self.system_valves.keys():
            random_gen = random.randint(min_operating, max_operating)
            if (random_gen > 10):
                self.system_valves[valve].set_status(_ACTIVE)
            else:
                self.system_valves[valve].set_status(_INACTIVE_VALVE)
        return True

    def run_online(self):

            valves_for_physical_layer = {}
            valves_for_logical_layer = {}

            for valve in self.system_valves:
                valves_for_physical_layer[self.translator.components(valve)] = valve
            valves_for_physical_layer[_DESCRIPTION] = _VALVE_STATUS

            valves_for_translation = self.comms.send(valves_for_physical_layer)

            for valve in valves_for_translation.keys():
                valves_for_logical_layer[self.translator.reverse_components(valve)] = valves_for_translation[valve]

            if (valves_for_logical_layer):
                for valve in valves_for_logical_layer.keys():
                    if isinstance(valves_for_logical_layer[valve], float):
                        if (valves_for_logical_layer[valve] >= _ACTIVE_VALVE):
                            self.system_valves[valve].set_status(_ACTIVE)
                        else:
                            self.system_valves[valve].set_status(_INACTIVE_VALVE)
                    else:
                        print("{0} is not answering please check the connection - it is now setted to off but it is a non responder ".format(valve))
                        self.system_valves[valve].set_status(_INACTIVE_VALVE)

                return True
            else:
                return False
