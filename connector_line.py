# Line Class
from system_sensor import system_sensor
from line_pump import line_pump


class connector_line(object):
    'Class for switch board definition and properties'

    def __init__(self, parent_ID, ID, line, flow_type, is_return):
        self.parent_ID = parent_ID
        self.ID = ID
        self.flow_type = flow_type
        self.line_sensors_list = {}
        self.pumps_list = {}
        self.line = line

        sensors = self.line.find_all("sensor", position="inline")
        pumps = self.line.find_all("pump", position="inline")

        for sensor in sensors:
            self.line_sensors_list[sensor["id"]] = system_sensor(self.ID, sensor["id"], sensor["variable"], sensor["embedded"], position="inline")

        for pump in pumps:
            self.pumps_list[pump["id"]] = line_pump(self.ID, pump["id"])

    def get_parent(self):
        return self.parent_ID

    def __repr__(self):
        return "<Line, id: {0}>".format(self.ID)

    def __str__(self):
        return "<Line, id: {0}>".format(self.ID)
