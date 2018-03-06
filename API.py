import sys
import getopt
from logical_layer import logical_layer


def main(argv):
    Building_List = ["Building716"]
    Switch_Board_List = ["Switch_Board_1"]
    nargs = 2
    recognized_building_ID = False
    recognized_board_ID = False
    sensors = {}
    parameters = {}
    setpoints = {}
    sources = {}

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

        logical = logical_layer(Building_ID, Switch_Board_ID)

        while(1):

            operating_mode = input("Operating Mode:")
            if (operating_mode == "M"):
                n_sensors = int(input("how many sensors do you want to control?"))
                for n in range(0, n_sensors):
                    sensors[n] = input("Insert sensor code for sensor {0}:".format(n + 1))
                    parameters[n] = input("Insert parameter code for sensor {0}:".format(n + 1))
                    setpoints[n] = int(input("Insert setpoint for sensor {0}:".format(n + 1)))
                    sources[n] = input("Insert source code to control sensor {0}:".format(n + 1))
            else:
                sensors[0] = "Sensor_1E8"
                parameters[0] = "Energy"
                setpoints[0] = 50
                sources[0] = "Source_1HP5"

            logical.run(sensors, parameters, setpoints, sources)
            print("\n\n\n")

    except getopt.GetoptError:
        print('main.py <BuildingID> <Switch_Board_ID>')
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
