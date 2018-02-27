# Class for object_tracker
import re


class object_tracker(object):

    def __init__(self, interface):
        self.intf = interface
        self.sensor_position = {}
        self.device_position = {}

    def where_are_sensors(self, sensors):
        final_location = "Bay_"
        sensors_list = sensors
        parents_list = self.intf.get_all_parents()

        for key in sensors_list.keys():
            sensor = sensors_list[key]
            sensor_location = sensor.get_parent()

            while not (re.match(final_location, sensor_location)):
                # print(sensor_location)
                parent = parents_list[sensor_location]
                sensor_location = parent.get_parent()
                # print(sensor_location)

            self.sensor_position[key] = sensor_location

        return self.sensor_position

    def where_are_connected_devices(self, devices):
        final_location = "Bay_"
        device_list = devices
        parents_list = self.intf.get_all_parents()

        for key in device_list.keys():
            device = device_list[key]
            device_location = device.get_parent()

            while not (re.match(final_location, device_location)):
                # print(device_location)
                parent = parents_list[device_location]
                device_location = parent.get_parent()
                # print(device_location)

            self.device_position[key] = device_location

        return self.device_position
