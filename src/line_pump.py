# Pump Class
from random import choice


class line_pump(object):
    'Class for Pump definition and properties'

    def __init__(self, parent_ID, ID, position, connected_dev, status=None):
        self.parent_ID = parent_ID
        self.ID = ID
        self.position = int(position)  # this tells you where is in the line
        self.location = connected_dev
        self.object_type = "Pump"

        if status is None:
            status = choice([1, 1, 1])
        self.status = status

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
