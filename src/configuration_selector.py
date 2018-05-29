from communicator_physical_layer import communicator_physical_layer
from components_status import components_status
import re
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


class configuration_selector(object):
    def __init__(self, sensors, valves, pumps, connected_devices, busbars, interface, comms):
        self.intf = interface
        self.sensors = sensors
        self.valves = valves
        self.pumps = pumps
        self.comms = comms
        self.system_busbars = busbars
        self.connected_devices = connected_devices
        self.system_components = {**self.sensors, **self.valves, **self.pumps, **self.connected_devices, **self.system_busbars}
        self.c_status = components_status()

    def start_screening(self, actuable_configuration, busy_busbar):
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
            print(busbars)
            for bb in busbars:
                print(bb)
                print(occupied_busbars)
                print(bb in occupied_busbars)
                if (bb in occupied_busbars):
                    busy = True
            print(not busy)
            if not busy:
                available_components[name] = self.c_status.run(self.intf, configuration_components)
                scores[name] = sum([available_components[name][_S_SCORE], available_components[name][_V_SCORE], available_components[name][_P_SCORE]])

        for name in scores.keys():
            print(name)
            print(scores[name])
        selected_configuration = max(scores, key=scores.get)  # this is to find the key that has the smallest value
        print(selected_configuration)

        nodes = list(actuable_configuration[selected_configuration].nodes)
        configuration_nodes = {}
        busbars = []
        for node in nodes:
            configuration_nodes[node] = self.system_components[node]
        for node in configuration_nodes.keys():
            if (configuration_nodes[node].object_type == _BUSBARS):
                busbars.append(node)

        message_to_return = {_GRAPH: actuable_configuration[selected_configuration],
                             _AVAILABLE_COMPONENTS: available_components[selected_configuration],
                             _BUSBARS: busbars}

        print(message_to_return)
        return message_to_return
