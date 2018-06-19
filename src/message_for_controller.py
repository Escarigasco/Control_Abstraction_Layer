# Class that prepare the message for the controller and select the pump to be used to govern the system
from components_status import components_status
import configparser
import pickle
from rule_engine import rule_engine
import socket
import sys
import time

_FIRST_OF_CLASS = 1
_CONTROLLER_ACTIVATED = "Active"
_CONTROLLER_DEACTIVED = "Inactive"
_DESCRIPTION = "description"
_KILLER = "killer"
_CREATOR = "creator"


class message_for_controller(object):

        def __init__(self, interface, comms, translator):
            self.translator = translator
            self.intf = interface
            self.comms = comms
            self.HOST = 'localhost'    # The remote host
            self.PORT = 2000              # The same port as used by the server

        def run(self, available_components, system_input, controller_name):

            system_valves = self.intf.get_system_valves()
            system_pipes = self.intf.get_system_pipes()
            system_pumps = self.intf.get_system_pumps()
            system_sensors = self.intf.get_system_sensors()
            system_busbars = self.intf.build_busbars(system_pipes)
            system_connected_devices = self.intf.get_connected_devices()
            system_components = {**system_sensors, **system_busbars, **system_connected_devices, **system_valves, **system_pumps}
            unique_nodes = {}
            config = configparser.ConfigParser()
            config.read("/home/federico/Desktop/SwitchBoard/SwitchBoard/src/config_controller.txt")

            try:
                valves_of_circuit = self.components_name_translator([valve.ID for valve in available_components["Valves_active"]])
                print(valves_of_circuit)
                engine = rule_engine()
                ideal_components = engine.run(system_input, available_components)
                act_circulator = self.pump_selector(ideal_components["Ideal_Pump"], available_components["Pumps_active"])
                #print(act_circulator)
                actuators = self.actuator_selector(ideal_components["Ideal_Actuator"], available_components["Valves_active"], available_components["Pumps_active"])
                #print(actuators)
                feedback_sensors = self.sensor_selector(ideal_components["Ideal_Sensor"], available_components["Sensors_active"], system_input["parameters"])
                #print(feedback_sensors)
                act_circulator["pumps"] = self.components_name_translator(act_circulator["pumps"])
                #print(act_circulator)
                feedback_sensors["sensors"] = self.components_name_translator(feedback_sensors["sensors"])
                #print(feedback_sensors)
                actuators["actuators"] = self.components_name_translator(actuators["actuators"])
                #print(actuators)
                controller_mode = act_circulator["mode"]
                # self.controller_name = act_circulator["mode"]

                input_for_controller = {"controller_name": controller_name, _DESCRIPTION: _CREATOR, "gain": config.get(controller_mode, "gain"), "kp": config.get(controller_mode, "kp"),
                                        "ki": config.get(controller_mode, "ki"), "kd": config.get(controller_mode, "kd"),
                                        "circulator": act_circulator["pumps"], "circulator_mode": act_circulator["mode"],
                                        "actuator": actuators["actuators"], "setpoint": system_input['setpoints'], "feedback_sensor": feedback_sensors["sensors"], "valves": valves_of_circuit}
                print(input_for_controller)
            except Exception:
                print("There is a failure in calculate the components to be used")
                return _CONTROLLER_DEACTIVED

            try:
                if ((len(system_input["sinks"]) >= 1) & (len(system_input["sources"]) == 1) & (system_input["boosted"] == 'N')):
                    feedback = self.comms.send(input_for_controller)
                    print("Message Sent")
                    print("Feedback: ", feedback)
                    return _CONTROLLER_ACTIVATED
                else:
                    print("\n Sorry I can't deliver Controller {0} as the use case is not implemented \n".format(input_for_controller["controller_name"]))
                    return _CONTROLLER_DEACTIVED
            except Exception:
                print("Message sending failed")
                return _CONTROLLER_DEACTIVED

        def kill(self, system_input, controller_name):
            input_for_controller = {"controller_name": controller_name, _DESCRIPTION: _KILLER}
            print(input_for_controller)

            try:
                if ((len(system_input["sinks"]) >= 1) & (len(system_input["sources"]) == 1) & (system_input["boosted"] == 'N')):
                    feedback = self.comms.send(input_for_controller)
                    print("Feedback: ", feedback)
                    return _CONTROLLER_DEACTIVED
            except Exception:
                print("Message sending failed")
                return _CONTROLLER_ACTIVATED


# deliver only the list of relevant component returning a dictionary stating the actuator and the feedback signal e.g. for the first use case will be pump x sensor and that's i
# where to decide the components to be used? if I do it here I won't take into account the posibility that a sensor/pump could be dead and replaced by another
# pump - if one sink use the pump of source, if there is booster use the booster
#       - if two sinks always use both pumps of each sink
# sensor -


        def components_name_translator(self, components):
            translated_components = []
            for component in components:
                translated_components.append(self.translator.components(component))
            return translated_components


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
                if ((actuator.object_type == ideal_actuator.type.data) & (actuator.location in locations)):
                    active_actuators.append(actuator.get_name())
            acts = {"actuators": active_actuators}
            return acts
