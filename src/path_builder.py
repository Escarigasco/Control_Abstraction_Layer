#  Class to create the all possible configuration - bays with relevant sinks and sources are identified -> valves connected to this bays are extracted.
#  the algorithm is of the type - for each hotbus bar, for each cold busbar, for each indentified valve connected to the bus bar and the relevant bay, if the flow entering the valve goes in/out to the connected device, if this flow is cold/hot,
#  then you know which connector line -> add all devices of the line -> add the connected device of the bay the valve in exam is connected
#  the method is necessary to extract the relevant valve based on the inputs

from matplotlib import pyplot as plt
from object_tracker import object_tracker
from path_matcher import path_matcher
from configuration_selector import configuration_selector
import networkx as nx
import sys

_COLD_FLOW = "C"
_HOT_FLOW = "H"
_DIRECTION_IN = "in"
_DIRECTION_OUT = "out"
_FIRST_OF_THE_CLASS = 0
_BOOSTER = "booster"
_BOOSTER_NAME = "Source_1BH4"
_BOOSTER_BAR = "B"
_OFFSET_FIGURE = 2
_FINAL_BOOSTER = "final_booster"
_START_SOURCE = "start_source"
_MIDDLE_BOOSTER = "middle_booster"
_POSSIBLE_VALVES = "possible_valves"
_ALL_VALVES = "all_valves"



