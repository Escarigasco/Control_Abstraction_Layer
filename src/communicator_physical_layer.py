import pickle
import socket
import sys
_NEG = "N"
_HOST = 'localhost'    # The remote host
_PORT = 2000


class communicator_physical_layer(object):

    def send(self, valves_for_physical_layer):
        valves_for_logical_layer = {}
        message_serialized = pickle.dumps(valves_for_physical_layer)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((_HOST, _PORT))
                s.sendall(message_serialized)
                while not valves_for_logical_layer:
                    valves_for_logical_layer = s.recv(2048)
                    print("Ok, I got the shit")
                s.close()
                valves_for_logical_layer = pickle.loads(valves_for_logical_layer)
            except Exception:
                print("sono l eccezione")
                pass
        return valves_for_logical_layer
