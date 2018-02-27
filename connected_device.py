# Connected Device Class


class connected_device:
    'Class for Pump definition and properties'

    def __init__(self, parent_ID, ID, type):
        self.parent_ID = parent_ID
        self.ID = ID
        self.type = type

    def get_parent(self):
        return self.parent_ID

    def get_name(self):
        return self.ID

    def __repr__(self):
        return "<Connected_device, id: {0}>".format(self.ID)

    def __str__(self):
        return "<Connected_device, id: {0}>".format(self.ID)
