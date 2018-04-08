from rule_engine import rule_engine
import re
from enum import IntFlag, auto


class message_for_controller(object):

        def __init__(self, unique, system_input, interface):
            system_valves = interface.get_system_valves()
            system_lines = interface.get_system_lines()
            system_pipes = interface.get_system_pipes()
            system_pumps = interface.get_system_pumps()
            system_sensors = interface.get_system_sensors()
            system_busbars = interface.build_busbars(system_pipes)
            system_connected_devices = interface.get_connected_devices()
            system_components = {**system_sensors, **system_busbars, **system_valves, **system_connected_devices, **system_valves, **system_pumps}
            object_nodes = {}
            sensors = []
            pumps = []

            nodes = list(unique.nodes)
            for node in nodes:
                object_nodes[node] = system_components[node]
                print(object_nodes[node])
            print('\n\n')

            for node in object_nodes.keys():
                s_name = 'Sensor'
                if (re.match(s_name, node)):
                    sensors.append(object_nodes[node])
                p_name = 'Pump'
                if (re.match(p_name, node)):
                    pumps.append(object_nodes[node])
            print(pumps)

            engine = rule_engine()
            ideal_pump = engine.run(system_input)
            act_pumps = self.pump_selector(ideal_pump, pumps)
            print(act_pumps)

            '''while(1):
                for successor in list(unique.successors(node)):
                    print("{0}\n".format(successor))
                    node = successor
                break'''
            # while(1):
                # node = unique.successors(node)


# deliver only the list of relevant component returning a dictionary stating the actuator and the feedback signal e.g. for the first use case will be pump x sensor and that's i
# where to decide the components to be used? if I do it here I won't take into account the posibility that a sensor/pump could be dead and replaced by another
#rules:
# pump - if one sink use the pump of source, if there is booster use the booster
#       - if two sinks always use both pumps of each sink
# sensor -
        def pump_selector(self, ideal_pump, pumps):
            actuators_pumps = []
            for pump in pumps:
                print(pump.location)
                print(str(ideal_pump.location))
                if (pump.location in str(ideal_pump.location)):
                    actuators_pumps.append(pump)
            return actuators_pumps
