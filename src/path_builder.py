from matplotlib import pyplot as plt
import networkx as nx
from object_tracker import object_tracker
from path_matcher import path_matcher

_COLD_FLOW = 'C'
_HOT_FLOW = 'H'
_DIRECTION_IN = 'in'
_DIRECTION_OUT = 'out'
_FIRST_OF_THE_CLASS = 0
_BOOSTER = "booster"
_BOOSTER_BAR = 'B'
_OFFSET_FIGURE = 1

class path_builder(object):

    def __init__(self, interface):
        self.builder = interface
        self.objtk = object_tracker(self.builder)

    def run(self, input_request, online_configuration):
        pm = path_matcher(online_configuration)
        sources = input_request['sources']
        sensors = input_request['sensor']
        boosted = input_request['boosted']
        bays_sensors = []
        bays_sources = []
        boosted = self.check_sources(sources, boosted)

        # It is hardcoded the number o
        Graph_A = nx.DiGraph()
        Graph_B = nx.DiGraph()
        Graph_C = nx.DiGraph()
        Graph_D = nx.DiGraph()
        possible_configurations = [Graph_A, Graph_B, Graph_C, Graph_D]
        idx = 0

        system_sensors = self.builder.get_system_sensors()
        system_valves = self.builder.get_system_valves()
        system_lines = self.builder.get_system_lines()
        system_pipes = self.builder.get_system_pipes()
        system_connected_devices = self.builder.get_connected_devices()
        system_busbars = self.builder.build_busbars(system_pipes)
        sensors_position = self.objtk.where_are_devices(system_sensors)
        connected_device_position = self.objtk.where_are_devices(system_connected_devices)
        valves_position = self.objtk.where_are_devices(system_valves)
        line_position = self.objtk.where_are_devices(system_lines)
        for source in sources:
            bays_sources.append(connected_device_position[source])
        for sensor in sensors:
            bays_sensors.append(sensors_position[sensor])

        hot_busbars = {}
        cold_busbars = {}
        x_bb = 0
        y = 0
        x_v = 0
        x_dev = 0

        connected_valves = self.all_possible_valves(valves_position, bays_sensors, bays_sources, boosted, connected_device_position)
        for busbar in system_busbars.keys():
            if (system_busbars[busbar].flow == _HOT_FLOW and system_busbars[busbar].type != _BOOSTER):
                hot_busbars[busbar] = system_busbars[busbar]

            elif (system_busbars[busbar].flow == _COLD_FLOW and system_busbars[busbar].type != _BOOSTER):
                cold_busbars[busbar] = system_busbars[busbar]

        for hot_busbar in hot_busbars.keys():
            x_bb = 0
            busbar_ID_hot = hot_busbars[hot_busbar].get_name()
            for cold_busbar in cold_busbars.keys():
                    y = 0
                    x_bb += 50
                    x_v = 0
                    x_dev = 0
                    busbar_ID_cold = cold_busbars[cold_busbar].get_name()
                    # possible_configurations[idx].add_node(hot_busbars[hot_busbar].get_name(), pos=(x_bb, y))
                    possible_configurations[idx].add_node(hot_busbars[hot_busbar].get_name())
                    x_bb += 50
                    # possible_configurations[idx].add_node(cold_busbars[cold_busbar].get_name(), pos=(x_bb, y))
                    possible_configurations[idx].add_node(cold_busbars[cold_busbar].get_name())
                    for valve in connected_valves:
                        valve = valve.get_name()  # here you are parsing list of object so to extract the name you have to call a method
                        bay = valves_position[valve]
                        valve_connection = system_valves[valve].get_connection()
                        if (valve_connection == busbar_ID_hot):
                            busbar = busbar_ID_hot
                        elif (valve_connection == busbar_ID_cold):
                            busbar = busbar_ID_cold
                        else:
                            busbar = _BOOSTER_BAR
                            x_bb += 50
                            if (valve_connection == busbar):
                                # possible_configurations[idx].add_node(system_busbars[busbar].get_name(), pos=(x_bb, 0))
                                possible_configurations[idx].add_node(system_busbars[busbar].get_name())
                                # print("yes, i have accessed because I was parsing valve {0}".format(valve))
                        y = 0.5
                        x_v += 20
                        if (valve_connection == busbar):

                            if (system_valves[valve].get_flow_direction() == _DIRECTION_IN):
                                # possible_configurations[idx].add_node(system_valves[valve].get_name(), pos=(x_v, y))
                                possible_configurations[idx].add_node(system_valves[valve].get_name())
                                possible_configurations[idx].add_edges_from([(system_busbars[busbar].get_name(), system_valves[valve].get_name())])
                                if (system_valves[valve].get_flow() == _HOT_FLOW):
                                        lines = line_position[bay]
                                        for line in lines:
                                            if (line.flow_type == _HOT_FLOW):
                                                x_dev += 50
                                                line_devices = {**line.line_sensors, **line.pumps}.values()
                                                sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)
                                                iterate_sensor = system_valves[valve]
                                                for line_device in sorted_devices:
                                                    # if (sensors[sensor].get_status()):
                                                        y += 0.5

                                                        # possible_configurations[idx].add_node(line_device.get_name(), pos=(x_dev, y))
                                                        possible_configurations[idx].add_node(line_device.get_name())
                                                        possible_configurations[idx].add_edges_from([(iterate_sensor.get_name(), line_device.get_name())])
                                                        iterate_sensor = line_device
                                                    # else:
                                                        # pass

                                                y += 0.5
                                                device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                # possible_configurations[idx].add_node(device.get_name(), pos=(x_dev, y))
                                                possible_configurations[idx].add_node(device.get_name())
                                                possible_configurations[idx].add_edges_from([(iterate_sensor.get_name(), device.get_name())])
                                                # else:  # if the pump is disconnected
                                                # continue  # if i want to make fail the loop because if you can't poll it could be anything and you can't control with unknown variables around + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                            elif (line.flow_type == _COLD_FLOW):
                                                pass

                                elif (system_valves[valve].get_flow() == _COLD_FLOW):
                                    lines = line_position[bay]
                                    for line in lines:
                                        if (line.flow_type == _COLD_FLOW):
                                            x_dev += 50
                                            line_devices = {**line.line_sensors, **line.pumps}.values()
                                            sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)
                                            iterate_sensor = system_valves[valve]
                                            for line_device in sorted_devices:
                                                # if (sensors[sensor].get_status()):
                                                    y += 0.5

                                                    possible_configurations[idx].add_node(line_device.get_name(), pos=(x_dev, y))
                                                    possible_configurations[idx].add_edges_from([(iterate_sensor.get_name(), line_device.get_name())])
                                                    iterate_sensor = line_device
                                                # else:
                                                    # pass

                                            y += 0.5
                                            device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                            possible_configurations[idx].add_node(device.get_name(), pos=(x_dev, y))
                                            possible_configurations[idx].add_edges_from([(iterate_sensor.get_name(), device.get_name())])

                                        # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility

                            elif (system_valves[valve].get_flow_direction() == _DIRECTION_OUT):
                                # possible_configurations[idx].add_node(system_valves[valve].get_name(), pos=(x_v, y))
                                possible_configurations[idx].add_node(system_valves[valve].get_name())
                                possible_configurations[idx].add_edges_from([(system_valves[valve].get_name(), system_busbars[busbar].get_name())])
                                if (system_valves[valve].get_flow() == _HOT_FLOW):
                                        lines = line_position[bay]
                                        for line in lines:
                                            if (line.flow_type == _HOT_FLOW):
                                                x_dev += 50
                                                line_devices = {**line.line_sensors, **line.pumps}.values()
                                                sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)
                                                iterate_sensor = system_valves[valve]
                                                for line_device in sorted_devices:
                                                    # if (sensors[sensor].get_status()):
                                                        y += 0.5

                                                        # possible_configurations[idx].add_node(line_device.get_name(), pos=(x_dev, y))
                                                        possible_configurations[idx].add_node(line_device.get_name())
                                                        possible_configurations[idx].add_edges_from([(line_device.get_name(), iterate_sensor.get_name())])
                                                        iterate_sensor = line_device
                                                    # else:
                                                        # pass

                                                y += 0.5
                                                device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                # possible_configurations[idx].add_node(device.get_name(), pos=(x_dev, y))
                                                possible_configurations[idx].add_node(device.get_name())
                                                possible_configurations[idx].add_edges_from([(device.get_name(), iterate_sensor.get_name())])

                                                # else: # if the pump is disconnected
                                                # continue # if i want to make fail the loop because if you can't poll it could be anything and you can't control with unknown variables around + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                            elif (line.flow_type == _COLD_FLOW):
                                                pass

                                elif (system_valves[valve].get_flow() == _COLD_FLOW):
                                    lines = line_position[bay]
                                    for line in lines:
                                        if (line.flow_type == _COLD_FLOW):
                                            x_dev += 50
                                            line_devices = {**line.line_sensors, **line.pumps}.values()
                                            sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)
                                            iterate_sensor = system_valves[valve]
                                            for line_device in sorted_devices:
                                                # if (sensors[sensor].get_status()):
                                                    y += 0.5

                                                    # possible_configurations[idx].add_node(line_device.get_name(), pos=(x_dev, y))
                                                    possible_configurations[idx].add_node(line_device.get_name())
                                                    possible_configurations[idx].add_edges_from([(line_device.get_name(), iterate_sensor.get_name())])
                                                    iterate_sensor = line_device
                                                # else:
                                                    # pass

                                            y += 0.5
                                            device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                            # possible_configurations[idx].add_node(device.get_name(), pos=(x_dev, y))
                                            possible_configurations[idx].add_node(device.get_name())
                                            possible_configurations[idx].add_edges_from([(device.get_name(), iterate_sensor.get_name())])
                    is_match = pm.run(possible_configurations[idx], idx)
                    print(is_match)
                    if (is_match):
                        plt.figure(idx + _OFFSET_FIGURE)
                        nx.draw_kamada_kawai(possible_configurations[idx], font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
                        return possible_configurations[idx]
                    else:
                        print("Configuration {0} did not match match online reading \n".format(idx))
                        plt.figure(idx + _OFFSET_FIGURE)
                        nx.draw_kamada_kawai(possible_configurations[0], font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
                        idx += 1

    def all_possible_valves(self, valves_position, bays_sensors, bays_sources, boosted, connected_device_position):
        possible_valves = []
        booster = 'Source_1BH4'
        if (boosted == 'N'):
            for bay_sources in bays_sources:
                for valve in valves_position[bay_sources]:
                    if (valve.get_connection() != _BOOSTER_BAR):
                        possible_valves.append(valve)
            for bay_sensors in bays_sensors:
                for valve in valves_position[bay_sensors]:
                    if (valve.get_connection() != _BOOSTER_BAR):
                        possible_valves.append(valve)
            return possible_valves
        elif (boosted == 'Y'):
            for bay_sources in bays_sources:
                for valve in valves_position[bay_sources]:
                    if ((valve.get_flow() == _COLD_FLOW and valve.get_connection() != _BOOSTER_BAR) or (valve.get_flow() == _HOT_FLOW and valve.get_connection() == _BOOSTER_BAR)):
                        possible_valves.append(valve)
            for bay_sensors in bays_sensors:
                possible_valves = possible_valves + valves_position[bay_sensors]
            bay_booster = connected_device_position[booster]
            booster_valves = valves_position[bay_booster]
            for valve in booster_valves:
                    if ((valve.get_flow() == _HOT_FLOW and valve.get_connection() != _BOOSTER_BAR) or (valve.get_flow() == _COLD_FLOW and valve.get_connection() == _BOOSTER_BAR)):
                        possible_valves.append(valve)
            return possible_valves

    def check_sources(self, sources, boosted):
        for source in sources:
            if (source == 'Source_1BH4'):
                boosted = 'N'
        return boosted
