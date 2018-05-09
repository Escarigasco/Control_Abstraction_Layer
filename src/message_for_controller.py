# Class that prepare the message for the controller and select the pump to be used to govern the system
import configparser
import pickle
import re
from rule_engine import rule_engine
import socket


class message_for_controller(object):

        def __init__(self):
            self.HOST = 'localhost'    # The remote host
            self.PORT = 50008              # The same port as used by the server

        def run(self, unique, system_input, interface):



            system_valves = interface.get_system_valves()
            system_pipes = interface.get_system_pipes()
            system_pumps = interface.get_system_pumps()
            system_sensors = interface.get_system_sensors()
            system_busbars = interface.build_busbars(system_pipes)
            system_connected_devices = interface.get_connected_devices()
            controller_name = system_input["controller_name"]
            system_components = {**system_sensors, **system_busbars, **system_valves, **system_connected_devices, **system_valves, **system_pumps}
            object_nodes = {}
            sensors = []
            pumps = []
            config = configparser.ConfigParser()
            config.read("/home/federico/Desktop/SwitchBoard/SwitchBoard/src/config_controller.txt")

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
            feedback_sensors = self.name_translator(system_input["sensors"])

            input_for_controller = {"controller_name": controller_name, "kill": 'N', "gain": config.get(controller_name, "gain"), "kp": config.get(controller_name, "kp"),
                                    "ki": config.get(controller_name, "ki"), "kd": config.get(controller_name, "kd"),
                                    "circulator": act_pumps, "circulator_mode": config.get(controller_name, "circulator_mode"),
                                    "actuator": act_pumps, "setpoint": system_input['setpoints'], "feedback_sensor": feedback_sensors}
            print(input_for_controller)

            if ((len(system_input["sinks"]) == 1) & (len(system_input["sources"]) == 1) & (system_input["boosted"] == 'N')):
                message_serialized = pickle.dumps(input_for_controller)

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.HOST, self.PORT))
                    s.sendall(message_serialized)

                s.close()

        def kill(self, system_input):
            input_for_controller = {"controller_name": "Constant_Energy_Pump_Actuating", "kill": 'Y'}
            print(input_for_controller)

            if ((len(system_input["sinks"]) == 1) & (len(system_input["sources"]) == 1) & (system_input["boosted"] == 'N')):
                message_serialized = pickle.dumps(input_for_controller)

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.HOST, self.PORT))
                    s.sendall(message_serialized)

                s.close()



# deliver only the list of relevant component returning a dictionary stating the actuator and the feedback signal e.g. for the first use case will be pump x sensor and that's i
# where to decide the components to be used? if I do it here I won't take into account the posibility that a sensor/pump could be dead and replaced by another
# pump - if one sink use the pump of source, if there is booster use the booster
#       - if two sinks always use both pumps of each sink
# sensor -

        def name_translator(self, sensors):
            translated_sensors = []
            sensors_name = {
                'Sensor_1HT4': "Bay_4", 'Sensor_1CT4': "Bay_4", 'Sensor_1CF4': "Bay_4", 'Sensor_1E4': "Bay_4",
                'Sensor_1HT5': "Bay_5", 'Sensor_1CT5': "Bay_5", 'Sensor_1CF5': "Bay_5", 'Sensor_1E5': "Bay_5",
                'Sensor_1HT6': "Bay_6", 'Sensor_1CT6': "Bay_6", 'Sensor_1CF6': "Bay_6", 'Sensor_1E6': "Bay_6",
                'Sensor_1HT7': "Bay_7", 'Sensor_1CT7': "Bay_7", 'Sensor_1CF7': "Bay_7", 'Sensor_1E7': "Bay_7",
                'Sensor_1HT8': "Bay_8", 'Sensor_1CT8': "Bay_8", 'Sensor_1CF8': "Bay_8", 'Sensor_1E8': "Bay_8"}
            for sensor in sensors:
                translated_sensors.append(sensors_name[sensor])
                print(translated_sensors)
            return translated_sensors



        def pump_selector(self, ideal_pump, pumps):
            actuators_pumps = []
            locations = []
            for location in ideal_pump.location:
                locations.append(location.data)
            for pump in pumps:
                if (pump.location in locations):
                    actuators_pumps.append(pump.get_name())
            return actuators_pumps
