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
        self.system_lines = self.config_reader.get_system_lines()
        self.system_pipes = self.config_reader.get_system_pipes()
        system_connected_devices = self.config_reader.get_connected_devices()
        # self.system_bays = self.config_reader.get_hydraulic_bays()
        system_busbars = self.config_reader.build_busbars(self.system_pipes)

        sensors_position = self.objtk.where_are_devices(system_sensors)
        connected_device_position = self.objtk.where_are_devices(system_connected_devices)

        valves_position = self.objtk.where_are_devices(system_valves)
        pump_position = self.objtk.where_are_devices(system_pumps)
        line_position = self.objtk.where_are_devices(self.system_lines)
        print(line_position)
        colf_flow = 'C'
        hot_flow = 'H'
        direction_out = 'out'
        direction_in = 'in'
        x_bb = 0
        y = 0
        x_v = 0
        x = 0
        x_dev = -700
        random_server(system_pumps, system_sensors, system_valves)

        for busbar in system_busbars.keys():

            y = 0
            z = 0
            x_bb += 200
            x_v = 0
            busbar_ID = system_busbars[busbar].get_name()
            Graph.add_node(system_busbars[busbar], pos=(x_bb, y))
            for valve in system_valves.keys():
                y = 0.5
                x_v += 100
                bay = valves_position[valve]
                if (system_valves[valve].get_status()):
                    Graph.add_node(system_valves[valve], pos=(x_v, y))
                    valve_connection = system_valves[valve].get_connection()
                    if (valve_connection == busbar_ID):
                        if (system_valves[valve].get_flow_direction() == direction_in):

                            Graph.add_edges_from([(system_busbars[busbar], system_valves[valve])])
                            if (system_valves[valve].get_flow() == hot_flow):

                                    lines = line_position[bay]
                                    for line in lines:
                                        if (line.flow_type == hot_flow):
                                            x_dev += 100
                                            sensors = line.line_sensors
                                            iterate_sensor = system_valves[valve]
                                            for sensor in sensors.keys():
                                                # if (sensors[sensor].get_status()):
                                                    y += 0.5

                                                    Graph.add_node(sensors[sensor], pos=(x_dev, y))
                                                    Graph.add_edges_from([(iterate_sensor, sensors[sensor])])
                                                    iterate_sensor = sensors[sensor]
                                                # else:
                                                    # pass
                                            y += 0.5
                                            pump_id = pump_position[bay][0].get_name()

                                            pump = line.pumps[pump_id]
                                            # if (pump.get_status()):
                                            Graph.add_node(pump, pos=(x_dev, y))
                                            Graph.add_edges_from([(iterate_sensor, pump)])
                                            y += 0.5
                                            device = connected_device_position[bay][0]
                                            Graph.add_node(device, pos=(x_dev, y))
                                            Graph.add_edges_from([(pump, device)])

                                            # else:  # if the pump is disconnected
                                            # continue  # if i want to make fail the loop because if you can't poll it could be anything and you can't control with unknown variables around + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                        elif (line.flow_type == colf_flow):
                                            pass

                            elif (system_valves[valve].get_flow() == colf_flow):
                                lines = line_position[bay]
                                for line in lines:
                                    if (line.flow_type == colf_flow):
                                        x_dev += 100
                                        sensors = line.line_sensors
                                        iterate_sensor = system_valves[valve]
                                        for sensor in sensors.keys():
                                            # if (sensors[sensor].get_status()):
                                                y += 0.5
                                                Graph.add_node(sensors[sensor], pos=(x_dev, y))
                                                Graph.add_edges_from([(iterate_sensor, sensors[sensor])])
                                                iterate_sensor = sensors[sensor]
                                       

                                            # else:
                                                # pass

                                        y += 0.5
                                        device = connected_device_position[bay][0]
                                        Graph.add_node(device, pos=(x_dev, y))
                                        Graph.add_edges_from([(iterate_sensor, device)])

                                    # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility

                        elif (system_valves[valve].get_flow_direction() == direction_out):

                            Graph.add_edges_from([(system_valves[valve], system_busbars[busbar])])
                            if (system_valves[valve].get_flow() == hot_flow):
                                    lines = line_position[bay]
                                    for line in lines:
                                        if (line.flow_type == hot_flow):
                                            x_dev += 100
                                            sensors = line.line_sensors
                                            iterate_sensor = system_valves[valve]
                                            for sensor in sensors.keys():
                                                # if (sensors[sensor].get_status()):
                                                    y += 0.5
                                                    Graph.add_node(sensors[sensor], pos=(x_dev, y))
                                                    Graph.add_edges_from([(sensors[sensor], iterate_sensor)])
                                                    iterate_sensor = sensors[sensor]
                                                # else:
                                                    # pass
                                            y += 0.5
                                            pump = pump_position[bay][0]
                                            # if (pump.get_status()):
                                            Graph.add_node(pump, pos=(x_dev, y))
                                            Graph.add_edges_from([(pump, iterate_sensor)])
                                            y += 0.5
                                            device = connected_device_position[bay][0]
                                            Graph.add_node(device, pos=(x_dev, y))
                                            Graph.add_edges_from([(device, pump)])

                                            # else: # if the pump is disconnected
                                            # continue # if i want to make fail the loop because if you can't poll it could be anything and you can't control with unknown variables around + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                        elif (line.flow_type == colf_flow):
                                            pass

                            elif (system_valves[valve].get_flow() == colf_flow):
                                lines = line_position[bay]
                                for line in lines:
                                    if (line.flow_type == colf_flow):
                                        x_dev += 100
                                        sensors = line.line_sensors
                                        iterate_sensor = system_valves[valve]
                                        for sensor in sensors.keys():
                                            # if (sensors[sensor].get_status()):
                                                y += 0.5
                                                Graph.add_node(sensors[sensor], pos=(x_dev, y))
                                                Graph.add_edges_from([(sensors[sensor], iterate_sensor)])
                                                iterate_sensor = sensors[sensor]
                                            # else:
                                                # pass
                                        y += 0.5
                                        device = connected_device_position[bay][0]
                                        Graph.add_node(device, pos=(x_dev, y))
                                        Graph.add_edges_from([(device, iterate_sensor)])

                                    # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility

        '''nx.draw(Graph, with_labels=True)
        plt.show()'''

        '''pos = nx.spring_layout(Graph, iterations=10)
        nx.draw(Graph, pos, font_size=8, with_labels=True, node_size=40)
        plt.show()'''

        pos = nx.get_node_attributes(Graph, 'pos')
        nx.draw(Graph, pos, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
        plt.show()

        # online_builder.run()
