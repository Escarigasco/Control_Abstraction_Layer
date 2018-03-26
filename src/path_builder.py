from object_tracker import object_tracker
import networkx as nx
from networkx.algorithms import isomorphism
from matplotlib import pyplot as plt
_COLD_FLOW = 'C'
_HOT_FLOW = 'H'
_DIRECTION_IN = 'in'
_DIRECTION_OUT = 'out'
_FIRST_OF_THE_CLASS = 0
_BOOSTER = "booster"

class path_builder(object):

    def __init__(self, interface):
        self.builder = interface
        self.objtk = object_tracker(self.builder)

    def run(self, input_request):
        sources = input_request['sources']
        sensors = input_request['sensor']
        bays_sensors = []
        bays_sources = []

        Graph_A = nx.DiGraph()
        Graph_B = nx.DiGraph()
        Graph_C = nx.DiGraph()
        Graph_D = nx.DiGraph()
        possible_configurations = [Graph_A, Graph_B, Graph_C, Graph_D]
        idx = 0

        system_pumps = self.builder.get_system_pumps()
        system_sensors = self.builder.get_system_sensors()
        system_valves = self.builder.get_system_valves()
        system_connectors = self.builder.get_system_connectors()
        system_lines = self.builder.get_system_lines()
        system_pipes = self.builder.get_system_pipes()
        system_connected_devices = self.builder.get_connected_devices()
        # self.system_bays = self.builder.get_hydraulic_bays()
        system_busbars = self.builder.build_busbars(system_pipes)
        sensors_position = self.objtk.where_are_devices(system_sensors)
        connected_device_position = self.objtk.where_are_devices(system_connected_devices)
        valves_position = self.objtk.where_are_devices(system_valves)
        pump_position = self.objtk.where_are_devices(system_pumps)
        line_position = self.objtk.where_are_devices(system_lines)
        for source in sources:
            print(connected_device_position[source])
            bays_sources.append(connected_device_position[source])
        for sensor in sensors:
            print(sensors_position[sensor])
            bays_sensors.append(sensors_position[sensor])

        hot_busbars = {}
        cold_busbars = {}
        x_bb = 0
        y = 0
        x_v = 0
        x_dev = 0

        connected_valves = self.all_possible_valves(valves_position, bays_sensors, bays_sources)
        print(connected_valves)

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

                    print(idx)
                    possible_configurations[idx].add_node(hot_busbars[hot_busbar], pos=(x_bb, y))
                    print(hot_busbar)
                    x_bb += 50
                    possible_configurations[idx].add_node(cold_busbars[cold_busbar], pos=(x_bb, y))
                    print(cold_busbar)
                    for valve in connected_valves:
                        valve = valve.get_name()  # here you are parsing list of object so to extract the name you have to call a method
                        bay = valves_position[valve]
                        y = 0.5
                        x_v += 20
                        print(valve)
                        valve_connection = system_valves[valve].get_connection()

                        if (valve_connection == busbar_ID_hot):
                            busbar = busbar_ID_hot
                        elif (valve_connection == busbar_ID_cold):
                            busbar = busbar_ID_cold
                        else:
                            continue
                        if (valve_connection == busbar):
                            print(valve)

                            if (system_valves[valve].get_flow_direction() == _DIRECTION_IN):
                                possible_configurations[idx].add_node(system_valves[valve], pos=(x_v, y))
                                possible_configurations[idx].add_edges_from([(system_busbars[busbar], system_valves[valve])])
                                if (system_valves[valve].get_flow() == _HOT_FLOW):
                                        lines = line_position[bay]
                                        for line in lines:
                                            if (line.flow_type == _HOT_FLOW):
                                                x_dev += 50
                                                sensors = line.line_sensors
                                                iterate_sensor = system_valves[valve]
                                                for sensor in sensors.keys():
                                                    # if (sensors[sensor].get_status()):
                                                        y += 0.5

                                                        possible_configurations[idx].add_node(sensors[sensor], pos=(x_dev, y))
                                                        possible_configurations[idx].add_edges_from([(iterate_sensor, sensors[sensor])])
                                                        iterate_sensor = sensors[sensor]
                                                    # else:
                                                        # pass

                                                if (line.pumps):
                                                    y += 0.5
                                                    pump_id = pump_position[bay][_FIRST_OF_THE_CLASS].get_name()
                                                    pump = line.pumps[pump_id]
                                                    # if (pump.get_status()):
                                                    possible_configurations[idx].add_node(pump, pos=(x_dev, y))
                                                    possible_configurations[idx].add_edges_from([(iterate_sensor, pump)])
                                                    y += 0.5
                                                    device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                    possible_configurations[idx].add_node(device, pos=(x_dev, y))
                                                    possible_configurations[idx].add_edges_from([(pump, device)])
                                                else:
                                                    y += 0.5
                                                    device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                    possible_configurations[idx].add_node(device, pos=(x_dev, y))
                                                    possible_configurations[idx].add_edges_from([(iterate_sensor, device)])
                                                # else:  # if the pump is disconnected
                                                # continue  # if i want to make fail the loop because if you can't poll it could be anything and you can't control with unknown variables around + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                            elif (line.flow_type == _COLD_FLOW):
                                                pass

                                elif (system_valves[valve].get_flow() == _COLD_FLOW):
                                    lines = line_position[bay]
                                    for line in lines:
                                        if (line.flow_type == _COLD_FLOW):
                                            x_dev += 50
                                            sensors = line.line_sensors
                                            iterate_sensor = system_valves[valve]
                                            for sensor in sensors.keys():
                                                # if (sensors[sensor].get_status()):
                                                    y += 0.5
                                                    possible_configurations[idx].add_node(sensors[sensor], pos=(x_dev, y))
                                                    possible_configurations[idx].add_edges_from([(iterate_sensor, sensors[sensor])])
                                                    iterate_sensor = sensors[sensor]


                                                # else:
                                                    # pass

                                            if (line.pumps):
                                                y += 0.5
                                                pump_id = pump_position[bay][0].get_name()
                                                pump = line.pumps[pump_id]
                                                # if (pump.get_status()):
                                                possible_configurations[idx].add_node(pump, pos=(x_dev, y))
                                                possible_configurations[idx].add_edges_from([(iterate_sensor, pump)])
                                                y += 0.5
                                                device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                possible_configurations[idx].add_node(device, pos=(x_dev, y))
                                                possible_configurations[idx].add_edges_from([(pump, device)])
                                            else:
                                                y += 0.5
                                                device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                possible_configurations[idx].add_node(device, pos=(x_dev, y))
                                                possible_configurations[idx].add_edges_from([(iterate_sensor, device)])

                                        # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility

                            elif (system_valves[valve].get_flow_direction() == _DIRECTION_OUT):
                                possible_configurations[idx].add_node(system_valves[valve], pos=(x_v, y))
                                possible_configurations[idx].add_edges_from([(system_valves[valve], system_busbars[busbar])])
                                if (system_valves[valve].get_flow() == _HOT_FLOW):
                                        lines = line_position[bay]
                                        for line in lines:
                                            if (line.flow_type == _HOT_FLOW):
                                                x_dev += 50
                                                sensors = line.line_sensors
                                                iterate_sensor = system_valves[valve]
                                                for sensor in sensors.keys():
                                                    # if (sensors[sensor].get_status()):
                                                        y += 0.5
                                                        possible_configurations[idx].add_node(sensors[sensor], pos=(x_dev, y))
                                                        possible_configurations[idx].add_edges_from([(sensors[sensor], iterate_sensor)])
                                                        iterate_sensor = sensors[sensor]
                                                    # else:
                                                        # pass
                                                if (line.pumps):
                                                    y += 0.5
                                                    pump_id = pump_position[bay][_FIRST_OF_THE_CLASS].get_name()
                                                    pump = line.pumps[pump_id]
                                                    # if (pump.get_status()):
                                                    possible_configurations[idx].add_node(pump, pos=(x_dev, y))
                                                    possible_configurations[idx].add_edges_from([(pump, iterate_sensor)])
                                                    y += 0.5
                                                    device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                    possible_configurations[idx].add_node(device, pos=(x_dev, y))
                                                    possible_configurations[idx].add_edges_from([(device, pump)])
                                                else:
                                                    y += 0.5
                                                    device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                    possible_configurations[idx].add_node(device, pos=(x_dev, y))
                                                    possible_configurations[idx].add_edges_from([(device, iterate_sensor)])

                                                # else: # if the pump is disconnected
                                                # continue # if i want to make fail the loop because if you can't poll it could be anything and you can't control with unknown variables around + insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                            elif (line.flow_type == _COLD_FLOW):
                                                pass

                                elif (system_valves[valve].get_flow() == _COLD_FLOW):
                                    lines = line_position[bay]
                                    for line in lines:
                                        if (line.flow_type == _COLD_FLOW):
                                            x_dev += 50
                                            sensors = line.line_sensors
                                            iterate_sensor = system_valves[valve]
                                            for sensor in sensors.keys():
                                                # if (sensors[sensor].get_status()):
                                                    y += 0.5
                                                    possible_configurations[idx].add_node(sensors[sensor], pos=(x_dev, y))
                                                    possible_configurations[idx].add_edges_from([(sensors[sensor], iterate_sensor)])
                                                    iterate_sensor = sensors[sensor]
                                                # else:
                                                    # pass
                                            if (line.pumps):
                                                y += 0.5
                                                pump_id = pump_position[bay][_FIRST_OF_THE_CLASS].get_name()
                                                pump = line.pumps[pump_id]
                                                # if (pump.get_status()):
                                                possible_configurations[idx].add_node(pump, pos=(x_dev, y))
                                                possible_configurations[idx].add_edges_from([(iterate_sensor, pump)])
                                                y += 0.5
                                                device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                possible_configurations[idx].add_node(device, pos=(x_dev, y))
                                                possible_configurations[idx].add_edges_from([(pump, device)])
                                            else:
                                                y += 0.5
                                                device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                possible_configurations[idx].add_node(device, pos=(x_dev, y))
                                                possible_configurations[idx].add_edges_from([(device, iterate_sensor)])

                                            # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                    idx += 1
        '''nx.draw(possible_configurations[idx], with_labels=True)
        plt.show()'''

        '''pos = nx.spring_layout(possible_configurations[idx], iterations=10)
        nx.draw(possible_configurations[idx], pos, font_size=8, with_labels=True, node_size=40)
        plt.show()'''

        pos_0 = nx.get_node_attributes(possible_configurations[0], 'pos')
        pos_1 = nx.get_node_attributes(possible_configurations[1], 'pos')
        pos_2 = nx.get_node_attributes(possible_configurations[2], 'pos')
        pos_3 = nx.get_node_attributes(possible_configurations[3], 'pos')

        plt.figure(2)
        # nx.draw_shell(possible_configurations[0], font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
        nx.draw(possible_configurations[0], pos_0, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
        plt.figure(3)
        nx.draw(possible_configurations[1], pos_1, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
        plt.figure(4)
        nx.draw(possible_configurations[2], pos_2, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
        plt.figure(5)
        nx.draw_circular(possible_configurations[3], font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
        plt.show()
        return possible_configurations



    def all_possible_valves(self, valves_position, bays_sensors, bays_sources):
        possible_valves = []
        for bay_sources in bays_sources:
            possible_valves = possible_valves + valves_position[bay_sources]
            print(possible_valves)
        for bay_sensors in bays_sensors:
            possible_valves = possible_valves + valves_position[bay_sensors]
            print(possible_valves)
            # possible_valves = {**valves_position[bay_sensor], **valves_position[bay_source]}
        return possible_valves
