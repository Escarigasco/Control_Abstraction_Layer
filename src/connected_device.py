# Connected Device Class


class connected_device:
    'Class for Pump definition and properties'

    def __init__(self, parent_ID, ID, type_device, rated_power):
        self.parent_ID = parent_ID
        self.ID = ID
        self.type = type_device
        self.rated_power = float(rated_power)

    def get_rated_power(self):
        return self.rated_power

    def get_parent(self):
        return self.parent_ID

    def get_name(self):
        return self.ID

    def __repr__(self):
        return "{0}".format(self.ID)

    def __str__(self):
        return "{0}".format(self.ID)
