class name_translator(object):
    def __init__(self):
        self.reversed_components_name_translator = {}
        self.components_name_translator = {
            'Pump_1C4': "Pump_Bay4",
            'Pump_1H5': "Pump_Bay5",
            'Pump_1H6': "Pump_Bay6",
            'Pump_1H7': "Pump_Bay7",
            'Pump_1H8': "Pump_Bay8",
            'Sensor_1HT2': "Bay_2", 'Sensor_1CT2': "Bay_2", 'Sensor_1CF2': "Bay_2", 'Sensor_1E2': "Bay_2",
            'Sensor_1HT3': "Bay_3", 'Sensor_1CT3': "Bay_3", 'Sensor_1CF3': "Bay_3", 'Sensor_1E3': "Bay_3",
            'Sensor_1HT4': "Bay_4", 'Sensor_1CT4': "Bay_4", 'Sensor_1CF4': "Bay_4", 'Sensor_1E4': "Bay_4",
            'Sensor_1HT5': "Bay_5", 'Sensor_1CT5': "Bay_5", 'Sensor_1CF5': "Bay_5", 'Sensor_1E5': "Bay_5",
            'Sensor_1HT6': "Bay_6", 'Sensor_1CT6': "Bay_6", 'Sensor_1CF6': "Bay_6", 'Sensor_1E6': "Bay_6",
            'Sensor_1HT7': "Bay_7", 'Sensor_1CT7': "Bay_7", 'Sensor_1CF7': "Bay_7", 'Sensor_1E7': "Bay_7",
            'Sensor_1HT8': "Bay_8", 'Sensor_1CT8': "Bay_8", 'Sensor_1CF8': "Bay_8", 'Sensor_1E8': "Bay_8",
            'Valve_2H2': "Bay_2H-Busbar_2F", 'Valve_1H2': "Bay_2H-Busbar_1F", 'Valve_1B2': "Bay_2H-Busbar_B", 'Valve_2C2': "Bay_2L-Busbar_2R", 'Valve_1C2': "Bay_2L-Busbar_1R", 'Valve_2B2': "Bay_2L-Busbar_B",
            'Valve_2H3': "Bay_3H-Busbar_2F", 'Valve_1H3': "Bay_3H-Busbar_1F", 'Valve_1B3': "Bay_3H-Busbar_B", 'Valve_2C3': "Bay_3L-Busbar_2R", 'Valve_1C3': "Bay_3L-Busbar_1R", 'Valve_2B3': "Bay_3L-Busbar_B",
            'Valve_2C4': "Bay_4L-Busbar_2R", 'Valve_1C4': "Bay_4L-Busbar_1R", 'Valve_1B4': "Bay_4H-Busbar_B", 'Valve_2H4': "Bay_4H-Busbar_2F", 'Valve_1H4': "Bay_4H-Busbar_1F", 'Valve_2B4': "Bay_4L-Busbar_B",
            'Valve_2C5': "Bay_5L-Busbar_1R", 'Valve_1C5': "Bay_5L-Busbar_2R", 'Valve_1B5': "Bay_5H-Busbar_B", 'Valve_2H5': "Bay_5H-Busbar_1F", 'Valve_1H5': "Bay_5H-Busbar_2F", 'Valve_2B5': "Bay_5L-Busbar_B",
            'Valve_2C6': "Bay_6L-Busbar_1R", 'Valve_1C6': "Bay_6L-Busbar_2R", 'Valve_1B6': "Bay_6H-Busbar_B", 'Valve_2H6': "Bay_6H-Busbar_1F", 'Valve_1H6': "Bay_6H-Busbar_2F", 'Valve_2B6': "Bay_6L-Busbar_B",
            'Valve_2H7': "Bay_7H-Busbar_1F", 'Valve_1H7': "Bay_7H-Busbar_2F", 'Valve_2C7': "Bay_7L-Busbar_1R", 'Valve_1C7': "Bay_7L-Busbar_2R",
            'Valve_2H8': "Bay_8H-Busbar_1F", 'Valve_1H8': "Bay_8H-Busbar_2F", 'Valve_2C8': "Bay_8L-Busbar_1R", 'Valve_1C8': "Bay_8L-Busbar_2R"}
        self.reversed_components_name_translator = {v: k for k, v in self.components_name_translator.items()}

    def components(self, valve):
            return self.components_name_translator[valve]

    def reverse_components(self, valve):
            return self.reversed_components_name_translator[valve]
