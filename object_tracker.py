# Class for object_tracker
import re


class object_tracker(object):

    def __init__(self, interface):
        self.intf = interface
        self.sensor_position = {}

    def where_are_sensors(self, sensors_list):
        final_location = "Bay_"
        self.sensors_list = sensors_list
        self.parents_list = self.intf.get_all_parents()

        for key in self.sensors_list.keys():
            sensor = self.sensors_list[key]
            sensor_location = sensor.get_parent()

            while not (re.match(final_location, sensor_location)):
                print(sensor_location)
                parent = self.parents_list[sensor_location]
                sensor_location = parent.get_parent()
                print(sensor_location)

            self.sensor_position[key] = sensor_location

        return self.sensor_position
