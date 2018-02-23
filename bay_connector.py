# connector class
from connector_line import connector_line


class bay_connector:

    def __init__(self, bay_ID, ID, connector, return_line):
        self.bay_ID = bay_ID
        self.ID = ID
        self.line_list = {}
        self.connector = connector
        self.return_line = return_line

        lines = self.connector.find_all("line")

        for line in lines:
            if (self.return_line == line["type"]):
                is_return = True
                self.line_list[line["id"]] = connector_line(self.ID, line["id"], line, is_return)
            else:
                is_return = False
                self.line_list[line["id"]] = connector_line(self.ID, line["id"], line, is_return)

        def get_name(self):
            return self.ID
