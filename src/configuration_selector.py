from communicator_physical_layer import communicator_physical_layer
from components_status import components_status
import sys

_S_NAME = 'Sensor'
_P_NAME = 'Pump'
_V_NAME = 'Valve'
_S_SCORE = "Sensors_score"
_P_SCORE = "Pumps_score"
_V_SCORE = "Valves_score"
_AVAILABLE_COMPONENTS = "available_components"
_GRAPH = "graph"
_BUSBARS = "busbar"
_HOT_BUSBAR = "hot_busbar"
_COLD_BUSBAR = "cold_busbar"
_VALVES_TO_SHUT = 'Valves_to_shut'
_VALVES = 'Valves_active'


class configuration_selector(object):
    def __init__(self, sensors, valves, pumps, connected_devices, busbars, interface, comms, translator):
        self.intf = interface
        self.sensors = sensors
        self.valves = valves
        self.pumps = pumps
        #self.comms = comms
        self.system_busbars = busbars
        self.connected_devices = connected_devices
        self.system_components = {**self.sensors, **self.valves, **self.pumps, **self.connected_devices, **self.system_busbars}
        self.c_status = components_status(comms, translator)

    def start_screening(self, actuable_configuration, busy_busbar, all_possible_valves):
        occupied_busbars = []
        available_components = {}
        scores = {}
        message_to_return = {} # this will be both the actual nx.graph and the available components

        for list_busbar in busy_busbar.values():
            occupied_busbars += list_busbar

        for name in actuable_configuration.keys():
            busy = False
            configuration_nodes = {}
            configuration_components = {}
            sensors = []
            pumps = []
            valves = []
            busbars = []
            nodes = list(actuable_configuration[name].nodes)
            for node in nodes:
                configuration_nodes[node] = self.system_components[node]
            for node in configuration_nodes.keys():
                if (configuration_nodes[node].object_type == _S_NAME):
                    sensors.append(configuration_nodes[node])
                elif (configuration_nodes[node].object_type == _P_NAME):
                    pumps.append(configuration_nodes[node])
                elif (configuration_nodes[node].object_type == _V_NAME):
                    valves.append(configuration_nodes[node])
                elif (configuration_nodes[node].object_type == _BUSBARS):
                    busbars.append(node)

            configuration_components = {_S_NAME: sensors, _P_NAME: pumps, _V_NAME: valves}
            #print(busbars)
            for bb in busbars:
                #print(bb)
                #print(occupied_busbars)
                if (bb in occupied_busbars):
                    busy = True
            if not busy:
                available_components[name] = self.c_status.run(configuration_components)
                scores[name] = sum([available_components[name][_S_SCORE],
                                    available_components[name][_V_SCORE],
                                    available_components[name][_P_SCORE]])

        #for name in scores.keys():
            #print(name)
            #print(scores[name])
        if scores:
            selected_configuration = max(scores, key=scores.get)  # this is to find the key that has the smallest value
            print("The winner is.... ", selected_configuration)
        else:
            print("You are already using all the busbars.. don't be greedy")
            return None

        nodes = list(actuable_configuration[selected_configuration].nodes)
        configuration_nodes = {}
        busbars = []
        for node in nodes:
            configuration_nodes[node] = self.system_components[node]
        for node in configuration_nodes.keys():
            if (configuration_nodes[node].object_type == _BUSBARS):
                busbars.append(node)

        '''this routine is to cloes the valves in the interested bays that are not part of the selected circuit'''
        available_components[selected_configuration][_VALVES_TO_SHUT] = [valve for valve in all_possible_valves
                                                                         if valve not in available_components[selected_configuration][_VALVES]]

        '''this routine is to close the valves in all the other bays that are connected to the selected busbars'''
        valves_other_bays_to_close = []
        for valve in self.valves.values():
            if ((valve.connection in busbars) & (valve not in available_components[selected_configuration][_VALVES])):
                valves_other_bays_to_close.append(valve)

        available_components[selected_configuration][_VALVES_TO_SHUT] = available_components[selected_configuration][_VALVES_TO_SHUT] + valves_other_bays_to_close
        print(available_components[selected_configuration][_VALVES_TO_SHUT])
        print(available_components[selected_configuration][_VALVES])

        message_to_return = {_GRAPH: actuable_configuration[selected_configuration],
                             _AVAILABLE_COMPONENTS: available_components[selected_configuration],
                             _BUSBARS: busbars}
    
        return message_to_return
