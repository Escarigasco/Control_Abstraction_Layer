# Class that prepare the message for the controller and select the pump to be used to govern the system
from components_status import components_status
import configparser
import pickle
from rule_engine import rule_engine
import socket
import sys

import time
_ACTIVE = 1
_INACTIVE = 0
_FIRST_OF_CLASS = 1


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
            system_components = {**system_sensors, **system_busbars, **system_valves, **system_connected_devices, **system_valves, **system_pumps}
            unique_nodes = {}
            config = configparser.ConfigParser()
            config.read("/home/federico/Desktop/SwitchBoard/SwitchBoard/src/config_controller.txt")



            nodes = list(unique.nodes)
            for node in nodes:
                unique_nodes[node] = system_components[node]

            c_status = components_status()
            available_components = c_status.run(interface, unique_nodes)
            try:
                engine = rule_engine()
                ideal_components = engine.run(system_input, available_components)
                act_circulator = self.pump_selector(ideal_components["Ideal_Pump"], available_components["Pumps_active"])
                print(act_circulator)
                actuators = self.actuator_selector(ideal_components["Ideal_Actuator"], available_components["Valves_active"], available_components["Pumps_active"])
                print(actuators)
                feedback_sensors = self.sensor_selector(ideal_components["Ideal_Sensor"], available_components["Sensors_active"], system_input["parameters"])
                print(feedback_sensors)
                act_circulator["pumps"] = self.circulator_name_translator(act_circulator["pumps"])
                print(act_circulator)
                feedback_sensors["sensors"] = self.sensors_name_translator(feedback_sensors["sensors"])
                print(feedback_sensors)
                actuators["actuators"] = self.actuators_name_translator(actuators["actuators"])
                print(actuators)
                self.controller_name = act_circulator["mode"]

                input_for_controller = {"controller_name": self.controller_name, "kill": 'N', "gain": config.get(self.controller_name, "gain"), "kp": config.get(self.controller_name, "kp"),
                                        "ki": config.get(self.controller_name, "ki"), "kd": config.get(self.controller_name, "kd"),
                                        "circulator": act_circulator["pumps"], "circulator_mode": act_circulator["mode"],
                                        "actuator": actuators["actuators"], "setpoint": system_input['setpoints'], "feedback_sensor": feedback_sensors["sensors"]}
                print(input_for_controller)
            except Exception:
                return
            #sys.exit()

            try:
                if ((len(system_input["sinks"]) == 1) & (len(system_input["sources"]) == 1) & (system_input["boosted"] == 'N')):
                    message_serialized = pickle.dumps(input_for_controller)

                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((self.HOST, self.PORT))
                        s.sendall(message_serialized)

                    s.close()
            except Exception:
                print("Message sending failed")
                pass

        def kill(self, system_input):
            input_for_controller = {"controller_name": self.controller_name, "kill": 'Y'}
            print(input_for_controller)
            try:
                if ((len(system_input["sinks"]) == 1) & (len(system_input["sources"]) == 1) & (system_input["boosted"] == 'N')):
                    message_serialized = pickle.dumps(input_for_controller)

                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((self.HOST, self.PORT))
                        s.sendall(message_serialized)
                    s.close()
            except Exception:
                print("Message sending failed")
                pass


