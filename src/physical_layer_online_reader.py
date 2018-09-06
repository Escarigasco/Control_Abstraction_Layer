# Create two threads as follow
from physical_logic import physical_logic
import pickle
import select
import socket
import sys
import time


_BEGIN_WITH = 0
_DESCRIPTION = "description"
_HOST = 'localhost'                 # Symbolic name meaning all available interfaces
_PORT = 20000             # Arbitrary non-privileged port


class physical_layer_online_reader(object):

    def run(self, queue):
        self.queue = queue
        self.p_logic = physical_logic()
        new_input = False

        #try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # https://stackoverflow.com/questions/45927337/recieve-data-only-if-available-in-python-sockets
            # op_controller = controller()
            s.bind((_HOST, _PORT))
            s.listen(2)
            print("Physical_Layer_Online_Reader Listening")
            readable = [s]  # list of readable sockets.  s is readable if a client is waiting.
            while True:
                time.sleep(0.2)
                r, w, e = select.select(readable, [], [], _BEGIN_WITH)  # the 0 here is the time out, it doesn't wait anything, it keeps cheking if the first argument is ready to be red
                for rs in r:  # iterate through readable sockets - so r is a list of objects included in readable that are ready to be read - if its ready there is a call from the client
                    if rs is s:  # is it the server - if one of the object ready to be red is the socket we are using to communicate, then we listen to it!
                        c, a = s.accept()  # this accept the first client in the queue - "c" is the socket object and "a" the ip and port object
                        #print('\r{}:'.format(a), 'connected')
                        readable.append(c)  # add the connection with the client
                    else:
                        # read from a client represented by that readable object

                        self.data_from_API = rs.recv(4096)
                        if not self.data_from_API:
                            readable.remove(rs)
                            rs.close()
                        else:
                            inputs = pickle.loads(self.data_from_API)
                            new_input = True
                            #print("request received")

                        try:
                            if not self.queue.empty():
                                self.p_logic.update_valves(self.queue.get())
                            if (new_input):
                                #print(inputs)
                                self.check_valves(inputs, c)

                                new_input = False

                        except(KeyboardInterrupt, SystemExit, Exception):
                                c.close()
                                print("Now has stopped")
                                s.shutdown(socket.SHUT_RDWR)
                                s.close()
                                if self.processes.keys():
                                    for process in self.processes.items():
                                        process.terminate()
                                        print("Stopped Process {0}".format(process))
                                sys.exit()

        #except(KeyboardInterrupt, SystemExit, Exception):
        #    if s:
                #s.shutdown(socket.SHUT_RDWR)
        #        s.close()
        #    print("Physical Layer is closing")
        #    sys.exit()

    def check_valves(self, inputs, c):
        #print(inputs)
        inputs.pop(_DESCRIPTION)
        valves_for_logical_layer = self.p_logic.get_valves_status(inputs)
        #valves_for_logical_layer = self.p_logic.get_valves_simulated_status(inputs)
        message_serialized = pickle.dumps(valves_for_logical_layer)
        c.sendall(message_serialized)
