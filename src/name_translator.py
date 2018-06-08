class name_translator(object):
    def __init__(self):
        self.reversed_valves_name_translator = {}
        self.valves_name_translator = {
            'Valve_2C4': "Bay_4L-Busbar_2R", 'Valve_1C4': "Bay_4L-Busbar_1R", 'Valve_1B4': "Bay_4H-Busbar_B", 'Valve_2H4': "Bay_4H-Busbar_2F", 'Valve_1H4': "Bay_4H-Busbar_1F", 'Valve_2B4': "Bay_4L-Busbar_B",
            'Valve_2C5': "Bay_5L-Busbar_1R", 'Valve_1C5': "Bay_5L-Busbar_2R", 'Valve_1B5': "Bay_5H-Busbar_B", 'Valve_2H5': "Bay_5H-Busbar_1F", 'Valve_1H5': "Bay_5H-Busbar_2F", 'Valve_2B5': "Bay_5L-Busbar_B",
            'Valve_2C6': "Bay_6L-Busbar_1R", 'Valve_1C6': "Bay_6L-Busbar_2R", 'Valve_1B6': "Bay_6H-Busbar_B", 'Valve_2H6': "Bay_6H-Busbar_1F", 'Valve_1H6': "Bay_6H-Busbar_2F", 'Valve_2B6': "Bay_6L-Busbar_B",
            'Valve_2H7': "Bay_7H-Busbar_1F", 'Valve_1H7': "Bay_7H-Busbar_2F", 'Valve_2C7': "Bay_7L-Busbar_1R", 'Valve_1C7': "Bay_7L-Busbar_2R",
            'Valve_2H8': "Bay_8H-Busbar_1F", 'Valve_1H8': "Bay_8H-Busbar_2F", 'Valve_2C8': "Bay_8L-Busbar_1R", 'Valve_1C8': "Bay_8L-Busbar_2R"}
        self.reversed_valves_name_translator = {v: k for k, v in self.valves_name_translator.items()}

    def valves(self, valve):
            return self.valves_name_translator[valve]

    def reverse_valves(self, valve):
            return self.reversed_valves_name_translator[valve]


    
