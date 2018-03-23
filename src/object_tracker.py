# Class for object_tracker
import re
from collections import defaultdict


class object_tracker(object):

    def __init__(self, interface):
        self.intf = interface
        self.sensor_position = {}
        self.device_position = {}
        self.line_position = {}
        self.valve_position = {}
        self.pump_position = {}

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

    def where_are_valves(self, system_valves, system_lines):
        final_location = "Bay_"
        parents_list = self.intf.get_all_parents()

        '''for line_name in system_lines.keys():
            line = system_lines[line_name]
            line_location = line.get_parent()

            while not (re.match(final_location, line_location)):

                parent = parents_list[line_location]
                line_location = parent.get_parent()

            self.line_position[line_name] = line_location'''

        for valve_name in system_valves.keys():
            valve = system_valves[valve_name]
            valve_location = valve.get_parent()

            while not (re.match(final_location, valve_location)):

                parent = parents_list[valve_location]
                valve_location = parent.get_parent()

            self.valve_position[valve_name] = valve_location

        return self.valve_position
