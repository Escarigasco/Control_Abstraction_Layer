# Valve Class


class bay_valve:
    'Class for Valve definition and properties'

    def __init__(self, bay_ID, ID):
        self.bay_ID = bay_ID
        self.ID = ID
        self.position = 10  # this needs to be real time read

    def get_name(self):
        return self.ID

    def get_position(self):
        return self.position

        def __repr__(self):
            return "<Valve, id: {0}>".format(self.ID)

        def __str__(self):
            return "<Valve, id: {0}>".format(self.ID)