class path_builder(object):

    def __init__(self, interface, comms, translator):
        self.builder = interface
        self.objtk = object_tracker(self.builder)
        self.system_sensors = self.builder.get_system_sensors()
        self.system_valves = self.builder.get_system_valves()
        self.system_lines = self.builder.get_system_lines()
        self.system_pipes = self.builder.get_system_pipes()
        self.system_pumps =  self.builder.get_system_pumps()
        self.system_connected_devices = self.builder.get_connected_devices()
        self.system_busbars = self.builder.build_busbars(self.system_pipes)
        self.connected_device_position = self.objtk.where_are_devices(self.system_connected_devices)
        self.valves_position = self.objtk.where_are_devices(self.system_valves)
        self.line_position = self.objtk.where_are_devices(self.system_lines)
        self.conf_slct = configuration_selector(self.system_sensors, self.system_valves, self.system_pumps, self.system_connected_devices, self.system_busbars, self.builder, comms, translator)

    def run(self, input_request, busy_busbars):

        #pm = path_matcher(online_configuration)
        hot_busbars = {}
        cold_busbars = {}
        actuable_configuration = {}
        excluded_components = input_request["excluded_components"]
        idx = 1

        valves_collection = self.all_possible_valves(input_request)
        connected_valves = valves_collection[_POSSIBLE_VALVES]
        all_valves = valves_collection[_ALL_VALVES]

        for busbar in self.system_busbars.keys():
            if (self.system_busbars[busbar].flow == _HOT_FLOW and self.system_busbars[busbar].type != _BOOSTER):
                hot_busbars[busbar] = self.system_busbars[busbar]

            elif (self.system_busbars[busbar].flow == _COLD_FLOW and self.system_busbars[busbar].type != _BOOSTER):
                cold_busbars[busbar] = self.system_busbars[busbar]

        for hot_busbar in hot_busbars.keys():

            busbar_ID_hot = hot_busbars[hot_busbar].get_name()
            for cold_busbar in cold_busbars.keys():

                    busbar_ID_cold = cold_busbars[cold_busbar].get_name()
                    # actuable_configuration[configuration_name].add_node(hot_busbars[hot_busbar].get_name(), pos=(x_bb, y))
                    configuration_name = busbar_ID_hot + busbar_ID_cold
                    actuable_configuration[configuration_name] = nx.DiGraph()
                    actuable_configuration[configuration_name].add_node(hot_busbars[hot_busbar].get_name())

                    # actuable_configuration[configuration_name].add_node(cold_busbars[cold_busbar].get_name(), pos=(x_bb, y))
                    actuable_configuration[configuration_name].add_node(cold_busbars[cold_busbar].get_name())

                    for valve in connected_valves:
                        valve = valve.get_name()  # here you are parsing list of object so to extract the name you have to call a method
                        bay = self.valves_position[valve]
                        valve_connection = self.system_valves[valve].get_connection()

                        if (valve_connection == busbar_ID_hot):
                            busbar = busbar_ID_hot
                        elif (valve_connection == busbar_ID_cold):
                            busbar = busbar_ID_cold
                        else:
                            busbar = _BOOSTER_BAR

                            if (valve_connection == busbar):
                                # actuable_configuration[configuration_name].add_node(self.system_busbars[busbar].get_name(), pos=(x_bb, 0))
                                actuable_configuration[configuration_name].add_node(self.system_busbars[busbar].get_name())
                                # print("yes, i have accessed because I was parsing valve {0}".format(valve))

                        if (valve_connection == busbar):

                            if (self.system_valves[valve].get_flow_direction() == _DIRECTION_IN):
                                # actuable_configuration[configuration_name].add_node(self.system_valves[valve].get_name(), pos=(x_v, y))
                                actuable_configuration[configuration_name].add_node(self.system_valves[valve].get_name())
                                actuable_configuration[configuration_name].add_edges_from([(self.system_busbars[busbar].get_name(), self.system_valves[valve].get_name())])
                                if (self.system_valves[valve].get_flow() == _HOT_FLOW):
                                        lines = self.line_position[bay]
                                        for line in lines:
                                            if (line.flow_type == _HOT_FLOW):

                                                line_devices = {**line.line_sensors, **line.pumps}.values()
                                                sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)  # this is to respect the imposed order
                                                iterate_sensor = self.system_valves[valve]
                                                for line_device in sorted_devices:
                                                    # if (sensors[sensor].get_status()):

                                                        # actuable_configuration[configuration_name].add_node(line_device.get_name(), pos=(x_dev, y))
                                                        actuable_configuration[configuration_name].add_node(line_device.get_name())
                                                        actuable_configuration[configuration_name].add_edges_from([(iterate_sensor.get_name(), line_device.get_name())])
                                                        iterate_sensor = line_device
                                                    # else:
                                                        # pass

                                                device = self.connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                # actuable_configuration[configuration_name].add_node(device.get_name(), pos=(x_dev, y))
                                                actuable_configuration[configuration_name].add_node(device.get_name())
                                                actuable_configuration[configuration_name].add_edges_from([(iterate_sensor.get_name(), device.get_name())])
                                                # else:  # if the pump is disconnected
                                                # continue  # if i want to make fail the loop because if you can't poll it could be anything and you can't control with unknown variables around + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                            elif (line.flow_type == _COLD_FLOW):
                                                pass

                                elif (self.system_valves[valve].get_flow() == _COLD_FLOW):
                                    lines = self.line_position[bay]
                                    for line in lines:
                                        if (line.flow_type == _COLD_FLOW):

                                            line_devices = {**line.line_sensors, **line.pumps}.values()
                                            sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)  # this is to respect the imposed order
                                            iterate_sensor = self.system_valves[valve]
                                            for line_device in sorted_devices:
                                                # if (sensors[sensor].get_status()):

                                                    actuable_configuration[configuration_name].add_node(line_device.get_name())
                                                    actuable_configuration[configuration_name].add_edges_from([(iterate_sensor.get_name(), line_device.get_name())])
                                                    iterate_sensor = line_device
                                                # else:
                                                    # pass

                                            device = self.connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                            actuable_configuration[configuration_name].add_node(device.get_name())
                                            actuable_configuration[configuration_name].add_edges_from([(iterate_sensor.get_name(), device.get_name())])

                                        # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility

                            elif (self.system_valves[valve].get_flow_direction() == _DIRECTION_OUT):
                                # actuable_configuration[configuration_name].add_node(self.system_valves[valve].get_name(), pos=(x_v, y))
                                actuable_configuration[configuration_name].add_node(self.system_valves[valve].get_name())
                                actuable_configuration[configuration_name].add_edges_from([(self.system_valves[valve].get_name(), self.system_busbars[busbar].get_name())])
                                if (self.system_valves[valve].get_flow() == _HOT_FLOW):
                                        lines = self.line_position[bay]
                                        for line in lines:
                                            if (line.flow_type == _HOT_FLOW):

                                                line_devices = {**line.line_sensors, **line.pumps}.values()
                                                sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)  # this is to respect the imposed order
                                                iterate_sensor = self.system_valves[valve]
                                                for line_device in sorted_devices:
                                                    # if (sensors[sensor].get_status()):

                                                        # actuable_configuration[configuration_name].add_node(line_device.get_name(), pos=(x_dev, y))
                                                        actuable_configuration[configuration_name].add_node(line_device.get_name())
                                                        actuable_configuration[configuration_name].add_edges_from([(line_device.get_name(), iterate_sensor.get_name())])
                                                        iterate_sensor = line_device
                                                    # else:
                                                        # pass

                                                device = self.connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                # actuable_configuration[configuration_name].add_node(device.get_name(), pos=(x_dev, y))
                                                actuable_configuration[configuration_name].add_node(device.get_name())
                                                actuable_configuration[configuration_name].add_edges_from([(device.get_name(), iterate_sensor.get_name())])

                                                # else: # if the pump is disconnected
                                                # continue # if i want to make fail the loop because if you can't poll it could be anything and you can't control with unknown variables around + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                            elif (line.flow_type == _COLD_FLOW):
                                                pass

                                elif (self.system_valves[valve].get_flow() == _COLD_FLOW):
                                    lines = self.line_position[bay]
                                    for line in lines:
                                        if (line.flow_type == _COLD_FLOW):

                                            line_devices = {**line.line_sensors, **line.pumps}.values()
                                            sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)  # this is to respect the imposed order
                                            iterate_sensor = self.system_valves[valve]
                                            for line_device in sorted_devices:
                                                # if (sensors[sensor].get_status()):

                                                    # actuable_configuration[configuration_name].add_node(line_device.get_name(), pos=(x_dev, y))
                                                    actuable_configuration[configuration_name].add_node(line_device.get_name())
                                                    actuable_configuration[configuration_name].add_edges_from([(line_device.get_name(), iterate_sensor.get_name())])
                                                    iterate_sensor = line_device
                                                # else:
                                                    # pass

                                            device = self.connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                            # actuable_configuration[configuration_name].add_node(device.get_name(), pos=(x_dev, y))
                                            actuable_configuration[configuration_name].add_node(device.get_name())
                                            actuable_configuration[configuration_name].add_edges_from([(device.get_name(), iterate_sensor.get_name())])
                    idx += 1
                    #plt.figure(idx)
                    #nx.draw_kamada_kawai(actuable_configuration[configuration_name], font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
                    #plt.pause(0.001)
                    #plt.savefig('books_read.png')

                    #is_match = pm.run(actuable_configuration[configuration_name], idx)
                    #if (is_match):

                    #    plt.figure(idx + _OFFSET_FIGURE)
                    #    plt.clf()
                    #    plt.title('Matched Configuration')
                    #    nx.draw_kamada_kawai(actuable_configuration[configuration_name], font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
                    #    plt.pause(0.001)

                    #    return actuable_configuration[configuration_name]

                    #else:
                    #    print("Configuration {0} did not match match online reading \n".format(idx))

                        #plt.figure(idx + _OFFSET_FIGURE)
                        #plt.clf()
                        #plt.title('Not Compatible Configuratiion')
                        #nx.draw_kamada_kawai(actuable_configuration[configuration_name], font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
                        #plt.pause(0.001)

        #for i in actuable_configuration.keys():
            #print(i)
            #print(actuable_configuration[i].nodes)

        configuration_selected = self.conf_slct.start_screening(actuable_configuration, busy_busbars, all_valves, excluded_components)
        return configuration_selected

    def all_possible_valves(self, input_request):
        sources = input_request['sources']
        sinks = input_request['sinks']
        boosted = input_request['boosted']
        possible_valves = []
        all_valves = []
        valves_collection = {}
        bays_sinks = []

        for sink in sinks:
            bays_sinks.append(self.connected_device_position[sink])

        if (boosted == 'Y'):
            #bay_start_source = []
            bays_middle_sources = []
            #bay_end_source = []

            start_source = input_request[_START_SOURCE]
            bay_start_source = self.connected_device_position[start_source]
            middle_sources = input_request[_MIDDLE_BOOSTER]
            if middle_sources:
                for source in middle_sources:
                    bays_middle_sources.append(self.connected_device_position[source])
            end_source = input_request[_FINAL_BOOSTER]
            bay_end_source = self.connected_device_position[end_source]

            print(bay_start_source, bays_middle_sources, bay_end_source)

        if (boosted == 'N'):
            bays_sources = []

            for source in sources:
                bays_sources.append(self.connected_device_position[source])

            for bay_sources in bays_sources:
                for valve in self.valves_position[bay_sources]:
                    all_valves.append(valve)
                    if (valve.get_connection() != _BOOSTER_BAR):
                        possible_valves.append(valve)
            for bay_sink in bays_sinks:
                for valve in self.valves_position[bay_sink]:
                    all_valves.append(valve)
                    if (valve.get_connection() != _BOOSTER_BAR):
                        possible_valves.append(valve)

        elif (boosted == 'Y'):
            for bay_sink in bays_sinks:
                possible_valves = possible_valves + self.valves_position[bay_sink]
                all_valves = all_valves + self.valves_position[bay_sink]
            '''start_source'''
            for valve in self.valves_position[bay_start_source]:
                all_valves.append(valve)
                if ((valve.get_flow() == _COLD_FLOW and valve.get_connection() != _BOOSTER_BAR) or (valve.get_flow() == _HOT_FLOW and valve.get_connection() == _BOOSTER_BAR)):
                    possible_valves.append(valve)

            '''end_source'''
            for valve in self.valves_position[bay_end_source]:
                all_valves.append(valve)
                if ((valve.get_flow() == _HOT_FLOW and valve.get_connection() != _BOOSTER_BAR) or (valve.get_flow() == _COLD_FLOW and valve.get_connection() == _BOOSTER_BAR)):
                    possible_valves.append(valve)
            '''middle_sources'''
            if bays_middle_sources:
                for bay in bays_middle_sources:
                    for valve in self.valves_position[bay]:
                        all_valves.append(valve)
                        if ((valve.get_flow() == _HOT_FLOW and valve.get_connection() == _BOOSTER_BAR) or (valve.get_flow() == _COLD_FLOW and valve.get_connection() == _BOOSTER_BAR)):
                            possible_valves.append(valve)

        valves_collection = {_ALL_VALVES: all_valves, _POSSIBLE_VALVES: possible_valves}
        return valves_collection
