import sys
import syslab
_ACTIVE = 1
_ACTIVE_VALVE = 0  # active- inactive doesn't exist with the same previous logic
_INACTIVE = 0
_VALVE_STATUS = "valve_status"
_SENSOR_STATUS = "sensor_status"
_PUMP_STATUS = "pump_status"
_DESCRIPTION = "description"
_SENSORS = 'Sensor'
_PUMPS = 'Pump'
_VALVES = 'Valve'
_MULTIPLIER = 1000
_DISCARD_VALUE = -10000
# _BUILDING_NAME = "716-h1"


class components_status(object):

    def __init__(self, comms, name_translator):
        self.comms = comms
        self.translator = name_translator

    def run(self, configuration_components, excluded_components):

        active_components = {}
        #self.interface_syslab = syslab.HeatSwitchBoard(_BUILDING_NAME)
        sensors = configuration_components[_SENSORS]
        pumps = configuration_components[_PUMPS]
        valves = configuration_components[_VALVES]
        pumps_score = 0
        sensors_score = 0
        valves_score = 0
        excluded_pumps = excluded_components["Pumps"]
        excluded_valves = excluded_components["Valves"]
        excluded_sensors = excluded_components["Sensors"]


        #TODO handle return true false
        #bool = self.sensor_evaluation(sensors)
        bool_pumps = self.pumps_evaluation(pumps)
        bool_valves = self.valves_evaluation(valves)
        if (bool_pumps and bool_valves):
            pumps_active = [pump for pump in pumps if pump.status == _ACTIVE]
            sensors_active = [sensor for sensor in sensors if sensor.status == _ACTIVE]
            valves_active = [valve for valve in valves if valve.status == _ACTIVE]

            ''' Selection of components once the excluded have been removed'''
            active_components = {"Pumps_active": [pump for pump in pumps_active if pump.ID not in excluded_pumps],
                                 "Sensors_active": [sensor for sensor in sensors_active if sensor.ID not in excluded_sensors],
                                 "Valves_active": [valve for valve in valves_active if valve.ID not in excluded_valves]}

            how_many_where = {"Pumps_in_sources": sum((device.location == "source") | (device.location == "booster") for device in active_components["Pumps_active"]),
                              "Pumps_in_sinks": sum(device.location == "sink" for device in active_components["Pumps_active"]),
                              "Sensors_in_sources": sum((device.location == "source") | (device.location == "booster") for device in active_components["Sensors_active"]),
                              "Sensors_in_sinks": sum(device.location == "sink" for device in active_components["Sensors_active"]),
                              "Valves_in_sources": sum((device.location == "source") | (device.location == "booster") for device in active_components["Valves_active"]),
                              "Valves_in_sinks": sum(device.location == "sink" for device in active_components["Valves_active"])}

            '''you only care about valves' score to determine the best combo'''
            for valve in valves:
                valves_score += valve.opening_score * _MULTIPLIER
                #valves_score = 0

            components_score = {"Pumps_score": pumps_score,
                                "Sensors_score": sensors_score,
                                "Valves_score": valves_score}

            active_components = {**active_components, **how_many_where, **components_score}

            return active_components
        else:
            active_components = []
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

            else:
                # sensor.set_status(_INACTIVE)
                sensor.set_status(_ACTIVE)

    def pumps_evaluation(self, pumps):

        pumps_for_physical_layer = {}
        pumps_for_logical_layer = {}
        pumps_dic = {}

        for pump in pumps:
            pumps_for_physical_layer[self.translator.components(pump.ID)] = pump.ID
            pumps_dic[pump.ID] = pump

        pumps_for_physical_layer[_DESCRIPTION] = _PUMP_STATUS

        pumps_for_translation = self.comms.send(pumps_for_physical_layer)

        if pumps_for_translation:
            for pump in pumps_for_translation.keys():
                pumps_for_logical_layer[self.translator.reverse_components(pump)] = pumps_for_translation[pump]

        print(pumps_for_logical_layer)
        if (pumps_for_logical_layer):
                for pump in pumps_for_logical_layer.keys():
                        if isinstance(pumps_for_logical_layer[pump], float):
                            pumps_dic[pump].set_status(_ACTIVE)
                        else:
                            pumps_dic[pump].set_status(_INACTIVE)
                return True
        else:
            return False

    def valves_evaluation(self, valves):
        try:
            valves_for_physical_layer = {}
            valves_for_logical_layer = {}
            valves_dic = {}

            for valve in valves:
                valves_for_physical_layer[self.translator.components(valve.ID)] = valve.ID
                valves_dic[valve.ID] = valve

            valves_for_physical_layer[_DESCRIPTION] = _VALVE_STATUS

            valves_for_translation = self.comms.send(valves_for_physical_layer)

            if valves_for_translation:
                for valve in valves_for_translation.keys():
                    valves_for_logical_layer[self.translator.reverse_components(valve)] = valves_for_translation[valve]

            if (valves_for_logical_layer):
                    for valve in valves_for_logical_layer.keys():
                            if isinstance(valves_for_logical_layer[valve], float):
                                valves_dic[valve].set_status(_ACTIVE)
                                valves_dic[valve].score_calculator(valves_for_logical_layer[valve])
                            else:
                                valves_dic[valve].set_status(_INACTIVE)
                                valves_dic[valve].score_calculator(_DISCARD_VALUE)
                    return True
            else:
                return False
        except Exception:
            print(valves_for_logical_layer.keys())
            print(valves_dic.keys())
            sys.exit()
