#  Class to read the online configuration - the random server will be replaced with a status reader.
#  the algorithm is of the type - for each bus bar, for each valve connected to the bus bar, if the flow entering the valve goes in/out to the connected device, if this flow is cold/hot,
#  then you know which connector line -> add all devices of the line -> add the connected device of the bay the valve in exam is connected
# if a valve is off the algo goes to the next one leaving one branch open

from object_tracker import object_tracker
from random_server import random_server
from random_server import current_status_reader
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
        system_lines = self.config_reader.get_system_lines()
        system_pipes = self.config_reader.get_system_pipes()
        system_connected_devices = self.config_reader.get_connected_devices()
        # self.system_bays = self.config_reader.get_hydraulic_bays()
        system_busbars = self.config_reader.build_busbars(system_pipes)
        connected_device_position = self.objtk.where_are_devices(system_connected_devices)

        valves_position = self.objtk.where_are_devices(system_valves)
        line_position = self.objtk.where_are_devices(system_lines)

        # random_server(system_pumps, system_sensors, system_valves)
        current_status_reader(system_pumps, system_sensors, system_valves)

        for busbar in system_busbars.keys():

            busbar_ID = system_busbars[busbar].get_name()
            Graph.add_node(system_busbars[busbar].get_name())
            for valve in system_valves.keys():

                bay = valves_position[valve]
                if (system_valves[valve].get_status()):
                    print("{0} open".format(system_valves[valve]))
                    Graph.add_node(system_valves[valve].get_name())
                    valve_connection = system_valves[valve].get_connection()
                    if (valve_connection == busbar_ID):
                        if (system_valves[valve].get_flow_direction() == _DIRECTION_IN):

                            Graph.add_edges_from([(system_busbars[busbar].get_name(), system_valves[valve].get_name())])
                            if (system_valves[valve].get_flow() == _HOT_FLOW):

                                    lines = line_position[bay]
                                    for line in lines:
                                        if (line.flow_type == _HOT_FLOW):

                                            line_devices = {**line.line_sensors, **line.pumps}.values()
                                            sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)  # this is to respect the imposed order
                                            iterate_sensor = system_valves[valve]
                                            for line_device in sorted_devices:
                                                # if (sensors[sensor].get_status()):

                                                    Graph.add_node(line_device.get_name())
                                                    Graph.add_edges_from([(iterate_sensor.get_name(), line_device.get_name())])
                                                    iterate_sensor = line_device
                                                # else:
                                                    # pass

                                            device = connected_device_position[bay][_FIRST_OF_THE_CLASS]

                                            Graph.add_node(device.get_name())
                                            Graph.add_edges_from([(iterate_sensor.get_name(), device.get_name())])
                                            # else:  # if the pump is disconnected
                                            # continue  # if i want to make fail the loop because if you can't poll it could be anything and you can't control with unknown variables around + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                        elif (line.flow_type == _COLD_FLOW):
                                            pass

                            elif (system_valves[valve].get_flow() == _COLD_FLOW):
                                lines = line_position[bay]
                                for line in lines:
                                    if (line.flow_type == _COLD_FLOW):

                                        line_devices = {**line.line_sensors, **line.pumps}.values()
                                        sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)  # this is to respect the imposed order
                                        iterate_sensor = system_valves[valve]
                                        for line_device in sorted_devices:
                                            # if (sensors[sensor].get_status()):

                                                Graph.add_node(line_device.get_name())
                                                Graph.add_edges_from([(iterate_sensor.get_name(), line_device.get_name())])
                                                iterate_sensor = line_device
                                            # else:
                                                # pass

                                        device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                        # Graph.add_node(device.get_name(), pos=(x_dev, y))
                                        Graph.add_node(device.get_name())
                                        Graph.add_edges_from([(iterate_sensor.get_name(), device.get_name())])

                                    #elif (line.flow_type == _HOT_FLOW):
                                        #pass
                                        # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility

                        elif (system_valves[valve].get_flow_direction() == _DIRECTION_OUT):

                            Graph.add_edges_from([(system_valves[valve].get_name(), system_busbars[busbar].get_name())])
                            if (system_valves[valve].get_flow() == _HOT_FLOW):
                                    lines = line_position[bay]
                                    for line in lines:
                                        if (line.flow_type == _HOT_FLOW):

                                            line_devices = {**line.line_sensors, **line.pumps}.values()
                                            sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)  # this is to respect the imposed order
                                            iterate_sensor = system_valves[valve]
                                            for line_device in sorted_devices:
                                                # if (sensors[sensor].get_status()):

                                                    Graph.add_node(line_device.get_name())
                                                    Graph.add_edges_from([(line_device.get_name(), iterate_sensor.get_name())])
                                                    iterate_sensor = line_device
                                                # else:
                                                    # pass

                                            device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                            # Graph.add_node(device.get_name(), pos=(x_dev, y))
                                            Graph.add_node(device.get_name())
                                            Graph.add_edges_from([(device.get_name(), iterate_sensor.get_name())])

                                            # else: # if the pump is disconnected
                                            # continue # if i want to make fail the loop because if you can't poll it could be anything and you can't control with unknown variables around + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                        elif (line.flow_type == _COLD_FLOW):
                                            pass

                            elif (system_valves[valve].get_flow() == _COLD_FLOW):
                                lines = line_position[bay]
                                for line in lines:
                                    if (line.flow_type == _COLD_FLOW):

                                        line_devices = {**line.line_sensors, **line.pumps}.values()
                                        sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)  # this is to respect the imposed order
                                        iterate_sensor = system_valves[valve]
                                        for line_device in sorted_devices:
                                            # if (sensors[sensor].get_status()):

                                                Graph.add_node(line_device.get_name())
                                                Graph.add_edges_from([(line_device.get_name(), iterate_sensor.get_name())])
                                                iterate_sensor = line_device
                                            # else:

                                    #elif (line.flow_type == _HOT_FLOW):
                                        #pass            # pass

                                        device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                        Graph.add_node(device.get_name())
                                        Graph.add_edges_from([(device.get_name(), iterate_sensor.get_name())])

                                    # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                else:
                    print("{0} close".format(system_valves[valve]))
                    continue

        pos = nx.get_node_attributes(Graph, 'pos')
        plt.figure(0)
        plt.title('Online Configuration')
        # nx.draw(Graph, pos, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
        nx.draw_kamada_kawai(Graph, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
        # plt.show()
        return Graph
