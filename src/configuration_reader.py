from object_tracker import object_tracker
from random_server import random_server
import networkx as nx
from networkx.algorithms import isomorphism
from matplotlib import pyplot as plt


class configuration_reader(object):

    def __init__(self, interface, online_builder):
        Graph = nx.DiGraph()
        self.config_reader = interface
        self.objtk = object_tracker(self.config_reader)
        # system_bays = self.config_reader.get_hydraulic_bays()
        system_pumps = self.config_reader.get_system_pumps()
        system_sensors = self.config_reader.get_system_sensors()
        system_valves = self.config_reader.get_system_valves()
        system_connectors = self.config_reader.get_system_connectors()
        # self.system_lines = self.config_reader.get_system_lines()
        self.system_pipes = self.config_reader.get_system_pipes()
        system_connected_devices = self.config_reader.get_connected_devices()
        # self.system_bays = self.config_reader.get_hydraulic_bays()
        system_busbars = self.config_reader.build_busbars(self.system_pipes)

        sensors_position = self.objtk.where_are_devices(system_sensors)
        connected_device_position = self.objtk.where_are_devices(system_connected_devices)
        valves_position = self.objtk.where_are_devices(system_valves)
        pump_position = self.objtk.where_are_devices(system_pumps)

        random_server(system_pumps, system_sensors, system_valves)

        for busbar in system_busbars.keys():
            busbar_ID = system_busbars[busbar].get_name()
            Graph.add_node(system_busbars[busbar])
            for valve in system_valves.keys():
                bay = valves_position[valve]
                if (system_valves[valve].get_status()):
                    Graph.add_node(system_valves[valve])
                    valve_connection = system_valves[valve].get_connection()
                    if (valve_connection == busbar_ID):
                        if (system_valves[valve].get_flow_direction() == 'in'):
                            Graph.add_edges_from([(system_busbars[busbar], system_valves[valve])])
                            if (system_valves[valve].get_flow() == 'H'):
                                    pump = pump_position[bay][0]
                                    print(pump)
                                    if (pump.get_status()):
                                        Graph.add_edges_from([(system_valves[valve], pump)])
                                    else: # if the pump is disconnected
                                        #continue# if i want to make fail the loop insert pump + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                        pass # if i want hydraulic
                            # else:
                                    # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility

                        else:
                            Graph.add_edges_from([(system_valves[valve], system_busbars[busbar])])

        nx.draw(Graph, with_labels=True)
        plt.show()

        #online_builder.run()
