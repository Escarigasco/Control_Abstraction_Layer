# Class for object_tracker - it identify with the simple method where are the specified devices (pumps, sensors, lines, etc..)
import re
from collections import defaultdict


class object_tracker(object):

    def __init__(self, interface):
        self.intf = interface

    def where_are_devices(self, devices):
        final_location = "Bay_"
        parents_list = self.intf.get_all_parents()
        device_position = defaultdict(list)

        for device_name in devices.keys():
            device = devices[device_name]
            device_location = device.get_parent()

            while not (re.match(final_location, device_location)):

                parent = parents_list[device_location]
                device_location = parent.get_parent()

            device_position[device_location].append(devices[device_name])
            device_position[device_name] = device_location
        return device_position
