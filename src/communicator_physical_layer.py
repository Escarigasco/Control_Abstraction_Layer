import pickle
import socket
import sys
import time
_NEG = "N"
_HOST = 'localhost'    # The remote host
_PORT = 2000
_TIME_OUT = 100


class communicator_physical_layer(object):

    def send(self, message_to_send):
        message_received = {}
        message_serialized = pickle.dumps(message_to_send)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((_HOST, _PORT))
                s.sendall(message_serialized)
                start_time = time.time()
                stop_clock = time.time() - start_time
                while ((not message_received) & (stop_clock < _TIME_OUT)):  # this is a routine in the really unlikely case the PL crashes after the call for online config
                    message_received = s.recv(4096)
                    stop_clock = time.time() - start_time
                s.close()
                message_received = pickle.loads(message_received)
            except (Exception, KeyboardInterrupt):
                try:
                    s.close()
                except Exception:
                    pass
                print("Messaged not received yet")
                pass
        return message_received
