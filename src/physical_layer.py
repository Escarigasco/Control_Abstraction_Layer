# Create two threads as follow
from controller_constant_flow import controller_constant_flow
from controller_constant_pressure import controller_constant_pressure
from multiprocessing import Process
import pickle
import random
import socket
import sys
import syslab
import syslab.core.datatypes.CompositeMeasurement as CM
import time

_MULTIPLIER = 1000000
_ACTUATE = "actuate"
_VALVE_STATUS = "valve_status"
_VALVES = 'Valves_active'
_BUILDING_NAME = "716-h1"
_NEG = "N"
_DESCRIPTION = "description"
_KILLER = "killer"
_CREATOR = "creator"
_HOST = 'localhost'                 # Symbolic name meaning all available interfaces
_PORT = 2000             # Arbitrary non-privileged port
_TURN_ME_ON = 1


class physical_layer(object):

    def __init__(self):
        op_controller_flow = controller_constant_flow()
        op_controller_pressure = controller_constant_pressure()
        processes = {}
        #interface = syslab.HeatSwitchBoard(_BUILDING_NAME)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # op_controller = controller()
                s.bind((_HOST, _PORT))
                while True:
                    print("Physical Layer Listening")
                    s.listen(1)
                    conn, addr = s.accept()
                    with conn:
                            try:
                                print('Connected by', addr)

                                data_from_logical_layer = conn.recv(2048)
                                print("Message received")
                                inputs = pickle.loads(data_from_logical_layer)

                                if (inputs[_DESCRIPTION] == _CREATOR):
                                    inputs.pop(_DESCRIPTION)
                                    input_for_controller = (data_from_logical_layer, inputs["controller_name"])
                                    processes[inputs["controller_name"]] = Process(target=op_controller_flow.PID_controller, args=input_for_controller)
                                    print("New Process started")
                                    processes[inputs["controller_name"]].start()
                                    feedback = "I have created controller " + inputs["controller_name"]
                                    message_serialized = pickle.dumps(feedback)
                                    conn.sendall(message_serialized)
                                    # processes[n].join()  # https://stackoverflow.com/questions/25391025/what-exactly-is-python-multiprocessing-modules-join-method-doing?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

                                elif (inputs[_DESCRIPTION] == _KILLER):
                                    inputs.pop(_DESCRIPTION)
                                    print("Mi è stato detto di ucciderti, ", inputs["controller_name"])
                                    processes[inputs["controller_name"]].terminate()
                                    print("process terminated", inputs["controller_name"])
                                    feedback = "I have killed controller " + inputs["controller_name"]
                                    message_serialized = pickle.dumps(feedback)
                                    conn.sendall(message_serialized)

                                elif (inputs[_DESCRIPTION] == _VALVE_STATUS):
                                    print(inputs)
                                    inputs.pop(_DESCRIPTION)
                                    #valves_for_logical_layer = self.get_valves_status(inputs, interface)
                                    valves_for_logical_layer = self.get_valves_simulated_status(inputs)
                                    message_serialized = pickle.dumps(valves_for_logical_layer)
                                    print(valves_for_logical_layer)
                                    conn.sendall(message_serialized)

                                elif (inputs[_DESCRIPTION] == _ACTUATE):
                                    print(inputs)
                                    inputs.pop(_DESCRIPTION)
                                    #complete = self.set_hydraulic_circuit(inputs, interface)
                                    complete = self.set_hydraulic_simulated_circuit(inputs)
                                    message_serialized = pickle.dumps(complete)
                                    print(complete)
                                    conn.sendall(message_serialized)

                            except(KeyboardInterrupt, SystemExit, Exception):
                                        conn.close()
                                        print("Now has stopped")
                                        s.shutdown(socket.SHUT_RDWR)
                                        s.close()
                                        for process in processes.items():
                                            process.terminate()
                                            print("Stopped Process {0}".format(process))
                                        sys.exit()

        except (KeyboardInterrupt, Exception, SystemExit):
            s.shutdown(socket.SHUT_RDWR)  # this is that close both end of connection  alternative are SHUT_RD to avoid receiving and SHUT_WR to avoid the other to send
            s.close()
            sys.exit()

    def get_valves_status(self, valves_for_physical_layer, interface):
        valves_for_logical_layer = {}
        for valve in valves_for_physical_layer.keys():
            opening = interface.getValvePosition(valve)
            print(valve, opening.value)
            valves_for_logical_layer[valves_for_physical_layer[valve]] = opening.value
        return valves_for_logical_layer

    def get_valves_simulated_status(self, valves_for_physical_layer):
        min_operating = 0
        max_operating = 1
        valves_for_logical_layer = {}
        for valve in valves_for_physical_layer.keys():
            print(valve)
            valves_for_logical_layer[valve] = random.uniform(min_operating, max_operating)
        return valves_for_logical_layer

    def set_hydraulic_circuit(self, inputs, interface):
        valves = inputs[_VALVES]
        valves_status = {}
        opening_threshold = 3.6
        CompositMess = CM(_TURN_ME_ON, time.time() * _MULTIPLIER)
        complete = False
        for valve in valves:
            interface.setValvePosition(valve, CompositMess)
        while not complete:
            for valve in valves:
                valves_status[valve] = interface.getValvePosition(valve, CompositMess).value
            time.sleep(2)
            if (sum(opening for opening in valves_status.values()) >= opening_threshold):
                complete = True
        return complete

    def set_hydraulic_simulated_circuit(self, inputs):
        valves = inputs[_VALVES]
        valves_status = {}
        opening_threshold = 3.6
        complete = False
        for valve in valves:
            valves_status[valve] = 1
        time.sleep(20)
        print(sum(opening for opening in valves_status.values()))
        if (sum(opening for opening in valves_status.values()) >= opening_threshold):
                complete = True
        return complete


if __name__ == "__main__":
    test = physical_layer()


# the circulator is selected automatically - what about the operation mode?
# where actuator is specified?
# define use cases with identificative name for look up table as the constants for the controller are hardcoded! shall it be a text config file?
# how flow is controlled in pumps % ?