# deliver only the list of relevant component returning a dictionary stating the actuator and the feedback signal e.g. for the first use case will be pump x sensor and that's i
# where to decide the components to be used? if I do it here I won't take into account the posibility that a sensor/pump could be dead and replaced by another
# pump - if one sink use the pump of source, if there is booster use the booster
#       - if two sinks always use both pumps of each sink
# sensor -

        def sensors_name_translator(self, sensors):
            translated_sensors = []
            sensors_name = {
                'Sensor_1HT4': "Bay_4", 'Sensor_1CT4': "Bay_4", 'Sensor_1CF4': "Bay_4", 'Sensor_1E4': "Bay_4",
                'Sensor_1HT5': "Bay_5", 'Sensor_1CT5': "Bay_5", 'Sensor_1CF5': "Bay_5", 'Sensor_1E5': "Bay_5",
                'Sensor_1HT6': "Bay_6", 'Sensor_1CT6': "Bay_6", 'Sensor_1CF6': "Bay_6", 'Sensor_1E6': "Bay_6",
                'Sensor_1HT7': "Bay_7", 'Sensor_1CT7': "Bay_7", 'Sensor_1CF7': "Bay_7", 'Sensor_1E7': "Bay_7",
                'Sensor_1HT8': "Bay_8", 'Sensor_1CT8': "Bay_8", 'Sensor_1CF8': "Bay_8", 'Sensor_1E8': "Bay_8"}
            for sensor in sensors:
                translated_sensors.append(sensors_name[sensor])
            return translated_sensors

        def actuators_name_translator(self, actuators):
            translated_actuator = []
            actuator_name = {
                'Pump_1C4': "Pump_Bay4",
                'Pump_1H5': "Pump_Bay5",
                'Pump_1H6': "Pump_Bay6",
                'Pump_1H7': "Pump_Bay7",
                'Pump_1H8': "Pump_Bay8",
                'Valve_2C4': "Bay_4L-Busbar_2R", 'Valve_1C4': "Bay_4L-Busbar_1R", 'Valve_1B4': "Bay_4H-Busbar_B", 'Valve_2H4': "Bay_4H-Busbar_2F", 'Valve_1H4': "Bay_4H-Busbar_1F", 'Valve_2B4': "Bay_4L-Busbar_B",
                'Valve_2C5': "Bay_5L-Busbar_1R", 'Valve_1C5': "Bay_5L-Busbar_2R", 'Valve_1B5': "Bay_5H-Busbar_B", 'Valve_2H5': "Bay_5H-Busbar_1F", 'Valve_1H5': "Bay_5H-Busbar_2F", 'Valve_2B5': "Bay_5L-Busbar_B",
                'Valve_2C6': "Bay_6L-Busbar_1R", 'Valve_1C6': "Bay_6L-Busbar_2R", 'Valve_1B6': "Bay_6H-Busbar_B", 'Valve_2H6': "Bay_6H-Busbar_1F", 'Valve_1H6': "Bay_6H-Busbar_2F", 'Valve_2B6': "Bay_6L-Busbar_B",
                'Valve_2H7': "Bay_7H-Busbar_1F", 'Valve_1H7': "Bay_7H-Busbar_2F", 'Valve_2C7': "Bay_7L-Busbar_1R", 'Valve_1C7': "Bay_7L-Busbar_2R",
                'Valve_2H8': "Bay_8H-Busbar_1F", 'Valve_1H8': "Bay_8H-Busbar_2F", 'Valve_2C8': "Bay_8L-Busbar_1R", 'Valve_1C8': "Bay_8L-Busbar_2R"}
            for actuator in actuators:
                translated_actuator.append(actuator_name[actuator])
            return translated_actuator

        def circulator_name_translator(self, circulators):
            translated_circulator = []
            circulators_name = {
                'Pump_1C4': "Pump_Bay4",
                'Pump_1H5': "Pump_Bay5",
                'Pump_1H6': "Pump_Bay6",
                'Pump_1H7': "Pump_Bay7",
                'Pump_1H8': "Pump_Bay8"}
            for circulator in circulators:
                translated_circulator.append(circulators_name[circulator])
            return translated_circulator




        def pump_selector(self, ideal_pump, pumps):
            circulation_pumps = []
            locations = []
            for location in ideal_pump.location:
                locations.append(location.data)
            for pump in pumps:
                if (pump.location in locations):
                    circulation_pumps.append(pump.get_name())
            pumps_mode = {"pumps": circulation_pumps, "mode": ideal_pump.mode.data}
            return pumps_mode

        def sensor_selector(self, ideal_sensor, sensors, variable):
            feedback_sensors = []
            locations = []
            for location in ideal_sensor.location:
                locations.append(location.data)
            for sensor in sensors:
                if ((sensor.location in locations) & (sensor.variable == variable)):
                    feedback_sensors.append(sensor.get_name())
            sensors_feed = {"sensors": feedback_sensors}
            return sensors_feed

        '''this method is missing the discrimination -- which valve of the rule engine'''
        def actuator_selector(self, ideal_actuator, valves, pumps):
            actuators = valves + pumps
            active_actuators = []
            locations = []
            for location in ideal_actuator.location:
                locations.append(location.data)
            for actuator in actuators:
                if ((actuator.type == ideal_actuator.type.data) & (actuator.location in locations)):
                    active_actuators.append(actuator.get_name())
            acts = {"actuators": active_actuators}
            return acts
