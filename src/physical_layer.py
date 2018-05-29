# Create two threads as follow
from controller_constant_flow import controller_constant_flow
from controller_constant_pressure import controller_constant_pressure
from multiprocessing import Process
import pickle
import socket
import sys
import syslab

_BUILDING_NAME = "716-h1"
_NEG = "N"
_VALVE_STATUS = "valve_status"
_DESCRIPTION = "description"
_KILLER = "killer"
_CREATOR = "creator"
_HOST = 'localhost'                 # Symbolic name meaning all available interfaces
_PORT = 2000             # Arbitrary non-privileged port


class physical_layer(object):

    def __init__(self):
        op_controller_flow = controller_constant_flow()
        op_controller_pressure = controller_constant_pressure()
        processes = {}
        interface = syslab.HeatSwitchBoard(_BUILDING_NAME)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # op_controller = controller()
            s.bind((_HOST, _PORT))
            while True:
                print("Physical Layer Listening")
                try:
                    s.listen(1)
                    conn, addr = s.accept()
                    with conn:
                            try:
                                print('Connected by', addr)

                                data_from_logical_layer = conn.recv(2048)
                                print("Message received")
                                inputs = pickle.loads(data_from_logical_layer)

                                if (inputs[_DESCRIPTION] == _CREATOR):
                                    input_for_controller = (data_from_logical_layer, inputs["controller_name"])

                                    processes[inputs["controller_name"]] = Process(target=op_controller_flow.PID_controller, args=input_for_controller)
                                    print("New Process started")
                                    processes[inputs["controller_name"]].start()
                                    # processes[n].join()  # https://stackoverflow.com/questions/25391025/what-exactly-is-python-multiprocessing-modules-join-method-doing?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

                                elif (inputs[_DESCRIPTION] == _KILLER):
                                    print("Mi è stato detto di ucciderti, ", inputs["controller_name"])
                                    processes[inputs["controller_name"]].terminate()
                                    print("process terminated", inputs["controller_name"])

                                elif (inputs[_DESCRIPTION] == _VALVE_STATUS):
                                    print(inputs)
                                    inputs.pop(_DESCRIPTION)
                                    valves_for_logical_layer = self.get_valves_status(inputs, interface)
                                    message_serialized = pickle.dumps(valves_for_logical_layer)
                                    print(valves_for_logical_layer)
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

if __name__ == "__main__":
    test = physical_layer()


# the circulator is selected automatically - what about the operation mode?
# where actuator is specified?
# define use cases with identificative name for look up table as the constants for the controller are hardcoded! shall it be a text config file?
# how flow is controlled in pumps % ?
