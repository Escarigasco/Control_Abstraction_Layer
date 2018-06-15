import pickle
import socket
import sys
import time
_NEG = "N"
_HOST = 'localhost'    # The remote host
_PORT = 2000


class communicator_physical_layer(object):

    def send(self, message_to_send):
        message_received = {}
        message_serialized = pickle.dumps(message_to_send)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((_HOST, _PORT))
                s.sendall(message_serialized)
                while not message_received:
                    #print("I am stucked here")
                    #TODO timeout
                    message_received = s.recv(4096)
                s.close()
                #print("Message received")
                message_received = pickle.loads(message_received)
            except Exception:
                print("Messaged not received yet")
                pass
        return message_received
