# Create two threads as follow
from controller_constant_flow import controller_constant_flow
from controller_constant_pressure import controller_constant_pressure
from multiprocessing import Process
from physical_logic import physical_logic
import pickle
import select
import socket
import sys

_MULTIPLIER = 1000000
_ACTUATE = "actuate"
_BEGIN_WITH = 0
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
        self.valves_status = {
            "Bay_4L-Busbar_2R": 0.11, "Bay_4L-Busbar_1R": 0.11, "Bay_4H-Busbar_B": 0.11, "Bay_4H-Busbar_2F": 0.11, "Bay_4H-Busbar_1F": 0.11, "Bay_4L-Busbar_B": 0.11,
            "Bay_5L-Busbar_1R": 0.11, "Bay_5L-Busbar_2R": 0.11, "Bay_5H-Busbar_B": 0.11, "Bay_5H-Busbar_1F": 0.11, "Bay_5H-Busbar_2F": 0.11, "Bay_5L-Busbar_B": 0.11,
            "Bay_6L-Busbar_1R": 0.11, "Bay_6L-Busbar_2R": 0.11, "Bay_6H-Busbar_B": 0.11, "Bay_6H-Busbar_1F": 0.11, "Bay_6H-Busbar_2F": 0.11, "Bay_6L-Busbar_B": 0.11,
            "Bay_7H-Busbar_1F": 0.11, "Bay_7H-Busbar_2F": 0.11, "Bay_7L-Busbar_1R": 0.11, "Bay_7L-Busbar_2R": 0.11,
            "Bay_8H-Busbar_1F": 0.11, "Bay_8H-Busbar_2F": 0.11, "Bay_8L-Busbar_1R": 0.11, "Bay_8L-Busbar_2R": 0.11}
        p_logic = physical_logic()
        op_controller_flow = controller_constant_flow()
        op_controller_pressure = controller_constant_pressure()
        processes = {}
        new_input = False
        #try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # https://stackoverflow.com/questions/45927337/recieve-data-only-if-available-in-python-sockets
            # op_controller = controller()
            s.bind((_HOST, _PORT))
            s.listen(1)
            print("Physical Layer Listening")
            readable = [s]  # list of readable sockets.  s is readable if a client is waiting.
            i = 0
            try:
                while True:
                    r, w, e = select.select(readable, [], [], _BEGIN_WITH)  # the 0 here is the time out, it doesn't wait anything, it keeps cheking if the first argument is ready to be red
                    for rs in r:  # iterate through readable sockets - so r is a list of objects included in readable that are ready to be read - if its ready there is a call from the client
                        if rs is s:  # is it the server - if one of the object ready to be red is the socket we are using to communicate, then we listen to it!
                            c, a = s.accept()  # this accept the first client in the queue - "c" is the socket object and "a" the ip and port object
                            #print('\r{}:'.format(a), 'connected')
                            readable.append(c)  # add the connection with the client
                        else:
                            # read from a client represented by that readable object
                            data_from_API = rs.recv(4096)
                            if not data_from_API:
                                #print('\r{}:'.format(rs.getpeername()), 'disconnected')
                                #self.killer_routine(requested_configuration, mssgr)
                                readable.remove(rs)
                                rs.close()
                            else:
                                print("Message received")
                                inputs = pickle.loads(data_from_API)
                                new_input = True
                            try:
                                if (new_input):
                                    if (inputs[_DESCRIPTION] == _CREATOR):
                                        inputs.pop(_DESCRIPTION)
                                        input_for_controller = (data_from_API, inputs["controller_name"])
                                        processes[inputs["controller_name"]] = Process(target=op_controller_flow.PID_controller, args=input_for_controller)
                                        print("New Process started")
                                        processes[inputs["controller_name"]].start()
                                        feedback = "I have created controller " + inputs["controller_name"]
                                        message_serialized = pickle.dumps(feedback)
                                        c.sendall(message_serialized)
                                        # processes[n].join()  # https://stackoverflow.com/questions/25391025/what-exactly-is-python-multiprocessing-modules-join-method-doing?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

                                    elif (inputs[_DESCRIPTION] == _KILLER):
                                        inputs.pop(_DESCRIPTION)
                                        print("Mi è stato detto di ucciderti, ", inputs["controller_name"])
                                        processes[inputs["controller_name"]].terminate()
                                        print("process terminated", inputs["controller_name"])
                                        feedback = "I have killed controller " + inputs["controller_name"]
                                        message_serialized = pickle.dumps(feedback)
                                        c.sendall(message_serialized)

                                    elif (inputs[_DESCRIPTION] == _VALVE_STATUS):
                                        #print(inputs)
                                        inputs.pop(_DESCRIPTION)
                                        #valves_for_logical_layer = p_logic.get_valves_status(inputs)
                                        valves_for_logical_layer = p_logic.get_valves_simulated_status(inputs)
                                        message_serialized = pickle.dumps(valves_for_logical_layer)
                                        #print(valves_for_logical_layer)
                                        c.sendall(message_serialized)

                                    elif (inputs[_DESCRIPTION] == _ACTUATE):
                                        '''Here you should firs check if actuation is necessary - not really at the end of the day because it will confirm a setpoint'''
                                        print(inputs)
                                        inputs.pop(_DESCRIPTION)
                                        #complete = p_logic.set_hydraulic_circuit(inputs)
                                        complete = p_logic.set_hydraulic_simulated_circuit(inputs)
                                        message_serialized = pickle.dumps(complete)
                                        #print(self.valves_status)
                                        c.sendall(message_serialized)

                                    new_input = False
                            except(KeyboardInterrupt, SystemExit, Exception):
                                        c.close()
                                        print("Now has stopped")
                                        s.shutdown(socket.SHUT_RDWR)
                                        s.close()
                                        if processes.keys():
                                            for process in processes.items():
                                                process.terminate()
                                                print("Stopped Process {0}".format(process))
                                        sys.exit()
            except(KeyboardInterrupt, SystemExit, Exception):
                if s:
                    #s.shutdown(socket.SHUT_RDWR)
                    s.close()
                sys.exit()

        '''except (KeyboardInterrupt, Exception, SystemExit):
            s.shutdown(socket.SHUT_RDWR)  # this is that close both end of connection  alternative are SHUT_RD to avoid receiving and SHUT_WR to avoid the other to send
            s.close()
            sys.exit()'''


if __name__ == "__main__":
    test = physical_layer()


# the circulator is selected automatically - what about the operation mode?
# where actuator is specified?
# define use cases with identificative name for look up table as the constants for the controller are hardcoded! shall it be a text config file?
# how flow is controlled in pumps % ?
