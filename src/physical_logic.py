import syslab
import syslab.core.datatypes.CompositeMeasurement as CM
import time
import sys

_BUILDING_NAME = "716-h1"
_MULTIPLIER = 1000000
_TURN_ME_ON = 1.0
_TURN_ME_OFF = 0.0
_VALVES = 'Valves_active'
_VALVES_TO_SHUT = 'Valves_to_shut'
_PUMP = "Pump"


class physical_logic(object):

    def __init__(self):
        self.valves_status = {
            "Bay_4L-Busbar_2R": 0.51, "Bay_4L-Busbar_1R": 0.11, "Bay_4H-Busbar_B": 0.11, "Bay_4H-Busbar_2F": 0.11, "Bay_4H-Busbar_1F": 0.91, "Bay_4L-Busbar_B": 0.11,
            "Bay_5L-Busbar_1R": 0.11, "Bay_5L-Busbar_2R": 0.11, "Bay_5H-Busbar_B": 0.11, "Bay_5H-Busbar_1F": 0.11, "Bay_5H-Busbar_2F": 0.11, "Bay_5L-Busbar_B": 0.11,
            "Bay_6L-Busbar_1R": 0.11, "Bay_6L-Busbar_2R": 0.11, "Bay_6H-Busbar_B": 0.11, "Bay_6H-Busbar_1F": 0.11, "Bay_6H-Busbar_2F": 0.11, "Bay_6L-Busbar_B": 0.11,
            "Bay_7H-Busbar_1F": 0.11, "Bay_7H-Busbar_2F": 0.11, "Bay_7L-Busbar_1R": 0.51, "Bay_7L-Busbar_2R": 0.11,
            "Bay_8H-Busbar_1F": 0.11, "Bay_8H-Busbar_2F": 0.11, "Bay_8L-Busbar_1R": 0.11, "Bay_8L-Busbar_2R": 0.11}
        self.pumps_status = {
            "Pump_Bay4": 0.0,
            "Pump_Bay5": 0.0,
            "Pump_Bay6": 0.0,
            "Pump_Bay7": 0.0,
            "Pump_Bay8": 0.0}

        #self.interface = syslab.HeatSwitchBoard(_BUILDING_NAME)

    def initialization(self, inputs):
        print("Initialization of the equipment")
        valves_status_checker = {}
        complete = False
        CompositMess_Shut = CM(_TURN_ME_OFF, time.time() * _MULTIPLIER)
        circulator_mode = "PUMP_MODE_CONSTANT_FLOW"
        opening_threshold = 0.05
        for pump in inputs[_PUMP]:
                    #self.interface.setPumpControlMode(pumps, circulator_mode)
                    print("mode set in pump ", pump)
                    #self.interface.setPumpSetpoint(circulator, CompositMess_Shut)
                    print("setpoint at 0 for pump ", pump)
        while not complete:
            for valve in inputs[_VALVES_TO_SHUT]:
                self.valves_status[valve] = 0.0
                print("setpoint at 0 for valve", valve)
                #self.interface.setValvePosition(valve, CompositMess_Shut)
            #time.sleep(10)
            for valve in inputs[_VALVES_TO_SHUT]:
                valves_status_checker[valve] = 0.0 #self.interface.getValvePosition(valve)
                if ((sum(opening for opening in valves_status_checker.values()) <= opening_threshold)):
                    complete = True
        return [complete, self.valves_status]


    def get_pumps_status(self, pumps_for_physical_layer):
        print("I am reading pumps")
        pumps_for_logical_layer = {}
        for pump in pumps_for_physical_layer.keys():
            head = self.interface.getPumpHead(pump)
            pumps_for_logical_layer[pump] = head.value
        return pumps_for_logical_layer

    def get_pumps_simulated_status(self, pumps_for_physical_layer):
        print("I am reading simulated pumps")
        pumps_for_logical_layer = {}
        for pump in pumps_for_physical_layer.keys():
            pumps_for_logical_layer[pump] = self.pumps_status[pump]
        return pumps_for_logical_layer

    def get_valves_status(self, valves_for_physical_layer):
        print("I am reading circuit")
        valves_for_logical_layer = {}
        for valve in valves_for_physical_layer.keys():
            opening = self.interface.getValvePosition(valve)
            valves_for_logical_layer[valve] = opening.value
        return valves_for_logical_layer

    def get_valves_simulated_status(self, valves_for_physical_layer, queue=None):
        #print("I am reading simulated circuit")
        valves_for_logical_layer = {}
        for valve in valves_for_physical_layer.keys():
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
        #time.sleep(1)
        valves = inputs[_VALVES]
        valves_to_shut = inputs[_VALVES_TO_SHUT]
        valves_status = {}
        valves_to_shut_status = {}
        opening_threshold = len(valves) * 0.9
        closing_threshold = len(valves_status) * 0.1
        complete = False
        for valve in valves:
            valves_status[valve] = 1.0
            self.valves_status[valve] = 1.0
        for valve in valves_to_shut:
            valves_to_shut_status[valve] = 1.0
            self.valves_status[valve] = 0.0
        # print(sum(opening for opening in valves_status.values()))
        if ((sum(opening for opening in valves_status.values()) >= opening_threshold)
           & (sum(opening for opening in valves_to_shut_status.values()) <= closing_threshold)):
                complete = True
        print(self.valves_status)
        return [complete, self.valves_status]

    def shut_pumps(self, pumps):
        pumps = pumps[_PUMP]
        CompositMess_Shut = CM(_TURN_ME_OFF, time.time() * _MULTIPLIER)
        circulator_mode = "PUMP_MODE_CONSTANT_FLOW"
        for pump in pumps:
                #self.interface.setPumpControlMode(pumps, circulator_mode)
                print("mode set in pump ", pump)
                #self.interface.setPumpSetpoint(circulator, CompositMess_Shut)
                print("setpoint at 0 for pump ", pump)
        return ("All the pumps are set to constant flow and setpoint 0")

    def update_valves(self, valves):
        self.valves_status = valves
