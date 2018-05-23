from configuration_reader import configuration_reader
from interface import interface
from matplotlib import pyplot as plt
from message_for_controller import message_for_controller
from object_tracker import object_tracker
from path_builder import path_builder
from switch_board_building import switch_board_building
from multiprocessing import Process, Pipe, Queue
import pickle
import select
import socket
import sys
import time


_BOOSTER_NAME = "Source_1BH4"
_HOST = 'localhost'                 # Symbolic name meaning all available interfaces
_PORT = 50010              # Arbitrary non-privileged port
_BEGIN_WITH = 0

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
        # online_reader.join()  # https://stackoverflow.com/questions/25391025/what-exactly-is-python-multiprocessing-modules-join-method-doing?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

    def run(self, sinks, sources, boosted, parameters, setpoints):
        self.used_sinks = sinks
        self.used_sources = sources
        self.boosted = boosted
        self.parameters = parameters
        self.setpoints = setpoints

        self.process_started = False
        #system_input = {"sinks": self.used_sinks, "sources": self.used_sources, "boosted": self.boosted,
                        #"parameters": self.parameters, "setpoints": self.setpoints}
        pb = path_builder(self.intf)
        mssgr = message_for_controller()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # op_controller = controller()
            s.bind((_HOST, _PORT))
            s.listen(1)
            print("Physical Layer Listening")
            readable = [s] # list of readable sockets.  s is readable if a client is waiting.

            while True:
                r, w, e = select.select(readable, [], [], _BEGIN_WITH)
                for rs in r:  # iterate through readable sockets
                    if rs is s:  # is it the server
                        c, a = s.accept()
                        print('\r{}:'.format(a), 'connected')
                        readable.append(c)  # add the client
                    else:
                        # read from a client
                        data_from_API = rs.recv(1024)
                        if not data_from_API:
                            print('\r{}:'.format(rs.getpeername()), 'disconnected')
                            readable.remove(rs)
                            rs.close()
                        else:
                            system_input = pickle.loads(data_from_API)
                            system_input = self.check_sources(system_input)
                            print('\r{}:'.format(rs.getpeername()), system_input)
                try:
                    if not self.work_q.empty():
                        print("I am checking again the matches because something changed in the online configuration")
                        # plt.close()
                        plt.close('all')
                        #online_configuration = self.main_end.recv()
                        online_configuration = self.work_q.get()
                        unique = pb.run(system_input, online_configuration)

                        if (unique is not None):  # if there is a matching between user input and online configuration
                            if (not self.process_started):
                                print("Preparing Message")
                                mssgr.run(unique, system_input, self.intf)
                                self.process_started = True
                        else:
                            if (self.process_started):
                                print("Kill started process")
                                mssgr.kill(system_input)
                                self.process_started = False
                except Exception:
                    print("No user inputs defined")
                    pass

                            #except KeyboardInterrupt:
                            #    self.online_reader.terminate()
                            #    sys.exit()

                    #except(KeyboardInterrupt, SystemExit, Exception):
                    #            conn.close()
                    #            print("Logical Layer Isolated")
                    #            s.shutdown(socket.SHUT_RDWR) # this is that close both end of connection  alternative are SHUT_RD to avoid receiving and SHUT_WR to avoid the other to send
                    #            s.close()
                    #            sys.exit()

    def check_sources(self, system_input):
        for source in system_input["sources"]:
            if (source == _BOOSTER_NAME):
                system_input["boosted"] = 'N'
        return system_input

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


'''From Test Rig to Online uncomment interface from configuration_reader.py, components_status.py, controller.py'''
