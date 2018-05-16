import re
_ACTIVE = 1
_INACTIVE = 0


class components_status(object):

    def run(self, interface, interface_syslab, unique_nodes):

        sensors = []
        pumps = []
        valves = []
        active_components = {}

        for node in unique_nodes.keys():
            s_name = 'Sensor'
            if (re.match(s_name, node)):
                sensors.append(unique_nodes[node])
                print(unique_nodes[node])
                print(unique_nodes[node].status)
            p_name = 'Pump'
            if (re.match(p_name, node)):
                pumps.append(unique_nodes[node])
            v_name = 'Valve'
            if (re.match(v_name, node)):
                valves.append(unique_nodes[node])

        #self.sensor_evaluation(sensors, interface_syslab)
        #self.pumps_evaluation(pumps, interface_syslab)
        #self.valves_evaluation(valves, interface_syslab)

        active_components = {"Pumps_active": [pump for pump in pumps if pump.status == _ACTIVE],
                             "Sensors_active": [sensor for sensor in sensors if sensor.status == _ACTIVE],
                             "Valves_active": [valve for valve in valves if valve.status == _ACTIVE]}

        how_may_where = {"Pumps_in_sources": sum((device.location == "source") | (device.location == "booster") for device in active_components["Pumps_active"]),
                         "Pumps_in_sinks": sum(device.location == "sink" for device in active_components["Pumps_active"]),
                         "Sensors_in_sources": sum((device.location == "source") | (device.location == "booster") for device in active_components["Sensors_active"]),
                         "Sensors_in_sinks": sum(device.location == "sink" for device in active_components["Sensors_active"]),
                         "Valves_in_sources": sum((device.location == "source") | (device.location == "booster") for device in active_components["Valves_active"]),
                         "Valves_in_sinks": sum(device.location == "sink" for device in active_components["Valves_active"])}

        active_components = {**active_components, **how_may_where}

        return active_components

    def sensor_evaluation(self, sensors, interface_syslab):

        sensors_name_translator = {
            'Sensor_1HT4': interface_syslab.getFwdTemperature("Bay_4"), 'Sensor_1CT4': interface_syslab.getBackTemperature("Bay_4"), 'Sensor_1CF4': interface_syslab.getFlow("Bay_4"), 'Sensor_1E4': interface_syslab.getThermalPower("Bay_4"),
            'Sensor_1HT5': interface_syslab.getFwdTemperature("Bay_5"), 'Sensor_1CT5': interface_syslab.getBackTemperature("Bay_5"), 'Sensor_1CF5': interface_syslab.getFlow("Bay_5"), 'Sensor_1E5': interface_syslab.getThermalPower("Bay_5"),
            'Sensor_1HT6': interface_syslab.getFwdTemperature("Bay_6"), 'Sensor_1CT6': interface_syslab.getBackTemperature("Bay_6"), 'Sensor_1CF6': interface_syslab.getFlow("Bay_6"), 'Sensor_1E6': interface_syslab.getThermalPower("Bay_6"),
            'Sensor_1HT7': interface_syslab.getFwdTemperature("Bay_7"), 'Sensor_1CT7': interface_syslab.getBackTemperature("Bay_7"), 'Sensor_1CF7': interface_syslab.getFlow("Bay_7"), 'Sensor_1E7': interface_syslab.getThermalPower("Bay_7"),
            'Sensor_1HT8': interface_syslab.getFwdTemperature("Bay_8"), 'Sensor_1CT8': interface_syslab.getBackTemperature("Bay_8"), 'Sensor_1CF8': interface_syslab.getFlow("Bay_8"), 'Sensor_1E8': interface_syslab.getThermalPower("Bay_8")}

        for sensor in sensors:
            status = sensors_name_translator[sensor.ID].value
            if (status != "NaN"):
                sensor.set_status(_ACTIVE)
                print(sensor.status)
            else:
                sensor.set_status(_INACTIVE)

    def pumps_evaluation(self, pumps, interface_syslab):

        pump_name_translator = {
            'Pump_1C4': "Pump_Bay4",
            'Pump_1H5': "Pump_Bay5",
            'Pump_1H6': "Pump_Bay6",
            'Pump_1H7': "Pump_Bay7",
            'Pump_1H8': "Pump_Bay8"}

        for pump in pumps:
            print(pump.ID)
            print(pump_name_translator[pump.ID])
            status = interface_syslab.getPumpFlow(pump_name_translator[pump.ID])
            if (status.value != "NaN"):
                pump.set_status(_ACTIVE)
                print(pump)
                print(pump.status)
            else:
                pump.set_status(_INACTIVE)

    def valves_evaluation(self, valves, interface_syslab):

        valves_name_translator = {
            'Valve_2C4': "Bay_4L-Busbar_2R", 'Valve_1C4': "Bay_4L-Busbar_1R", 'Valve_1B4': "Bay_4H-Busbar_B", 'Valve_2H4': "Bay_4H-Busbar_2F", 'Valve_1H4': "Bay_4H-Busbar_1F", 'Valve_2B4': "Bay_4L-Busbar_B",
            'Valve_2C5': "Bay_5L-Busbar_1R", 'Valve_1C5': "Bay_5L-Busbar_2R", 'Valve_1B5': "Bay_5H-Busbar_B", 'Valve_2H5': "Bay_5H-Busbar_1F", 'Valve_1H5': "Bay_5H-Busbar_2F", 'Valve_2B5': "Bay_5L-Busbar_B",
            'Valve_2C6': "Bay_6L-Busbar_1R", 'Valve_1C6': "Bay_6L-Busbar_2R", 'Valve_1B6': "Bay_6H-Busbar_B", 'Valve_2H6': "Bay_6H-Busbar_1F", 'Valve_1H6': "Bay_6H-Busbar_2F", 'Valve_2B6': "Bay_6L-Busbar_B",
            'Valve_2H7': "Bay_7H-Busbar_1F", 'Valve_1H7': "Bay_7H-Busbar_2F", 'Valve_2C7': "Bay_7L-Busbar_1R", 'Valve_1C7': "Bay_7L-Busbar_2R",
            'Valve_2H8': "Bay_8H-Busbar_1F", 'Valve_1H8': "Bay_8H-Busbar_2F", 'Valve_2C8': "Bay_8L-Busbar_1R", 'Valve_1C8': "Bay_8L-Busbar_2R"}

        for valve in valves:
            #time.sleep(0.1)
            status = interface_syslab.getValvePosition(valves_name_translator[valve.ID])
            print(valve)
            print(status.value)
            if(status.value != "NaN"):
                valve.set_status(_ACTIVE)
            else:
                valve.set_status(_INACTIVE)
