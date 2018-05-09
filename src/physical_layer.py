# Create two threads as follow
import _thread
from controller import controller
from multiprocessing import Process
import socket
import sys
import pickle
_NEG = "N"

HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50008              # Arbitrary non-privileged port
op_controller = controller()
n = 0
threads = []
processes = {}
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # op_controller = controller()
    s.bind((HOST, PORT))
    while True:
        print("Physical Layer Listening")
        try:
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                try:
                    print('Connected by', addr)

                    data_from_logical_layer = conn.recv(1024)
                    print("Control objective received")
                    inputs = pickle.loads(data_from_logical_layer)
                    if (inputs["kill"] == _NEG):
                        input_for_controller = (data_from_logical_layer, inputs["controller_name"])
                        # print(input_for_controller)
                        # threads.append(_thread.start_new_thread(op_controller.PID_controller, input_for_controller))
                        processes[inputs["controller_name"]] = Process(target=op_controller.PID_controller, args=input_for_controller)
                        print("New Process started")
                        processes[inputs["controller_name"]].start()
                        # processes[n].join()  # https://stackoverflow.com/questions/25391025/what-exactly-is-python-multiprocessing-modules-join-method-doing?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa

                    else:
                        processes[inputs["controller_name"]].terminate()
                        print("process terminated", inputs["controller_name"])

                except(KeyboardInterrupt, SystemExit, Exception):
                            for process in processes.items():
                                process.terminate()
                                print("Stopped Process {0}".format(process))
                            conn.close()
                            print("Now has stopped")
                            s.shutdown(socket.SHUT_RDWR)
                            s.close()
                            sys.exit()
                            
        except KeyboardInterrupt:
            s.shutdown(socket.SHUT_RDWR) # this is that close both end of connection  alternative are SHUT_RD to avoid receiving and SHUT_WR to avoid the other to send
            s.close()
            sys.exit()

# the circulator is selected automatically - what about the operation mode?
# where actuator is specified?
# define use cases with identificative name for look up table as the constants for the controller are hardcoded! shall it be a text config file?
# how flow is controlled in pumps % ?
