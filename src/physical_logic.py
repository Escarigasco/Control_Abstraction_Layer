import syslab
import syslab.core.datatypes.CompositeMeasurement as CM
import time

_BUILDING_NAME = "716-h1"
_MULTIPLIER = 1000000
_TURN_ME_ON = 1
_TURN_ME_OFF = 0
_VALVES = 'Valves_active'
_VALVES_TO_SHUT = 'Valves_to_shut'


class physical_logic(object):

    def __init__(self):
        self.valves_status = {
            "Bay_4L-Busbar_2R": 0.11, "Bay_4L-Busbar_1R": 0.11, "Bay_4H-Busbar_B": 0.11, "Bay_4H-Busbar_2F": 0.11, "Bay_4H-Busbar_1F": 0.11, "Bay_4L-Busbar_B": 0.11,
            "Bay_5L-Busbar_1R": 0.11, "Bay_5L-Busbar_2R": 0.11, "Bay_5H-Busbar_B": 0.11, "Bay_5H-Busbar_1F": 0.11, "Bay_5H-Busbar_2F": 0.11, "Bay_5L-Busbar_B": 0.11,
            "Bay_6L-Busbar_1R": 0.11, "Bay_6L-Busbar_2R": 0.11, "Bay_6H-Busbar_B": 0.11, "Bay_6H-Busbar_1F": 0.11, "Bay_6H-Busbar_2F": 0.11, "Bay_6L-Busbar_B": 0.11,
            "Bay_7H-Busbar_1F": 0.11, "Bay_7H-Busbar_2F": 0.11, "Bay_7L-Busbar_1R": 0.11, "Bay_7L-Busbar_2R": 0.11,
            "Bay_8H-Busbar_1F": 0.11, "Bay_8H-Busbar_2F": 0.11, "Bay_8L-Busbar_1R": 0.11, "Bay_8L-Busbar_2R": 0.11}

        self.interface = syslab.HeatSwitchBoard(_BUILDING_NAME)

    def get_valves_status(self, valves_for_physical_layer):
        valves_for_logical_layer = {}
        for valve in valves_for_physical_layer.keys():
            opening = self.interface.getValvePosition(valve)
            #print(valve, opening.value)
            valves_for_logical_layer[valve] = opening.value
        return valves_for_logical_layer

    def get_valves_simulated_status(self, valves_for_physical_layer):
        print("I am reading simulated circuit")
        time.sleep(1)
        min_operating = 0
        max_operating = 1
        valves_for_logical_layer = {}
        for valve in valves_for_physical_layer.keys():
            #valves_for_logical_layer[valve] = random.uniform(min_operating, max_operating)
            valves_for_logical_layer[valve] = self.valves_status[valve]
        return valves_for_logical_layer

    def set_hydraulic_circuit(self, inputs):
        valves = inputs[_VALVES]
        valves_to_shut = inputs[_VALVES_TO_SHUT]
        valves_status = {}
        valves_to_shut_status = {}
        opening_threshold = len(valves) * 0.9
        closing_threshold = len(valves_status) * 0.1
        CompositMess_Shut = CM(_TURN_ME_OFF, time.time() * _MULTIPLIER)
        CompositMess = CM(_TURN_ME_ON, time.time() * _MULTIPLIER)
        complete = False
        for valve in valves_to_shut:
            self.interface.setValvePosition(valve, CompositMess_Shut)
        for valve in valves:
            self.interface.setValvePosition(valve, CompositMess)
        while not complete:
            for valve in valves:
                valves_status[valve] = self.interface.getValvePosition(valve).value
                time.sleep(0.2)
            for valve in valves_to_shut:
                valves_to_shut_status[valve] = self.interface.getValvePosition(valve).value
                time.sleep(0.2)
            if ((sum(opening for opening in valves_status.values()) >= opening_threshold)
               & (sum(opening for opening in valves_to_shut_status.values()) <= closing_threshold)):
                complete = True
        return complete

    def set_hydraulic_simulated_circuit(self, inputs):
        print("I am setting simulated circuit")
        time.sleep(1)
        valves = inputs[_VALVES]
        valves_to_shut = inputs[_VALVES_TO_SHUT]
        valves_status = {}
        valves_to_shut_status = {}
        opening_threshold = len(valves) * 0.9
        closing_threshold = len(valves_status) * 0.1
        complete = False
        for valve in valves:
            valves_status[valve] = 1
            self.valves_status[valve] = 1
        for valve in valves_to_shut:
            valves_to_shut_status[valve] = 1
            self.valves_status[valve] = 0
        # print(sum(opening for opening in valves_status.values()))
        if ((sum(opening for opening in valves_status.values()) >= opening_threshold)
           & (sum(opening for opening in valves_to_shut_status.values()) <= closing_threshold)):
                complete = True
        print(self.valves_status)
        return complete
