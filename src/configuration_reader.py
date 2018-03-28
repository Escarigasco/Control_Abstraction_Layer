from object_tracker import object_tracker
from random_server import random_server
import networkx as nx
from matplotlib import pyplot as plt
_COLD_FLOW = 'C'
_HOT_FLOW = 'H'
_DIRECTION_IN = 'in'
_DIRECTION_OUT = 'out'
_FIRST_OF_THE_CLASS = 0  # a constant is use to indicate the first element of a list - in reality for every case it could be a random number within the list indexes range, used 0 not to call a random number generator


class configuration_reader(object):

    def __init__(self, interface):

        self.config_reader = interface
        self.objtk = object_tracker(self.config_reader)
        # system_bays = self.config_reader.get_hydraulic_bays()

    def run(self):
        Graph = nx.DiGraph()
        system_pumps = self.config_reader.get_system_pumps()
        system_sensors = self.config_reader.get_system_sensors()
        system_valves = self.config_reader.get_system_valves()
        self.system_lines = self.config_reader.get_system_lines()
        self.system_pipes = self.config_reader.get_system_pipes()
        system_connected_devices = self.config_reader.get_connected_devices()
        # self.system_bays = self.config_reader.get_hydraulic_bays()
        system_busbars = self.config_reader.build_busbars(self.system_pipes)
        connected_device_position = self.objtk.where_are_devices(system_connected_devices)

        valves_position = self.objtk.where_are_devices(system_valves)
        pump_position = self.objtk.where_are_devices(system_pumps)
        line_position = self.objtk.where_are_devices(self.system_lines)
        x_bb = 0
        y = 0
        x_v = 0
        x_dev = -900
        random_server(system_pumps, system_sensors, system_valves)

        for busbar in system_busbars.keys():
            y = 0
            x_bb += 800
            x_v = 0
            busbar_ID = system_busbars[busbar].get_name()
            Graph.add_node(system_busbars[busbar].get_name(), pos=(x_bb, y))
            for valve in system_valves.keys():
                y = 0.5
                x_v += 200
                bay = valves_position[valve]
                if (system_valves[valve].get_status()):
                    print("{0} open".format(system_valves[valve]))
                    Graph.add_node(system_valves[valve].get_name(), pos=(x_v, y))
                    valve_connection = system_valves[valve].get_connection()
                    if (valve_connection == busbar_ID):
                        if (system_valves[valve].get_flow_direction() == _DIRECTION_IN):

                            Graph.add_edges_from([(system_busbars[busbar].get_name(), system_valves[valve].get_name())])
                            if (system_valves[valve].get_flow() == _HOT_FLOW):

                                    lines = line_position[bay]
                                    for line in lines:
                                        if (line.flow_type == _HOT_FLOW):
                                            x_dev += 250

                                            line_devices = {**line.line_sensors, **line.pumps}.values()
                                            sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)
                                            iterate_sensor = system_valves[valve]
                                            for line_device in sorted_devices:
                                                # if (sensors[sensor].get_status()):
                                                    y += 0.5

                                                    Graph.add_node(line_device.get_name(), pos=(x_dev, y))
                                                    Graph.add_edges_from([(iterate_sensor.get_name(), line_device.get_name())])
                                                    iterate_sensor = line_device
                                                # else:
                                                    # pass

                                            y += 0.5
                                            device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                            Graph.add_node(device.get_name(), pos=(x_dev, y))
                                            Graph.add_edges_from([(iterate_sensor.get_name(), device.get_name())])
                                            # else:  # if the pump is disconnected
                                            # continue  # if i want to make fail the loop because if you can't poll it could be anything and you can't control with unknown variables around + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                        elif (line.flow_type == _COLD_FLOW):
                                            pass

                            elif (system_valves[valve].get_flow() == _COLD_FLOW):
                                lines = line_position[bay]
                                for line in lines:
                                    if (line.flow_type == _COLD_FLOW):
                                        x_dev += 250
                                        line_devices = {**line.line_sensors, **line.pumps}.values()
                                        sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)
                                        iterate_sensor = system_valves[valve]
                                        for line_device in sorted_devices:
                                            # if (sensors[sensor].get_status()):
                                                y += 0.5

                                                Graph.add_node(line_device.get_name(), pos=(x_dev, y))
                                                Graph.add_edges_from([(iterate_sensor.get_name(), line_device.get_name())])
                                                iterate_sensor = line_device
                                            # else:
                                                # pass

                                        y += 0.5
                                        device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                        Graph.add_node(device.get_name(), pos=(x_dev, y))
                                        Graph.add_edges_from([(iterate_sensor.get_name(), device.get_name())])

                                    # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility

                        elif (system_valves[valve].get_flow_direction() == _DIRECTION_OUT):

                            Graph.add_edges_from([(system_valves[valve].get_name(), system_busbars[busbar].get_name())])
                            if (system_valves[valve].get_flow() == _HOT_FLOW):
                                    lines = line_position[bay]
                                    for line in lines:
                                        if (line.flow_type == _HOT_FLOW):
                                            x_dev += 250
                                            line_devices = {**line.line_sensors, **line.pumps}.values()
                                            sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)
                                            iterate_sensor = system_valves[valve]
                                            for line_device in sorted_devices:
                                                # if (sensors[sensor].get_status()):
                                                    y += 0.5

                                                    Graph.add_node(line_device.get_name(), pos=(x_dev, y))
                                                    Graph.add_edges_from([(line_device.get_name(), iterate_sensor.get_name())])
                                                    iterate_sensor = line_device
                                                # else:
                                                    # pass

                                            y += 0.5
                                            device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                            Graph.add_node(device.get_name(), pos=(x_dev, y))
                                            Graph.add_edges_from([(device.get_name(), iterate_sensor.get_name())])

                                            # else: # if the pump is disconnected
                                            # continue # if i want to make fail the loop because if you can't poll it could be anything and you can't control with unknown variables around + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                        elif (line.flow_type == _COLD_FLOW):
                                            pass

                            elif (system_valves[valve].get_flow() == _COLD_FLOW):
                                lines = line_position[bay]
                                for line in lines:
                                    if (line.flow_type == _COLD_FLOW):
                                        x_dev += 250
                                        line_devices = {**line.line_sensors, **line.pumps}.values()
                                        sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)
                                        iterate_sensor = system_valves[valve]
                                        for line_device in sorted_devices:
                                            # if (sensors[sensor].get_status()):
                                                y += 0.5

                                                Graph.add_node(line_device.get_name(), pos=(x_dev, y))
                                                Graph.add_edges_from([(line_device.get_name(), iterate_sensor.get_name())])
                                                iterate_sensor = line_device
                                            # else:
                                                # pass

                                        y += 0.5
                                        device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                        Graph.add_node(device.get_name(), pos=(x_dev, y))
                                        Graph.add_edges_from([(device.get_name(), iterate_sensor.get_name())])

                                    # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                else:
                    print("{0} close".format(system_valves[valve]))
                    continue

        pos = nx.get_node_attributes(Graph, 'pos')
        plt.figure(1)
        nx.draw(Graph, pos, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
        # plt.show()
        return Graph
