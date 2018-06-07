from communicator_physical_layer import communicator_physical_layer
from configuration_reader import configuration_reader
from interface import interface
from matplotlib import pyplot as plt
from message_for_controller import message_for_controller
from object_tracker import object_tracker
from path_builder import path_builder
from switch_board_building import switch_board_building
from multiprocessing import Process, Pipe, Queue
from miscellaneous import AutoVivification
import pickle
import select
import socket
import sys
import time


_BOOSTER_NAME = "Source_1BH4"
_HOST = 'localhost'                 # Symbolic name meaning all available interfaces
_PORT = 50000              # Arbitrary non-privileged port
_BEGIN_WITH = 0
_INPUTS = "inputs"
_STATE = "state"
_GRAPH = "graph"
_COUNTER = "counter"
_BUSBARS = "busbar"
_AVAILABLE_COMPONENTS = "available_components"
_VALVES = 'Valves_active'


#  from IPython.core.debugger import Tracer
#  Tracer()()


class logical_layer(object):
    'Component that output the control object'
    def __init__(self, buildingID, SwitchID):
        self.buildingID = buildingID
        self.SwitchID = SwitchID
        self.building_config = switch_board_building(self.buildingID)
        self.intf = interface(self.building_config, self.SwitchID)
        self.objtk = object_tracker(self.intf)
        cfg = configuration_reader(self.intf)
        self.main_end, self.cfg_end = Pipe()
        self.work_q = Queue()
        #self.online_reader = Process(target=cfg.run, args=(self.cfg_end,))
        self.online_reader = Process(target=cfg.run, args=(self.work_q,))
        self.online_reader.daemon = True
        self.online_reader.start()
        self.comms = communicator_physical_layer()
        self.busy_busbars = {}
        # online_reader.join()  # https://stackoverflow.com/questions/25391025/what-exactly-is-python-multiprocessing-modules-join-method-doing?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

    def run(self, sinks, sources, boosted, parameters, setpoints):
        self.used_sinks = sinks
        self.used_sources = sources
        self.boosted = boosted
        self.parameters = parameters
        self.setpoints = setpoints
        self.process_started = False
        new_input = False
        requested_configuration = AutoVivification()  # nothing but a dictionary
        #system_input = {"sinks": self.used_sinks, "sources": self.used_sources, "boosted": self.boosted,
                        #"parameters": self.parameters, "setpoints": self.setpoints}
        pb = path_builder(self.intf, self.comms)
        mssgr = message_for_controller(self.intf, self.comms)
        #try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # https://stackoverflow.com/questions/45927337/recieve-data-only-if-available-in-python-sockets
            # op_controller = controller()
            s.bind((_HOST, _PORT))
            s.listen(1)
            print("Physical Layer Listening")
            readable = [s]  # list of readable sockets.  s is readable if a client is waiting.
            i = 0
            while True:
                r, w, e = select.select(readable, [], [], _BEGIN_WITH)  # the 0 here is the time out, it doesn't wait anything, it keeps cheking if the first argument is ready to be red
                for rs in r:  # iterate through readable sockets - so r is a list of objects included in readable that are ready to be read - if its ready there is a call from the client
                    if rs is s:  # is it the server - if one of the object ready to be red is the socket we are using to communicate, then we listen to it!
                        c, a = s.accept()  # this accept the first client in the queue - "c" is the socket object and "a" the ip and port object
                        print('\r{}:'.format(a), 'connected')
                        readable.append(c)  # add the connection with the client
                    else:
                        # read from a client represented by that readable object
                        data_from_API = rs.recv(1024)
                        if not data_from_API:
                            print('\r{}:'.format(rs.getpeername()), 'disconnected')
                            #self.killer_routine(requested_configuration, mssgr)
                            readable.remove(rs)
                            rs.close()
                        else:
                            system_input = pickle.loads(data_from_API)
                            system_input = self.check_sources(system_input)
                            name = str(system_input["sources"]) + str(system_input["sinks"])  # the logic is to check the name matching and then also the inputs matching and do something about it
                            print(name)
                            if (name not in requested_configuration.keys()):
                                requested_configuration[name][_INPUTS] = system_input
                                requested_configuration[name][_STATE] = "Inactive"
                                requested_configuration[name][_GRAPH] = []
                                requested_configuration[name][_COUNTER] = 0
                                requested_configuration[name][_BUSBARS] = []
                                requested_configuration[name][_AVAILABLE_COMPONENTS] = []
                                print('\r{}:'.format(rs.getpeername()), system_input)
                                new_input = True
                            else:
                                print("Input already given")
                if (new_input):
                    new_input = False
                    requested_configuration = self.find_suitable_setup(requested_configuration, pb)
                    requested_configuration = self.actuate_suitable_setup(requested_configuration)

                    print("si sono qui buone vacanze")
                    sys.exit()
                    '''
                    try:
                        if not self.work_q.empty():  # if there is a change in the online reading
                            plt.close('all')
                            online_configuration = self.work_q.get()
                            #print(requested_configuration)
                            requested_configuration = self.check_compatibility(requested_configuration, online_configuration, mssgr, pb)
                        elif (new_input):  # this handle the possibility that you have a new input without the online reading has changed --> please, do a method that enclose all this shit so you don't repeat
                                new_input = False
                                requested_configuration = self.check_compatibility(requested_configuration, online_configuration, mssgr, pb)
                        else: # this handle the possibility that the new input has not been activated at the first shot - should double check if this is still actual
                            for name, attributes in requested_configuration.items():
                                if ((requested_configuration[name][_STATE] == "Inactive") & (requested_configuration[name][_COUNTER] >= 1)):
                                    requested_configuration[name][_STATE] = mssgr.run(requested_configuration[name][_GRAPH], requested_configuration[name][_INPUTS], name)
                                    if (requested_configuration[name][_STATE] == "Inactive"):
                                        requested_configuration[name][_COUNTER] += 1
                                        if (requested_configuration[name][_COUNTER] >= 3):
                                            print("Configuration {0} failed to be delivered to the controller, please check the Pysical Layer connection")
                                            requested_configuration.pop(name)
                        i += 1
                        print('/-\|'[i % 4] + '\r', end='', flush=True)
                    except Exception:
                        print("Waiting for user input" + "." * 3, end="\r", flush=True)
                        pass'''

        #except(KeyboardInterrupt, SystemExit, Exception):
                    #for n in readable:
                    #    n.close()
        #            print(Exception.args)
        #            print("Unexpected error:", sys.exc_info()[0])
        #            print("Logical Layer Isolated")
        #            #s.shutdown() # this is that close both end of connection  alternative are SHUT_RD to avoid receiving and SHUT_WR to avoid the other to send
        #            self.online_reader.terminate()
        #            s.close()
        #            sys.exit()

    def check_sources(self, system_input):
        for source in system_input["sources"]:
            if (source == _BOOSTER_NAME):
                system_input["boosted"] = 'N'
        return system_input

    def check_compatibility(self, requested_configuration, online_configuration, mssgr, pb):
        if (requested_configuration):
            for name, attributes in requested_configuration.items():
                print(requested_configuration)
                requested_configuration[name][_GRAPH] = pb.run(requested_configuration[name][_INPUTS], online_configuration)
                if (requested_configuration[name][_GRAPH] is not None):  # if there is a matching between user input and online configuration
                    if (requested_configuration[name][_STATE] == "Inactive"):
                        print("Preparing Message")
                        requested_configuration[name][_STATE] = mssgr.run(requested_configuration[name][_GRAPH], requested_configuration[name][_INPUTS], name)
                        if (requested_configuration[name][_STATE] == "Inactive"):
                            requested_configuration[name][_COUNTER] = 1
                        print(requested_configuration[name][_STATE])

                else:
                    if (requested_configuration[name][_STATE] == "Active"):
                        print("Kill started process")
                        requested_configuration[name][_STATE] = mssgr.kill(requested_configuration[name][_INPUTS], name)
                        requested_configuration.pop(name)
                        print(requested_configuration)
                    else:
                        requested_configuration.pop(name)
        return requested_configuration

    def find_suitable_setup(self, requested_configuration, pb):
        for name, attributes in requested_configuration.items():
            if (requested_configuration[name][_STATE] == "Inactive"):
                suitable_setup = pb.run(requested_configuration[name][_INPUTS], self.busy_busbars)
                requested_configuration[name][_GRAPH] = suitable_setup[_GRAPH]
                requested_configuration[name][_AVAILABLE_COMPONENTS] = suitable_setup[_AVAILABLE_COMPONENTS]
                requested_configuration[name][_BUSBARS] = suitable_setup[_BUSBARS]
                self.busy_busbars[name] = suitable_setup[_BUSBARS]
        return requested_configuration

    def actuate_suitable_setup(self, requested_configuration):
        for name, attributes in requested_configuration.items():
            if (requested_configuration[name][_STATE] == "Inactive"):
                print(requested_configuration[name][_AVAILABLE_COMPONENTS][_VALVES])

        return requested_configuration

    '''def killer_routine(self, requested_configuration, mssgr):
        print("I will kill them all")
        if (requested_configuration):
            for name, attributes in requested_configuration.items():
                if (requested_configuration[name][_STATE] == "Active"):
                    print("Kill started process")
                    requested_configuration[name][_STATE] = mssgr.kill(requested_configuration[name][_INPUTS], name)
                    requested_configuration.pop(name)
        return requested_configuration'''


if __name__ == "__main__":
    start_time = time.time()
    test = logical_layer("Building716", "Switch_Board_1")
    sinks = ["Sink_1H7"]
    sources = ["Source_1BH4"]
    boosted = "N"
    parameters = "Energy"
    setpoints = 2

    test.run(sinks, sources, boosted, parameters, setpoints)
    print("--- %s seconds ---" % (time.time() - start_time))


'''From Test Rig to Online uncomment interface and related from, components_status.py, controller.py, physical_layer.py'''
