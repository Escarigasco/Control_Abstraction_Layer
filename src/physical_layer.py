# Create two threads as follow
import _thread
from controller import controller
import pickle
import socket

HOST = 'localhost'                 # Symbolic name meaning all available interfaces
PORT = 50008              # Arbitrary non-privileged port
op_controller = controller()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                input_for_controller = pickle.loads(data)
                try:
                    _thread.start_new_thread(op_controller.PID_controller, input_for_controller)
                except:
                    print("Error: unable to start thread")
                if not data:
                    break
                # conn.sendall(data)
    conn.close()
