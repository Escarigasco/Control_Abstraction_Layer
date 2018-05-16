from configuration_reader import configuration_reader
from interface import interface
from matplotlib import pyplot as plt
from message_for_controller import message_for_controller
from object_tracker import object_tracker
from path_builder import path_builder
from switch_board_building import switch_board_building
import time
import threading
import queue
from multiprocessing import Process, Pipe, Queue
import sys

_BOOSTER_NAME = "Source_1BH4"
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

        # self.work_q = queue.Queue()     # first create your "work object"
        # self.q_lock = threading.Lock()
        # cfg = configuration_reader(self.intf, self.work_q, self.q_lock)  # after instantiate like this your Thread

        # cfg.setDaemon(True)  # this is to join the thread with the main
        # cfg.start()

        cfg = configuration_reader(self.intf)
        self.main_end, self.cfg_end = Pipe()
        self.work_q = Queue()
        #self.online_reader = Process(target=cfg.run, args=(self.cfg_end,))
        self.online_reader = Process(target=cfg.run, args=(self.work_q,))
        self.online_reader.daemon = True
        self.online_reader.start()
        #self.online_reader.join()
        # online_reader.join()  # https://stackoverflow.com/questions/25391025/what-exactly-is-python-multiprocessing-modules-join-method-doing?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

    def run(self, sinks, sources, boosted, parameters, setpoints):
        self.used_sinks = sinks
        self.used_sources = sources
        self.boosted = boosted
        self.parameters = parameters
        self.setpoints = setpoints
        self.check_sources()
        self.process_started = False
        system_input = {"sinks": self.used_sinks, "sources": self.used_sources, "boosted": self.boosted,
                        "parameters": self.parameters, "setpoints": self.setpoints}
        pb = path_builder(self.intf)
        mssgr = message_for_controller()
        # plt.close('all')
        # builder = rule_engine(self.intf)
        # cfg = configuration_reader(self.intf)
        # online_configuration = cfg.run()

        while True:
            try:
                #if self.main_end.recv():
                if not self.work_q.empty():
                    # plt.close()
                    plt.close('all')
                    #online_configuration = self.main_end.recv()
                    online_configuration = self.work_q.get()
                    unique = pb.run(system_input, online_configuration)
                    print(unique)
                    print("tu che sei diversooooooooooooooooooooooooooooooooooooooo")

                    if (unique is not None):  # if there is a matching between user input and online configuration
                        if (not self.process_started):
                            print("how many messagessssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
                            mssgr.run(unique, system_input, self.intf)
                            self.process_started = True
                    else:
                        if (self.process_started):
                            print("when I am hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee?")
                            mssgr.kill(system_input)
                            self.process_started = False
            except KeyboardInterrupt:
                self.online_reader.terminate()
                sys.exit()
                # break
            '''with self.q_lock:
                if not self.work_q.empty():
                        online_configuration = self.work_q.get()
                        pb = path_builder(self.intf)
                        unique = pb.run(system_input, online_configuration)
                        if unique is None:
                            return
                        mssgr = message_for_controller()
                        message = mssgr.run(unique, system_input, self.intf)
                        break'''

    def check_sources(self):
        for source in self.used_sources:
            if (source == _BOOSTER_NAME):
                self.boosted = 'N'


if __name__ == "__main__":
    start_time = time.time()
    test = logical_layer("Building716", "Switch_Board_1")
    sinks = ["Sink_1H7"]
    sources = ["Source_1BH4"]
    boosted = "N"
    #sensors = ["Sensor_1E7"]
    parameters = "Energy"
    setpoints = 20
    #controlled_device = "Pump_1H7"
    #controller_name = "Constant_Energy_Pump_Actuating"

    test.run(sinks, sources, boosted, parameters, setpoints)
    print("--- %s seconds ---" % (time.time() - start_time))
