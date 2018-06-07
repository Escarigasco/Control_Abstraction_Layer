from name_translator import name_translator
import re
import syslab
import sys
_ACTIVE = 1
_ACTIVE_VALVE = 0.1
_INACTIVE_VALVE = 0
_VALVE_STATUS = "valve_status"
_DESCRIPTION = "description"
_SENSORS = 'Sensor'
_PUMPS = 'Pump'
_VALVES = 'Valve'
_MULTIPLIER = 1000
_BUILDING_NAME = "716-h1"


class components_status(object):

    def __init__(self, comms, name_translator):
        self.comms = comms
        self.translator = name_translator

    def run(self, configuration_components):

        active_components = {}
        #self.interface_syslab = syslab.HeatSwitchBoard(_BUILDING_NAME)
        interface = 0
        sensors = configuration_components[_SENSORS]
        pumps = configuration_components[_PUMPS]
        valves = configuration_components[_VALVES]
        pumps_score = 0
        sensors_score = 0
        valves_score = 0

        #TODO handle return true false
        #bool = self.sensor_evaluation(sensors)
        #bool = self.pumps_evaluation(pumps)
        bool = self.valves_evaluation(valves)

        active_components = {"Pumps_active": [pump for pump in pumps if pump.status == _ACTIVE],
                             "Sensors_active": [sensor for sensor in sensors if sensor.status == _ACTIVE],
                             "Valves_active": [valve for valve in valves if valve.status == _ACTIVE]}

        how_many_where = {"Pumps_in_sources": sum((device.location == "source") | (device.location == "booster") for device in active_components["Pumps_active"]),
                          "Pumps_in_sinks": sum(device.location == "sink" for device in active_components["Pumps_active"]),
                          "Sensors_in_sources": sum((device.location == "source") | (device.location == "booster") for device in active_components["Sensors_active"]),
                          "Sensors_in_sinks": sum(device.location == "sink" for device in active_components["Sensors_active"]),
                          "Valves_in_sources": sum((device.location == "source") | (device.location == "booster") for device in active_components["Valves_active"]),
                          "Valves_in_sinks": sum(device.location == "sink" for device in active_components["Valves_active"])}

        '''let's keep ot simple for now and we use only the valves'''
        for pump in pumps:
            #pumps_score += pump.status * _MULTIPLIER
            pumps_score = 0
        for sensor in sensors:
            #sensors_score += sensor.status * _MULTIPLIER
            sensors_score = 0
        for valve in valves:
            print(valve)
            valves_score += valve.opening_score * _MULTIPLIER
            #valves_score = 0

        components_score = {"Pumps_score": pumps_score,
                            "Sensors_score": sensors_score,
                            "Valves_score": valves_score}

        active_components = {**active_components, **how_many_where, **components_score}

        return active_components

    def sensor_evaluation(self, sensors):

        sensors_name_translator = {
            'Sensor_1HT4': self.interface_syslab.getFwdTemperature("Bay_4"), 'Sensor_1CT4': self.interface_syslab.getBackTemperature("Bay_4"), 'Sensor_1CF4': self.interface_syslab.getFlow("Bay_4"), 'Sensor_1E4': self.interface_syslab.getThermalPower("Bay_4"),
            'Sensor_1HT5': self.interface_syslab.getFwdTemperature("Bay_5"), 'Sensor_1CT5': self.interface_syslab.getBackTemperature("Bay_5"), 'Sensor_1CF5': self.interface_syslab.getFlow("Bay_5"), 'Sensor_1E5': self.interface_syslab.getThermalPower("Bay_5"),
            'Sensor_1HT6': self.interface_syslab.getFwdTemperature("Bay_6"), 'Sensor_1CT6': self.interface_syslab.getBackTemperature("Bay_6"), 'Sensor_1CF6': self.interface_syslab.getFlow("Bay_6"), 'Sensor_1E6': self.interface_syslab.getThermalPower("Bay_6"),
            'Sensor_1HT7': self.interface_syslab.getFwdTemperature("Bay_7"), 'Sensor_1CT7': self.interface_syslab.getBackTemperature("Bay_7"), 'Sensor_1CF7': self.interface_syslab.getFlow("Bay_7"), 'Sensor_1E7': self.interface_syslab.getThermalPower("Bay_7"),
            'Sensor_1HT8': self.interface_syslab.getFwdTemperature("Bay_8"), 'Sensor_1CT8': self.interface_syslab.getBackTemperature("Bay_8"), 'Sensor_1CF8': self.interface_syslab.getFlow("Bay_8"), 'Sensor_1E8': self.interface_syslab.getThermalPower("Bay_8")}

        for sensor in sensors:
            status = sensors_name_translator[sensor.ID].value
            if (status != "NaN"):
                sensor.set_status(_ACTIVE)
                print(sensor.status)
            else:
                # sensor.set_status(_INACTIVE)
                sensor.set_status(_ACTIVE)

    def pumps_evaluation(self, pumps):

        pump_name_translator = {
            'Pump_1C4': "Pump_Bay4",
            'Pump_1H5': "Pump_Bay5",
            'Pump_1H6': "Pump_Bay6",
            'Pump_1H7': "Pump_Bay7",
            'Pump_1H8': "Pump_Bay8"}

        for pump in pumps:
            print(pump.ID)
            print(pump_name_translator[pump.ID])
            status = self.interface_syslab.getPumpFlow(pump_name_translator[pump.ID])
            if (status.value != "NaN"):
                pump.set_status(_ACTIVE)
                print(pump)
                print(pump.status)
            else:
                # pump.set_status(_INACTIVE)
                pump.set_status(_ACTIVE)

    def valves_evaluation(self, valves):
        valves_for_physical_layer = {}
        valves_for_logical_layer = {}
        valves_dic = {}

        for valve in valves:
            valves_for_physical_layer[self.translator.valves(valve.ID)] = valve.ID
            valves_dic[valve.ID] = valve

        valves_for_physical_layer[_DESCRIPTION] = _VALVE_STATUS

        valves_for_translation = self.comms.send(valves_for_physical_layer)

        for valve in valves_for_translation.keys():
            print(valves_for_translation)
            valves_for_logical_layer[self.translator.reverse_valves(valve)] = valves_for_translation[valve]
            #valves_for_logical_layer.pop(valve)

        print(valves_for_logical_layer)
        if (valves_for_logical_layer):
                for valve in valves_for_logical_layer.keys():
                        if (valves_for_logical_layer[valve] >= _ACTIVE_VALVE):
                            valves_dic[valve].set_status(_ACTIVE)
                            valves_dic[valve].score_calculator(valves_for_logical_layer[valve])
                        else:
                            valves_dic[valve].set_status(_INACTIVE_VALVE)
                            valves_dic[valve].score_calculator(valves_for_logical_layer[valve])
                return True
        else:
            return False
