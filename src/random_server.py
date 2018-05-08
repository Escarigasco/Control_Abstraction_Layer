import random
import syslab
# import sys
_BUILDING_NAME = "716-h1"


class random_server(object):

    def run(self, pumps, sensors, valves):
        min_operating = 0
        max_operating = 100
        step = max_operating * 0.5
        for valve in valves.keys():
            setpoint = random.randint(min_operating, max_operating)
            valves[valve].set_status(setpoint)


class current_status_reader(object):
    def __init__(self, pumps, sensors, valves):
            interface = syslab.HeatSwitchBoard(_BUILDING_NAME)

            valves_name_translator = {
                'Valve_1C4': "Bay_4L-Busbar_2R", 'Valve_2C4': "Bay_4L-Busbar_1R", 'Valve_2B4': "Bay_4H-Busbar_B", 'Valve_1H4': "Bay_4H-Busbar_2F", 'Valve_2H4': "Bay_4H-Busbar_1F", 'Valve_1B4': "Bay_4L-Busbar_B",
                'Valve_1C5': "Bay_5L-Busbar_1R", 'Valve_2C5': "Bay_5L-Busbar_2R", 'Valve_2B5': "Bay_5H-Busbar_B", 'Valve_1H5': "Bay_5H-Busbar_1F", 'Valve_2H5': "Bay_5H-Busbar_2F", 'Valve_1B5': "Bay_5L-Busbar_B",
                'Valve_1C6': "Bay_6L-Busbar_1R", 'Valve_2C6': "Bay_6L-Busbar_2R", 'Valve_2B6': "Bay_6H-Busbar_B", 'Valve_1H6': "Bay_6H-Busbar_1F", 'Valve_2H6': "Bay_6H-Busbar_2F", 'Valve_1B6': "Bay_6L-Busbar_B",
                'Valve_1H7': "Bay_7H-Busbar_1F", 'Valve_2H7': "Bay_7H-Busbar_2F", 'Valve_1C7': "Bay_7L-Busbar_1R", 'Valve_2C7': "Bay_7L-Busbar_2R",
                'Valve_1H8': "Bay_8H-Busbar_1F", 'Valve_2H8': "Bay_8H-Busbar_2F", 'Valve_1C8': "Bay_8L-Busbar_1R", 'Valve_2C8': "Bay_8L-Busbar_2R"}

            pump_name_translator = {
                'Pump_1C4': "Bay_4",
                'Pump_1H5': "Bay_5",
                'Pump_1H6': "Bay_6",
                'Pump_1H7': "Bay_7",
                'Pump_1H8': "Bay_8"}

            sensors_name = {
                'Sensor_1HT4': "Bay_4", 'Sensor_1CT4': "Bay_4", 'Sensor_1CF4': "Bay_4", 'Sensor_1E4': "Bay_4",
                'Sensor_1HT5': "Bay_5", 'Sensor_1CT5': "Bay_5", 'Sensor_1CF5': "Bay_5", 'Sensor_1E5': "Bay_5",
                'Sensor_1HT6': "Bay_6", 'Sensor_1CT6': "Bay_6", 'Sensor_1CF6': "Bay_6", 'Sensor_1E6': "Bay_6",
                'Sensor_1HT7': "Bay_7", 'Sensor_1CT7': "Bay_7", 'Sensor_1CF7': "Bay_7", 'Sensor_1E7': "Bay_7",
                'Sensor_1HT8': "Bay_8", 'Sensor_1CT8': "Bay_8", 'Sensor_1CF8': "Bay_8", 'Sensor_1E8': "Bay_8"}

            for valve in valves.keys():
                opening = interface.getValvePosition(valves_name_translator[valve])
                print(opening.value)
                valves[valve].set_status(opening.value)
            # sys.exit()
