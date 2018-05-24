# Interface to specify the configuration and launch the logical layer

import sys
import getopt
from logical_layer import logical_layer
import pickle
import socket
_HOST = 'localhost'                 # Symbolic name meaning all available interfaces
_PORT = 50000              # Arbitrary non-privileged port
_BEGIN_WITH = 0



def main(argv):
    Building_List = ["Building716"]
    Switch_Board_List = ["Switch_Board_1"]
    nargs = 2
    recognized_building_ID = False
    recognized_board_ID = False
    parameters = []
    setpoints = []
    sources = []
    sinks = []
    input_dictionary = {}

    try:
        ops, args = getopt.getopt(argv, "")

        if (len(argv) != nargs):
            print('main.py <BuildingID> <Switch_Board_ID>')
            sys.exit(2)

        for Building_ID in Building_List:
            if (argv[0] == Building_ID):
                recognized_building_ID = True
                break
        if (not recognized_building_ID):
            print('Invalid Building ID')
            sys.exit(2)

        for Switch_Board_ID in Switch_Board_List:
            if (argv[1] == Switch_Board_ID):
                recognized_board_ID = True
                break
        if (not recognized_board_ID):
                print('Invalid Board ID')
                sys.exit(2)

        while(1):
            n = int(input("How many sources? \n"))
            if n == 100:
                sinks = ["Sink_1H7"]
                sources = ["Source_1BH4"]
                boosted = "N"
                parameters = "Energy"
                setpoints = [2]
            elif (n == 200):
                sinks = ["Sink_1H8"]
                sources = ["Source_1DH6"]
                boosted = "N"
                parameters = "Energy"
                setpoints = [6]
            elif (n == 300):
                sinks = ["Sink_1H8", "Sink_1H7"]
                sources = ["Source_1HP5"]
                boosted = "N"
                parameters = "Energy"
                setpoints = [1, 2]
            elif (n == 400):
                sinks = ["Sink_1H8", "Sink_1H7"]
                sources = ["Source_1HP5"]
                boosted = "Y"
                parameters = "Energy"
                setpoints = [1, 2]
            elif (n == 500):
                sinks = ["Source_1HP5"]
                sources = ["Sink_1H8"]
                boosted = "N"
                parameters = "Energy"
                setpoints = [1]
                print("1 to 1 reverse")
            elif (n == 600):
                sinks = ["Source_1HP5", "Source_1BH4"]
                sources = ["Sink_1H8"]
                boosted = "N"
                parameters = "Energy"
                setpoints = [1, 2]
                print("1 to 2 reverse")

            else:
                parameters = []
                setpoints = []
                sources = []
                sinks = []

                for i in range(_BEGIN_WITH, n):
                    sources.insert(i, input("Insert code for source {0}: \n".format(i)))
                n = int(input("How many sinks? \n"))
                for i in range(_BEGIN_WITH, n):
                    sinks.insert(i, input("Insert code for sink {0}: \n".format(i)))
                n = int(input("How many parameters? \n"))
                for i in range(_BEGIN_WITH, n):
                    parameters.insert(i, input("Insert parameter code for sensor {0}: \n".format(i)))
                    setpoints.insert(i, int(input("Insert setpoint for sensor {0}: \n".format(i))))
                boosted = input("Is the system Boosted? \n")

            input_dictionary = {"sinks": sinks, "sources": sources, "boosted": boosted,
                                "parameters": parameters, "setpoints": setpoints}
            print(input_dictionary)
            print("\n\n\n\n")
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((_HOST, _PORT))
                    message_serialized = pickle.dumps(input_dictionary)
                    s.sendall(message_serialized)
                    print("\n\n\n")
                    s.close()

            except (Exception, KeyboardInterrupt):
                print("Message sending failed")
                sys.exit()


    except getopt.GetoptError:
        print('main.py <BuildingID> <Switch_Board_ID>')
        s.close()
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
