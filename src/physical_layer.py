#!~/Desktop/SwitchBoard/SwitchBoard/bin/activate python

from controller_constant_flow import controller_constant_flow
from controller_constant_pressure import controller_constant_pressure
from multiprocessing import Process
from multiprocessing import Queue
from physical_layer_online_reader import physical_layer_online_reader
from physical_logic import physical_logic
import pickle
import select
import socket
import signal
import sys
import time

_MULTIPLIER = 1000000
_ACTUATE = "actuate"
_BEGIN_WITH = 0
_FIRST_OF_CLASS = 1
_VALVE_STATUS = "valve_status"
_PUMP_STATUS = "pump_status"
_VALVES = 'Valves_active'
_BUILDING_NAME = "716-h1"
_NEG = "N"
_DESCRIPTION = "description"
_KILLER = "killer"
_CREATOR = "creator"
_HOST = 'localhost'                 # Symbolic name meaning all available interfaces
_PORT = 2000             # Arbitrary non-privileged port
_TURN_ME_ON = 1
_SETPOINT = "setpoints"
_CONTROLLER_NAME = "controller_name"
_SHUTTER = "shutter"
_TEST_COMMS = "4x4?"
_ANSWER_TO_TEST_COMMS = "16"
_TIME_OUT = 10
_RESET = 0
_CIRCULATOR_MODE = "circulator_mode"
_COMPONENTS = "components"
_INIT = "init"


