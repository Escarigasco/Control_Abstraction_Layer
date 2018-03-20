from object_tracker import object_tracker
from random_server import random_server
import networkx as nx
from networkx.algorithms import isomorphism
from matplotlib import pyplot as plt


class configuration_reader(object):

    def __init__(self, config_reader, online_builder):
        Graph = nx.DiGraph()
        self.config_reader = config_reader
        objtk = object_tracker(self.config_reader)
        # system_bays = self.config_reader.get_hydraulic_bays()
        system_pumps = self.config_reader.get_system_pumps()
        system_sensors = self.config_reader.get_system_sensors()
        system_valves = self.config_reader.get_system_valves()
        # self.system_connectors = self.config_reader.get_system_connectors()
        # self.system_lines = self.config_reader.get_system_lines()
        self.system_pipes = self.config_reader.get_system_pipes()
        # self.system_connected_devices = self.config_reader.get_connected_devices()
        # self.system_bays = self.config_reader.get_hydraulic_bays()
        system_busbars = self.config_reader.build_busbars(self.system_pipes)

        random_server(system_pumps, system_sensors, system_valves)

        for busbar in system_busbars.keys():
            busbar_ID = system_busbars[busbar].get_name()
            Graph.add_node(system_busbars[busbar])
            for valve in system_valves.keys():
                if (system_valves[valve].get_status()):
                    Graph.add_node(system_valves[valve])
                    valve_connection = system_valves[valve].get_connection()
                    if (valve_connection == busbar_ID):
                        if (system_valves[valve].get_flow_direction() == 'in'):
                            Graph.add_edges_from([(system_busbars[busbar], system_valves[valve])])
                                if (system_valves[valve].get_flow() == 'H'):
                                    # insert pump + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                else:
                                    # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility

                        else:
                            Graph.add_edges_from([(system_valves[valve], system_busbars[busbar])])

        nx.draw(Graph, with_labels=True)
        plt.show()

        #online_builder.run()
