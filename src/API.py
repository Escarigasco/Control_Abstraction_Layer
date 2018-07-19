# Interface to specify the configuration and launch the logical layer

import getopt
import pickle
import socket
import sys
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

    #try:
    #    ops, args = getopt.getopt(argv, "")

    #    if (len(argv) != nargs):
    #        print('main.py <BuildingID> <Switch_Board_ID>')
    #        sys.exit(2)

    #    for Building_ID in Building_List:
    #        if (argv[0] == Building_ID):
    #            recognized_building_ID = True
    #            break
    #    if (not recognized_building_ID):
    #        print('Invalid Building ID')
    #        sys.exit(2)

    #    for Switch_Board_ID in Switch_Board_List:
    #        if (argv[1] == Switch_Board_ID):
    #            recognized_board_ID = True
    #            break
    #    if (not recognized_board_ID):
    #            print('Invalid Board ID')
    #            sys.exit(2)

    while(1):
        n = int(input("How many sources? \n"))
        # controller start tested
        if n == 100:
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1BH4"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [2]
            sinks_two = ["Sink_1H8"]
            sources_two = ["Source_1DH6"]
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = [6]
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        elif n == 120:
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1BH4"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [2]
            sinks_two = ["Sink_1H8"]
            sources_two = ["Source_1DH6"]
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = [6]
            get_rid_of = {"Pumps": [], "Sensors": ["Sensor_1E8"], "Valves": []}
        elif n == 150:
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1BH4"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [200]
            sinks_two = ["Sink_1H8"]
            sources_two = ["Source_1DH6"]
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = [600]
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        # controller start tested
        elif (n == 200):
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1BH4"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [2]
            sinks_two = ["Sink_1H8"]
            sources_two = ["Source_1DH6"]
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        elif (n == 290):
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1DH6"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [2]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        elif (n == 300):
            sinks_one = []
            sources_one = []
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = []
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        # controller start tested
        elif (n == 400):
            sinks_one = ["Sink_1H7", "Sink_1H8"]
            sources_one = ["Source_1BH4"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [5, 5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        elif (n == 420):
            sinks_one = ["Sink_1H7", "Sink_1H8"]
            sources_one = ["Source_1BH4"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [5, 5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": ["Pump_1H7"], "Sensors": [], "Valves": []}
        elif (n == 450):
            sinks_one = ["Sink_1H7", "Sink_1H8"]
            sources_one = ["Source_1BH4"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [5000, 5555]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        # controller start tested
        elif (n == 500):
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1BH4", "Source_1HP5"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = [6]
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        elif (n == 520):
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1BH4", "Source_1HP5"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": ["Pump_1H7"], "Sensors": [], "Valves": []}
        # controller start tested
        elif (n == 600):
            sinks_one = ["Sink_1H7", "Sink_1H8"]
            sources_one = ["Source_1BH4", "Source_1HP5"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [5, 5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        elif (n == 620):
            sinks_one = ["Sink_1H7", "Sink_1H8"]
            sources_one = ["Source_1BH4", "Source_1HP5"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [5, 5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": ["Pump_1H7"], "Sensors": [], "Valves": []}
        # controller start tested
        elif (n == 700):
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1BH4", "Source_1HP5", "Source_1DH6"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        elif (n == 720):
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1BH4", "Source_1HP5", "Source_1DH6"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": ["Pump_1H7"], "Sensors": [], "Valves": []}
        # controller start tested
        elif (n == 800):
            sinks_one = ["Sink_1H7", "Sink_1H8"]
            sources_one = ["Source_1BH4", "Source_1HP5", "Source_1DH6"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [5, 5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        elif (n == 820):
            sinks_one = ["Sink_1H7", "Sink_1H8"]
            sources_one = ["Source_1BH4", "Source_1HP5", "Source_1DH6"]
            boosted_one = []
            parameters_one = "Energy"
            setpoints_one = [5, 5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": ["Pump_1H7"], "Sensors": [], "Valves": []}
        # controller start tested
        elif (n == 1700):
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1HP5", "Source_1DH6"]
            boosted_one = [("Source_1HP5", "Source_1DH6"), ]
            parameters_one = "Energy"
            setpoints_one = [5, 5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        elif (n == 1720):
            sinks_one = ["Sink_1H7", "Sink_1H8"]
            sources_one = ["Source_1HP5", "Source_1DH6"]
            boosted_one = [("Source_1HP5", "Source_1DH6"), ]
            parameters_one = "Energy"
            setpoints_one = [5, 5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": ["Pump_1H7"], "Sensors": [], "Valves": []}
        # controller start tested
        elif (n == 1800):
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1BH4", "Source_1HP5", "Source_1DH6"]
            boosted_one = [("Source_1BH4", "Source_1HP5"), ("Source_1HP5", "Source_1DH6")]
            parameters_one = "Energy"
            setpoints_one = [5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}
        elif (n == 1820):
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1BH4", "Source_1HP5", "Source_1DH6"]
            boosted_one = [("Source_1BH4", "Source_1HP5"), ("Source_1HP5", "Source_1DH6")]
            parameters_one = "Energy"
            setpoints_one = [5]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": ["Pump_1H6", "Pump_1C4"], "Sensors": ["Sensor_1E7", "Sensor_1E5", "Sensor_1E6"], "Valves": []}
        # controller start tested
        elif (n == 1850):
            sinks_one = ["Sink_1H7"]
            sources_one = ["Source_1BH4", "Source_1HP5", "Source_1DH6"]
            boosted_one = [("Source_1BH4", "Source_1HP5"), ("Source_1HP5", "Source_1DH6")]
            parameters_one = "Energy"
            setpoints_one = [50]
            sinks_two = []
            sources_two = []
            boosted_two = []
            parameters_two = "Energy"
            setpoints_two = []
            get_rid_of = {"Pumps": [], "Sensors": [], "Valves": []}

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

        Configuration_one = {"sinks": sinks_one, "sources": sources_one, "boosted": boosted_one,
                             "parameters": parameters_one, "setpoints": setpoints_one, "excluded_components": get_rid_of}
        Configuration_two = {"sinks": sinks_two, "sources": sources_two, "boosted": boosted_two,
                             "parameters": parameters_two, "setpoints": setpoints_two, "excluded_components": get_rid_of}
        for key in Configuration_one.keys():
            if ((not Configuration_one[key]) & (key != "boosted")):
                Configuration_one = None
                break
        for key in Configuration_two.keys():
            if ((not Configuration_two[key]) & (key != "boosted")):
                Configuration_two = None
                break

        input_dictionary = {"Configuration_one": Configuration_one, "Configuration_two": Configuration_two}
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

    #except getopt.GetoptError:
    #    print('main.py <BuildingID> <Switch_Board_ID>')
    #    s.close()
    #    sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
