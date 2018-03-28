# connector class
from connector_line import connector_line
from system_sensor import system_sensor
from connected_device import connected_device


class bay_connector:

    def __init__(self, parent_ID, ID, connector, output_line):
        self.parent_ID = parent_ID
        self.ID = ID
        self.lines_list = {}
        self.connector = connector
        self.output_line = output_line
        self.connected_devices_list = {}

        lines = self.connector.find_all("line")
        devices = self.connector.find_all("connected_device")

        for line in lines:
            if (self.output_line == line["type"]):
                is_output = True
                self.lines_list[line["id"]] = connector_line(self.ID, line["id"], line, line["type"], is_output)

            else:
                is_output = False
                self.lines_list[line["id"]] = connector_line(self.ID, line["id"], line, line["type"], is_output)

        for device in devices:
            self.connected_devices_list[device["id"]] = connected_device(self.ID, device["id"], device["type"], device["rating"])

    def get_parent(self):
        return self.parent_ID

    def get_name(self):
        return self.ID

    def __repr__(self):
        return "<Connector, id: {0}>".format(self.ID)

    def __str__(self):
        return "<Connector, id: {0}>".format(self.ID)
