# Class that prepare the message for the controller and select the pump to be used to govern the system

import pickle
import re
from rule_engine import rule_engine
import socket


class message_for_controller(object):

        def run(self, unique, system_input, interface):
            HOST = 'localhost'    # The remote host
            PORT = 50008              # The same port as used by the server
            system_valves = interface.get_system_valves()
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
                # print(object_nodes[node])
            # print('\n\n')

            for node in object_nodes.keys():
                s_name = 'Sensor'
                if (re.match(s_name, node)):
                    sensors.append(object_nodes[node])
                p_name = 'Pump'
                if (re.match(p_name, node)):
                    pumps.append(object_nodes[node])
            # print(pumps)

            engine = rule_engine()
            ideal_pump = engine.run(system_input)
            act_pumps = self.pump_selector(ideal_pump, pumps)
            print(act_pumps)

            '''while(1):
                for successor in list(unique.successors(node)):
                    print("{0}\n".format(successor))
                    node = successor
                break'''

            input_for_controller = {"gain": 1, "kp": 2.58, "ki": 2.58, "kd": 0, "circulator": act_pumps, "circulator_mode": "constant m", "actuator": act_pumps, "setpoint": system_input['setpoints'], "feedback": system_input['sensors']}
            
            if ((len(system_input["sinks"]) == 1) & (len(system_input["sources"]) == 1) & (system_input["boosted"] == 'N')):
                message_serialized = pickle.dumps(input_for_controller)
                print(message_serialized)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((HOST, PORT))
                    s.sendall(message_serialized)
                    #data = s.recv(1024)
                    #print('Received', repr(data))
                s.close()

            return input_for_controller

# deliver only the list of relevant component returning a dictionary stating the actuator and the feedback signal e.g. for the first use case will be pump x sensor and that's i
# where to decide the components to be used? if I do it here I won't take into account the posibility that a sensor/pump could be dead and replaced by another
# pump - if one sink use the pump of source, if there is booster use the booster
#       - if two sinks always use both pumps of each sink
# sensor -
        def pump_selector(self, ideal_pump, pumps):
            actuators_pumps = []
            locations = []
            for location in ideal_pump.location:
                locations.append(location.data)
            for pump in pumps:
                if (pump.location in locations):
                    actuators_pumps.append(pump)
            return actuators_pumps
