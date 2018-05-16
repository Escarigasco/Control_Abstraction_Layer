# Line Class - all pumps and sensors are now embedded in the line

from system_sensor import system_sensor
from line_pump import line_pump


class connector_line(object):
    'Class for switch board definition and properties'

    def __init__(self, parent_ID, ID, line, flow_type, is_return, connected_dev):
        self.parent_ID = parent_ID
        self.ID = ID
        self.flow_type = flow_type
        self.line_sensors = {}
        self.pumps = {}
        self.line = line

        sensors = self.line.find_all("sensor")
        pumps = self.line.find_all("pump")

        for sensor in sensors:
            self.line_sensors[sensor["id"]] = system_sensor(self.ID, sensor["id"], sensor["variable"], sensor["embedded"], sensor["line_position"], connected_dev)

        for pump in pumps:
            self.pumps[pump["id"]] = line_pump(self.ID, pump["id"], pump["line_position"], connected_dev)

    def get_parent(self):
        return self.parent_ID

    def __repr__(self):
        return "<Line, id: {0}>".format(self.ID)

    def __str__(self):
        return "<Line, id: {0}>".format(self.ID)
