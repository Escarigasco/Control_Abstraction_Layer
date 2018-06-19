#  Class to read the online configuration - the random server will be replaced with a status reader.
#  the algorithm is of the type - for each bus bar, for each valve connected to the bus bar, if the flow entering the valve goes in/out to the connected device, if this flow is cold/hot,
#  then you know which connector line -> add all devices of the line -> add the connected device of the bay the valve in exam is connected
# if a valve is off the algo goes to the next one leaving one branch open
from communicator_physical_layer import communicator_physical_layer
import threading
from object_tracker import object_tracker
from random_server import current_status_reader
import networkx as nx
import time
from matplotlib import pyplot as plt
import sys
_COLD_FLOW = 'C'
_HOT_FLOW = 'H'
_DIRECTION_IN = 'in'
_DIRECTION_OUT = 'out'
_FIRST_OF_THE_CLASS = 0  # a constant is use to indicate the first element of a list - in reality for every case it could be a random number within the list indexes range, used 0 not to call a random number generator


class configuration_reader(object):
#class configuration_reader(threading.Thread):

    def __init__(self, interface):
    #def __init__(self, interface, work_queue, queue_lock):
        #super(configuration_reader, self).__init__()   # super() will call Thread.__init__ for you
        self.config_reader = interface
        self.objtk = object_tracker(self.config_reader)
        #self.q_lock = queue_lock
        #self.work_q = work_queue
        #self._stop_event = threading.Event()
        # system_bays = self.config_reader.get_hydraulic_bays()
        self.comms = communicator_physical_layer()

    def run(self, worker_q):
        self.Graph = nx.DiGraph()
        self.UpdatedGraph = nx.DiGraph()
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
        cold_start = 1
        valve_status_online = []
        valve_status_previous = []

        ro = current_status_reader(self.comms, system_pumps, system_sensors, system_valves)
        plt.ion()
        plt.show()

        while True:
            try:

                time.sleep(0.1)
                status_online_reading = ro.run_online()
                if (status_online_reading):

                    valve_status_online = []
                    for valve in system_valves.values():
                        valve_status_online.append(valve.get_status())

                    if (valve_status_online != valve_status_previous):
                        valve_status_previous = valve_status_online

                        for busbar in system_busbars.keys():

                            busbar_ID = system_busbars[busbar].get_name()
                            self.Graph.add_node(system_busbars[busbar].get_name())
                            for valve in system_valves.keys():

                                bay = valves_position[valve]
                                if (system_valves[valve].get_status()):
                                    #print("{0} open".format(system_valves[valve]))
                                    self.Graph.add_node(system_valves[valve].get_name())
                                    valve_connection = system_valves[valve].get_connection()
                                    if (valve_connection == busbar_ID):
                                        if (system_valves[valve].get_flow_direction() == _DIRECTION_IN):

                                            self.Graph.add_edges_from([(system_busbars[busbar].get_name(), system_valves[valve].get_name())])
                                            if (system_valves[valve].get_flow() == _HOT_FLOW):

                                                    lines = line_position[bay]
                                                    for line in lines:
                                                        if (line.flow_type == _HOT_FLOW):

                                                            line_devices = {**line.line_sensors, **line.pumps}.values()
                                                            sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)  # this is to respect the imposed order
                                                            iterate_sensor = system_valves[valve]
                                                            for line_device in sorted_devices:
                                                                # if (sensors[sensor].get_status()):

                                                                    self.Graph.add_node(line_device.get_name())
                                                                    self.Graph.add_edges_from([(iterate_sensor.get_name(), line_device.get_name())])
                                                                    iterate_sensor = line_device
                                                                # else:
                                                                    # pass

                                                            device = connected_device_position[bay][_FIRST_OF_THE_CLASS]

                                                            self.Graph.add_node(device.get_name())
                                                            self.Graph.add_edges_from([(iterate_sensor.get_name(), device.get_name())])
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

                                                                self.Graph.add_node(line_device.get_name())
                                                                self.Graph.add_edges_from([(iterate_sensor.get_name(), line_device.get_name())])
                                                                iterate_sensor = line_device
                                                            # else:
                                                                # pass

                                                        device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                        #self.Graph.add_node(device.get_name(), pos=(x_dev, y))
                                                        self.Graph.add_node(device.get_name())
                                                        self.Graph.add_edges_from([(iterate_sensor.get_name(), device.get_name())])

                                                    #elif (line.flow_type == _HOT_FLOW):
                                                        #pass
                                                        # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility

                                        elif (system_valves[valve].get_flow_direction() == _DIRECTION_OUT):

                                            self.Graph.add_edges_from([(system_valves[valve].get_name(), system_busbars[busbar].get_name())])
                                            if (system_valves[valve].get_flow() == _HOT_FLOW):
                                                    lines = line_position[bay]
                                                    for line in lines:
                                                        if (line.flow_type == _HOT_FLOW):

                                                            line_devices = {**line.line_sensors, **line.pumps}.values()
                                                            sorted_devices = sorted(line_devices, key=lambda line_object: line_object.position)  # this is to respect the imposed order
                                                            iterate_sensor = system_valves[valve]
                                                            for line_device in sorted_devices:
                                                                # if (sensors[sensor].get_status()):

                                                                    self.Graph.add_node(line_device.get_name())
                                                                    self.Graph.add_edges_from([(line_device.get_name(), iterate_sensor.get_name())])
                                                                    iterate_sensor = line_device
                                                                # else:
                                                                    # pass

                                                            device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                            #self.Graph.add_node(device.get_name(), pos=(x_dev, y))
                                                            self.Graph.add_node(device.get_name())
                                                            self.Graph.add_edges_from([(device.get_name(), iterate_sensor.get_name())])

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

                                                                self.Graph.add_node(line_device.get_name())
                                                                self.Graph.add_edges_from([(line_device.get_name(), iterate_sensor.get_name())])
                                                                iterate_sensor = line_device
                                                            # else:

                                                    #elif (line.flow_type == _HOT_FLOW):
                                                        #pass            # pass

                                                        device = connected_device_position[bay][_FIRST_OF_THE_CLASS]
                                                        self.Graph.add_node(device.get_name())
                                                        self.Graph.add_edges_from([(device.get_name(), iterate_sensor.get_name())])

                                                    # insert sensor(for the sensors the order doesn't matter) + insert device -- define methods to do this to increase readibility
                                else:
                                    #print("{0} close".format(system_valves[valve]))
                                    continue

                        #print(not nx.is_isomorphic(self.UpdatedGraph, self.Graph))
                        #if (cold_start):

                        #    worker_q.put(self.Graph)
                            #self.Graph.clear()
                        #    cold_start = 0
                        #if (not self.UpdatedGraph.nodes() == self.Graph.nodes()):
                        if (not nx.is_isomorphic(self.UpdatedGraph, self.Graph)):
                            self.UpdatedGraph.clear()
                            #print("I am updatingggggggggggggggggggggggggggggggggggggggggggggggggggggggggg")
                            plt.clf()
                            plt.title('Online Configuration')
                            self.UpdatedGraph = nx.union(self.UpdatedGraph, self.Graph)
                            self.Graph.clear()
                            nx.draw_kamada_kawai(self.UpdatedGraph, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
                            plt.pause(0.001)
                            #worker_q.send(self.UpdatedGraph)
                            print("Give me some new honeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
                            worker_q.put(self.UpdatedGraph)
                            #print(self.UpdatedGraph.nodes())
                else:
                    pass
            except (KeyboardInterrupt, SystemExit, Exception):
                print("Online reader Thread Stopped")
                print("Process Error. Stopped")
                worker_q.close()
                sys.exit()

        #print(self.UpdatedGraph.nodes())
        #print(self.Graph.nodes())
            # plt.show()
        #returnself.Graph
