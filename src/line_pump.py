# Pump Class


class line_pump:
    'Class for Pump definition and properties'

    def __init__(self, parent_ID, ID):
        self.parent_ID = parent_ID
        self.ID = ID

    def get_name(self):
        return self.ID

    def set_status(self, status):
        self.status = status

    def get_parent(self):
        return self.parent_ID

    def get_status(self):
        return self.status

    def __repr__(self):
        return "{0}".format(self.ID)

    def __str__(self):
        return "{0}".format(self.ID)
