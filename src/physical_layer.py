# Create two threads as follow
import _thread
from controller import controller
import socket
import sys
# import pickle


HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50008              # Arbitrary non-privileged port
op_controller = controller()
n = 0
threads = []
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # op_controller = controller()
    s.bind((HOST, PORT))
    while True:
        print("Physical Layer Listening")
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            try:
                print('Connected by', addr)

                data_from_logical_layer = conn.recv(1024)
                input_for_controller = (data_from_logical_layer, n)
                # print(input_for_controller)
                threads.append(_thread.start_new_thread(op_controller.PID_controller, input_for_controller))
                n = n + 1

            except (KeyboardInterrupt, SystemExit, Exception):
                for thread in threads:
                    _thread.exit()
                    print("Stopped Thread {0}".format(thread))
                conn.close()
                print("Now has stopped")
                sys.exit()
    conn.close()

# one error is the change of port







# where actuator is specified
# defined use case with identificative name for look up table
# shall it be a text config file?
