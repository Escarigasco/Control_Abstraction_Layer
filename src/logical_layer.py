from communicator_physical_layer import communicator_physical_layer
from configuration_reader import configuration_reader
from interface import interface
from logic import logic
from message_for_controller import message_for_controller
from miscellaneous import AutoVivification
from multiprocessing import Process
from multiprocessing import Queue
from name_translator import name_translator
from path_builder import path_builder
from path_matcher import path_matcher
from switch_board_building import switch_board_building
import copy
import pickle
import select
import socket
import sys
import time

_BEGIN_WITH = 0
_HOST = 'localhost'                 # Symbolic name meaning all available interfaces
_PORT = 50000              # Arbitrary non-privileged port

#  from IPython.core.debugger import Tracer
#  Tracer()()


class logical_layer(object):
    'Component that output the control object'
    def __init__(self, buildingID, SwitchID):
        self.buildingID = buildingID
        self.SwitchID = SwitchID
        self.building_config = switch_board_building(self.buildingID)
        self.intf = interface(self.building_config, self.SwitchID)
        cfg = configuration_reader(self.intf)
        self.work_q = Queue()
        self.online_reader = Process(target=cfg.run, args=(self.work_q,))
        self.online_reader.daemon = True
        self.online_reader.start()
        self.comms = communicator_physical_layer()
        self.translator = name_translator()
        self.busy_busbars = {}
        # online_reader.join()  # https://stackoverflow.com/questions/25391025/what-exactly-is-python-multiprocessing-modules-join-method-doing?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

    def run(self):
        self.logic = logic(self.comms, self.work_q, self.translator)
        new_input = False
        processed_configurations = AutoVivification()  # nothing but a dictionary

        pb = path_builder(self.intf, self.comms, self.translator)
        pm = path_matcher()
        mssgr = message_for_controller(self.intf, self.comms, self.translator)
        #try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # https://stackoverflow.com/questions/45927337/recieve-data-only-if-available-in-python-sockets
            # op_controller = controller()
            s.bind((_HOST, _PORT))
            s.listen(1)
            print("Logical Layer Listening")
            readable = [s]  # list of readable sockets.  s is readable if a client is waiting.

            while True:
                r, w, e = select.select(readable, [], [], _BEGIN_WITH)  # the 0 here is the time out, it doesn't wait anything, it keeps cheking if the first argument is ready to be red
                for rs in r:  # iterate through readable sockets - so r is a list of objects included in readable that are ready to be read - if its ready there is a call from the client
                    if rs is s:  # if one of the object ready to be red is the speified socket we are using to communicate, then we listen to it!
                        c, a = s.accept()  # this accept the first client in the queue - "c" is the socket object and "a" the ip and port object
                        print('\r{}:'.format(a), 'connected')
                        readable.append(c)  # add the connection with the client
                    else:
                        # read from a client represented by that readable object
                        data_from_API = rs.recv(1024)
                        if not data_from_API:
                            print('\r{}:'.format(rs.getpeername()), 'disconnected')
                            readable.remove(rs)
                            rs.close()
                        else:
                            system_input = pickle.loads(data_from_API)
                            system_input = self.logic.check_sources(system_input)
                            print(system_input)

                            processed_configurations = self.logic.configurations_request_analyser(processed_configurations, system_input, mssgr)

                            print('\r{}:'.format(rs.getpeername()), system_input)
                            new_input = True

                if (new_input):
                    new_input = False
                    processed_configurations = self.logic.find_suitable_setup(processed_configurations, pb)
                    processed_configurations = self.logic.actuate_suitable_setup(processed_configurations)
                    processed_configurations = self.logic.controller_starter(processed_configurations, pm, mssgr)
                    processed_configurations = self.logic.inactive_configuration_cleaner(processed_configurations)
                    print(processed_configurations)
                    #TODO send the actual controller command


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


if __name__ == "__main__":
    start_time = time.time()
    test = logical_layer("Building716", "Switch_Board_1")

    test.run()
    print("--- %s seconds ---" % (time.time() - start_time))


'''From Test Rig to Online uncomment syslab interface and related from, components_status.py, controller.py, physical_layer.py'''
'''component_status.py is meant to be disconnected from syslab too'''
