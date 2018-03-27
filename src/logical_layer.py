from switch_board_building import switch_board_building
from interface import interface
from object_tracker import object_tracker
from path_builder import path_builder
from path_matcher import path_matcher
from configuration_reader import configuration_reader
import time
from matplotlib import pyplot as plt

#  from IPython.core.debugger import Tracer
#  Tracer()()


class logical_layer(object):
    'Component that output the control object'
    def __init__(self, buildingID, SwitchID):
        self.buildingID = buildingID
        self.SwitchID = SwitchID

        self.building_config = switch_board_building(self.buildingID)
        self.intf = interface(self.building_config, self.SwitchID)
        self.objtk = object_tracker(self.intf)

    def run(self, sensors, parameters, setpoints, sources, controlled_device, control_strategy):

        self.used_sensors = sensors
        self.parameters = parameters
        self.setpoints = setpoints
        self.used_sources = sources
        self.controlled_device = controlled_device
        self.control_strategy = control_strategy
        system_input = {"sensor": self.used_sensors, "parameter": self.parameters,
                        "setpoint": self.setpoints, "sources": self.used_sources,
                        "control_strategy": self.control_strategy, "controlled_device": self.controlled_device}

        # builder = rule_engine(self.intf)
        cfg = configuration_reader(self.intf)
        online_configuration = cfg.run()
        pb = path_builder(self.intf)
        possible_configurations = pb.run(system_input)
        pm = path_matcher(online_configuration, possible_configurations)
        short_list = pm.run()


if __name__ == "__main__":
    start_time = time.time()
    test = logical_layer("Building716", "Switch_Board_1")
    sensors = ["Sensor_1E8"]
    parameters = "Energy"
    setpoints = 50
    sources = ["Source_1HP5"]
    controlled_device = "Pump_1H5"
    control_strategy = "flow"
    test.run(sensors, parameters, setpoints, sources, controlled_device, control_strategy)
    print("--- %s seconds ---" % (time.time() - start_time))
    plt.show()
