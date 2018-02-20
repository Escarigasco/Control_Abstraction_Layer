# Pipeline Class


class pipeline(object):
    'Class for Pipeline definition and properties'

    def __init__(self, bay_ID, ID, direction):
        self.bay_ID = bay_ID
        self.ID = ID
        self.direction = direction

    def __repr__(self):
        return "<Pipe, id: {0}>".format(self.ID)

    def __str__(self):
        return "<Pipe, id: {0}>".format(self.ID)
