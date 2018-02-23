# Line Class


class connector_line(object):
    'Class for switch board definition and properties'

    def __init__(self, connector_ID, ID, line, is_return):
        self.connector_ID = connector_ID
        self.ID = ID
        self.sensor_list = {}
        self.line = line

        sensors = self.line.find_all("sensor")     # find sensor
        pump = self.line.find_all("pump")        # find pump

        for sensor in sensors:
            self.sensor_list[sensor["id"]] = line_sensor(self.ID, sensor["ID"], sensor, sensor["T"], sensor["embedded"])
