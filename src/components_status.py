import re
import syslab
_ACTIVE = 1
_INACTIVE = 0
_BUILDING_NAME = "716-h1"
_SENSORS = 'Sensor'
_PUMPS = 'Pump'
_VALVES = 'Valve'
_MULTIPLIER = 1000


class components_status(object):

    def run(self, interface, configuration_components):


        active_components = {}
        self.interface_syslab = syslab.HeatSwitchBoard(_BUILDING_NAME)
        interface = 0
        sensors = configuration_components[_SENSORS]
        pumps = configuration_components[_PUMPS]
        valves = configuration_components[_VALVES]
        pumps_score = 0
        sensors_score = 0
        valves_score = 0

        self.sensor_evaluation(sensors)
        self.pumps_evaluation(pumps)
        self.valves_evaluation(valves)

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
            #valves_score += valve.opening_score * _MULTIPLIER
            valves_score = 0

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

        valves_name_translator = {
            'Valve_2C4': "Bay_4L-Busbar_2R", 'Valve_1C4': "Bay_4L-Busbar_1R", 'Valve_1B4': "Bay_4H-Busbar_B", 'Valve_2H4': "Bay_4H-Busbar_2F", 'Valve_1H4': "Bay_4H-Busbar_1F", 'Valve_2B4': "Bay_4L-Busbar_B",
            'Valve_2C5': "Bay_5L-Busbar_1R", 'Valve_1C5': "Bay_5L-Busbar_2R", 'Valve_1B5': "Bay_5H-Busbar_B", 'Valve_2H5': "Bay_5H-Busbar_1F", 'Valve_1H5': "Bay_5H-Busbar_2F", 'Valve_2B5': "Bay_5L-Busbar_B",
            'Valve_2C6': "Bay_6L-Busbar_1R", 'Valve_1C6': "Bay_6L-Busbar_2R", 'Valve_1B6': "Bay_6H-Busbar_B", 'Valve_2H6': "Bay_6H-Busbar_1F", 'Valve_1H6': "Bay_6H-Busbar_2F", 'Valve_2B6': "Bay_6L-Busbar_B",
            'Valve_2H7': "Bay_7H-Busbar_1F", 'Valve_1H7': "Bay_7H-Busbar_2F", 'Valve_2C7': "Bay_7L-Busbar_1R", 'Valve_1C7': "Bay_7L-Busbar_2R",
            'Valve_2H8': "Bay_8H-Busbar_1F", 'Valve_1H8': "Bay_8H-Busbar_2F", 'Valve_2C8': "Bay_8L-Busbar_1R", 'Valve_1C8': "Bay_8L-Busbar_2R"}

        for valve in valves:
            # time.sleep(0.1)
            status = self.interface_syslab.getValvePosition(valves_name_translator[valve.ID])
            print(valve)
            print(status.value)
            if(status.value != "NaN"):
                valve.set_status(_ACTIVE)
                valve.score_calculator(status.value)
            else:
                valve.set_status(_INACTIVE)
