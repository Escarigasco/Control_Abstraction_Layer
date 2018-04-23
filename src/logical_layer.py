from configuration_reader import configuration_reader
from interface import interface
from matplotlib import pyplot as plt
from message_for_controller import message_for_controller
from object_tracker import object_tracker
from path_builder import path_builder
from switch_board_building import switch_board_building
import time
_BOOSTER_NAME = "Source_1BH4"
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

    def run(self, sinks, sensors, parameters, setpoints, sources, controlled_device, control_strategy, boosted):
        self.boosted = boosted
        self.used_sinks = sinks
        self.parameters = parameters
        self.setpoints = setpoints
        self.used_sources = sources
        self.controlled_device = controlled_device
        self.control_strategy = control_strategy
        self.sensors = sensors
        self.check_sources()
        system_input = {"sinks": self.used_sinks, "sensors": self.sensors, "parameters": self.parameters,
                        "setpoints": self.setpoints, "sources": self.used_sources,
                        "control_strategy": self.control_strategy, "controlled_device": self.controlled_device, "boosted": self.boosted}

        # builder = rule_engine(self.intf)
        cfg = configuration_reader(self.intf)
        online_configuration = cfg.run()
        pb = path_builder(self.intf)
        unique = pb.run(system_input, online_configuration)
        if unique is None:
            return
        mssgr = message_for_controller()
        message = mssgr.run(unique, system_input, self.intf)
        print(message)
        
    def check_sources(self):
        for source in self.used_sources:
            if (source == _BOOSTER_NAME):
                self.boosted = 'N'


if __name__ == "__main__":
    start_time = time.time()
    test = logical_layer("Building716", "Switch_Board_1")
    sinks = ["Sink_1H7"]
    sources = ["Source_1HP5"]
    boosted = "N"
    sensors = ["Sensor_1E8"]
    parameters = "Energy"
    setpoints = 50
    controlled_device = "Pump_1H5"
    control_strategy = "flow"
    test.run(sinks, sensors, parameters, setpoints, sources, controlled_device, control_strategy, boosted)
    print("--- %s seconds ---" % (time.time() - start_time))
    #plt.show()