class physical_layer(object):

    def __init__(self):
        self.work_q = Queue()
        physical_reader = physical_layer_online_reader()
        self.physical_reader = Process(target=physical_reader.run, args=(self.work_q,))
        self.physical_reader.daemon = True
        self.physical_reader.start()

        self.p_logic = physical_logic()
        self.op_controller_flow = controller_constant_flow()
        self.op_controller_pressure = controller_constant_pressure()
        self.processes = {}
        self.queues = {}
        new_input = False
        self.loss_of_comms = False
        self.methods = {_TEST_COMMS: self.test_comms, _CREATOR: self.process_create, _SETPOINT: self.change_setpoint,
                        _KILLER: self.kill_process, _VALVE_STATUS: self.check_valves, _PUMP_STATUS: self.check_pumps,
                        _ACTUATE: self.actuate, _SHUTTER: self.pumps_shutter, _INIT: self.initialization}

        #signal.signal(signal.SIGALRM, self.time_out_handler)
        #signal.alarm(_TIME_OUT)

        #try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # https://stackoverflow.com/questions/45927337/recieve-data-only-if-available-in-python-sockets
            # op_controller = controller()

            s.bind((_HOST, _PORT))
            s.listen(2)
            print("Physical Layer Listening")
            readable = [s]  # list of readable sockets.  s is readable if a client is waiting.
            i = 0
            while True:
                #time.sleep(1)
                time.sleep(0.2)
                #print(time.time() - start_time)
                r, w, e = select.select(readable, [], [], _BEGIN_WITH)  # the 0 here is the time out, it doesn't wait anything, it keeps cheking if the first argument is ready to be red
                for rs in r:  # iterate through readable sockets - so r is a list of objects included in readable that are ready to be read - if its ready there is a call from the client
                    if rs is s:  # is it the server - if one of the object ready to be red is the socket we are using to communicate, then we listen to it!
                        c, a = s.accept()  # this accept the first client in the queue - "c" is the socket object and "a" the ip and port object
                        #print('\r{}:'.format(a), 'connected')
                        readable.append(c)  # add the connection with the client
                    else:
                        # read from a client represented by that readable object

                        self.data_from_API = rs.recv(4096)
                        if not self.data_from_API:
                            #print('\r{}:'.format(rs.getpeername()), 'disconnected')
                            #self.killer_routine(requested_configuration, mssgr)
                            readable.remove(rs)
                            rs.close()
                        else:
                            #print("Message received")
                            inputs = pickle.loads(self.data_from_API)
                            new_input = True
                        try:
                            if (new_input):
                                #print(inputs)

                                method = self.methods.get(inputs[_DESCRIPTION], lambda: None)
                                if method:
                                    method(inputs, c)

                                new_input = False

                        except(KeyboardInterrupt, SystemExit, Exception):
                                    c.close()
                                    print("Now has stopped")
                                    s.shutdown(socket.SHUT_RDWR)
                                    s.close()
                                    if self.processes.keys():
                                        for process in self.processes.items():
                                            process.terminate()
                                            print("Stopped Process {0}".format(process))
                                    sys.exit()

                #if self.loss_of_comms:
                #    self.connection_lost()
                #    self.loss_of_comms = False

        #except(KeyboardInterrupt, SystemExit, Exception):
        #    if s:
                #s.shutdown(socket.SHUT_RDWR)
        #        s.close()
        #    print("Physical Layer is closing")
        #    sys.exit()

    #def connection_lost(self):
    #    signal.alarm(_RESET)
    #    print("If there are active self.processes I will terminate them")
    #    processes_names = []
    #    if self.processes.keys():
    #        for name in self.processes.keys():
    #            processes_names.append(name)
    #        for name in processes_names:
    #            self.processes[name].terminate()
    #            print("Stopped Process {0}".format(name))
    #            self.processes.pop(name)
    #    signal.alarm(_TIME_OUT)

    #def time_out_handler(self, signum, frame):
    #    self.loss_of_comms = True

    def initialization(self, inputs, c):
            inputs.pop(_DESCRIPTION)
            processes_names = []
            #complete = self.p_logic.set_hydraulic_circuit(inputs)
            if self.processes:
                for name in self.processes.keys():
                    processes_names.append(name)
                print(self.processes.keys())
                for process in processes_names:
                    self.processes[process].terminate()
                    self.processes.pop(process)
                    print("process terminated", process)

            complete = self.p_logic.initialization(inputs)
            self.work_q.put(complete[_FIRST_OF_CLASS])
            message_serialized = pickle.dumps(complete[_BEGIN_WITH])
            c.sendall(message_serialized)

    def test_comms(self, inputs, c):
        #signal.alarm(_RESET)
        print(inputs[_DESCRIPTION])
        inputs[_DESCRIPTION] = _ANSWER_TO_TEST_COMMS
        message_serialized = pickle.dumps(inputs)
        c.sendall(message_serialized)
        #signal.alarm(_TIME_OUT)

    def process_create(self, inputs, c):
        inputs.pop(_DESCRIPTION)
        name = inputs[_CONTROLLER_NAME]
        if name not in self.processes.keys():
            self.queues[inputs[_CONTROLLER_NAME]] = Queue()
            input_for_controller = (self.data_from_API, inputs[_CONTROLLER_NAME], self.queues[inputs[_CONTROLLER_NAME]])

            if (inputs[_CIRCULATOR_MODE] == '4'):
                self.processes[inputs[_CONTROLLER_NAME]] = Process(target=self.op_controller_flow.PID_controller, args=input_for_controller)
            else:
                print("this is a constant pressure controller")
                self.processes[inputs[_CONTROLLER_NAME]] = Process(target=self.op_controller_pressure.PID_controller, args=input_for_controller)

            print("New Process started")
            self.processes[inputs[_CONTROLLER_NAME]].start()
            feedback = "I have created controller " + inputs[_CONTROLLER_NAME]
            message_serialized = pickle.dumps(feedback)
            c.sendall(message_serialized)
        else:
            print("Process {0} is already running".format(name))
            feedback = "Controller was there already - " + inputs[_CONTROLLER_NAME]
            message_serialized = pickle.dumps(feedback)
            c.sendall(message_serialized)
            pass
        # self.processes[n].join()  # https://stackoverflow.com/questions/25391025/what-exactly-is-python-multiprocessing-modules-join-method-doing?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

    def change_setpoint(self, inputs, c):
        inputs.pop(_DESCRIPTION)
        print("Mi è stato detto di cambiarti setpoint Mr., ", inputs[_CONTROLLER_NAME])
        self.queues[inputs[_CONTROLLER_NAME]].put(inputs[_SETPOINT])
        feedback = "I have changed setpoint to controller {0}, the new setpoint is {1}".format(inputs[_CONTROLLER_NAME], inputs[_SETPOINT])
        message_serialized = pickle.dumps(feedback)
        c.sendall(message_serialized)

    def kill_process(self, inputs, c):
        inputs.pop(_DESCRIPTION)
        name = inputs[_CONTROLLER_NAME]
        killed = False
        if name in self.processes.keys():
            print("Mi è stato detto di ucciderti, ", inputs[_CONTROLLER_NAME])
            while self.processes[inputs[_CONTROLLER_NAME]].is_alive():
                time.sleep(0.1)
                self.processes[inputs[_CONTROLLER_NAME]].terminate()
            self.processes.pop(inputs[_CONTROLLER_NAME])
            print("process terminated", inputs[_CONTROLLER_NAME])
            feedback = "I have killed controller " + inputs[_CONTROLLER_NAME]
            message_serialized = pickle.dumps(feedback)
            c.sendall(message_serialized)
        else:
            print("There is no one here called ", name)
            feedback = "There is no one here called " + inputs[_CONTROLLER_NAME]
            message_serialized = pickle.dumps(feedback)
            c.sendall(message_serialized)

    def check_valves(self, inputs, c):
        #print(inputs)
        inputs.pop(_DESCRIPTION)
        #valves_for_logical_layer = self.p_logic.get_valves_status(inputs)
        valves_for_logical_layer = self.p_logic.get_valves_simulated_status(inputs)
        message_serialized = pickle.dumps(valves_for_logical_layer)
        #print(valves_for_logical_layer)
        c.sendall(message_serialized)

    def check_pumps(self, inputs, c):
        #print(inputs)
        inputs.pop(_DESCRIPTION)
        #pumps_for_logical_layer = self.p_logic.get_pumps_status(inputs)
        pumps_for_logical_layer = self.p_logic.get_pumps_simulated_status(inputs)
        message_serialized = pickle.dumps(pumps_for_logical_layer)
        #print(valves_for_logical_layer)
        c.sendall(message_serialized)

    '''if you want to move to the simulator, you have to uncomment all the below'''
    def actuate(self, inputs, c):
        '''Here you should firs check if actuation is necessary - not really at the end of the day because it will confirm a setpoint and it's not a big issue'''
        inputs.pop(_DESCRIPTION)
        #complete = self.p_logic.set_hydraulic_circuit(inputs)
        complete = self.p_logic.set_hydraulic_simulated_circuit(inputs)
        self.work_q.put(complete[_FIRST_OF_CLASS])
        message_serialized = pickle.dumps(complete[_BEGIN_WITH])
        #message_serialized = pickle.dumps(complete)
        c.sendall(message_serialized)

    def pumps_shutter(self, inputs, c):
        '''Shut the pumps'''
        print(inputs)
        inputs.pop(_DESCRIPTION)
        #complete = self.p_logic.set_hydraulic_circuit(inputs)
        complete = self.p_logic.shut_pumps(inputs)
        message_serialized = pickle.dumps(complete)
        c.sendall(message_serialized)


if __name__ == "__main__":
    test = physical_layer()

# the circulator is selected automatically - what about the operation mode?
# where actuator is specified?
# define use cases with identificative name for look up table as the constants for the controller are hardcoded! shall it be a text config file?
# how flow is controlled in pumps % ?
