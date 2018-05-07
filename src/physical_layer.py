# Create two threads as follow
import _thread
from controller import controller
from multiprocessing import Process
import socket
import sys


HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50008              # Arbitrary non-privileged port
op_controller = controller()
n = 0
threads = []
processes = []
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
                print("Control objective received")
                input_for_controller = (data_from_logical_layer, n)
                # print(input_for_controller)
                # threads.append(_thread.start_new_thread(op_controller.PID_controller, input_for_controller))
                processes.append(Process(target=op_controller.PID_controller, args=input_for_controller))
                print("New Process started")
                processes[n].start()
                # processes[n].join()
                n = n + 1

            except (KeyboardInterrupt, SystemExit, Exception):
                '''for thread in threads:
                    thread.exit()
                    print("Stopped Thread {0}".format(thread))'''
                for process in processes:
                    process.terminate()
                    print("Stopped Process {0}".format(process))

                conn.close()
                print("Now has stopped")
                sys.exit()
    conn.close()

# the circulator is selected automatically - what about the operation mode?
# where actuator is specified?
# define use cases with identificative name for look up table as the constants for the controller are hardcoded! shall it be a text config file?
# how flow is controlled in pumps % ?
