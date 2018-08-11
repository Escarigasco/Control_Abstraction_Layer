import syslab
import time
import matplotlib.pyplot as plt
import syslab.core.datatypes.CompositeMeasurement as CM
import syslab.core.datatypes.HeatCirculationPumpMode as PM
import pandas as pd
import csv

_MULTIPLIER = 1000000
_SOURCE = 1
_VALIDITY = 1
_ZERO = 0
_N = 10


interface = syslab.HeatSwitchBoard("716-h1")
pump = "Pump_Bay4"
constant_pressure = 3
start_time = time.time()
pump_head_response = []
pump_rpm_response = []
pump_flow_response = []
sensor_power_response = []
sensor_flow_response = []
total_flow_response = []
total_power_response = []
sensor_power_response_2 = []
sensor_flow_response_2 = []
valve_position = []
valve_position_2 = []
time_passed = []
meter = "Bay_3"
meter_2 = "Bay_2"
main_meter = "Bay_4"
full_power = 1000
half = 0.5
full = 1
full_power = CM(full_power, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
half_position = CM(half, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
#full_position = CM(full, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
first_time = True
valve_name = "Bay_2L-Busbar_1R"
valve_name_2 = "Bay_3L-Busbar_1R"
valve_1_position = [0.5, 0.6, 0.7, 0.8]
valve_2_position = [0.5, 0.4, 0.3, 0.2]
#interface.startPump(pump)
#interface.setPumpSetpoint(pump, full_power)
calc_position = 1
print("Starting the loop")
n = 0
time_sec = 0
#time.sleep(120)
try:
    while (time.time() - start_time) < 4000:
        time.sleep(0.001)
        pump_head_response.append(interface.getPumpHead(pump).value)
        pump_flow_response.append(interface.getPumpFlow(pump).value)
        pump_rpm_response.append(interface.getPumpRPM(pump).value)
        sensor_power_response.append(interface.getThermalPower(meter).value)
        sensor_flow_response.append(interface.getFlow(meter).value)
        sensor_power_response_2.append(interface.getThermalPower(meter_2).value)
        sensor_flow_response_2.append(interface.getFlow(meter_2).value)
        total_flow_response.append(interface.getFlow(main_meter).value)
        total_power_response.append(interface.getThermalPower(main_meter).value)
        valve_position.append(interface.getValvePosition(valve_name).value)
        valve_position_2.append(interface.getValvePosition(valve_name_2).value)
        time_passed.append(time.time() - start_time)
        #time_sec += time.time() - start_time
        #print(time_sec)

        '''
        if ((time.time() - start_time) > 60 * n) and first_time:
            print("Valve 1 position is {0} ".format(valve_1_position[n]))
            print("Valve 2 position is {0} ".format(valve_2_position[n]))
            position_1 = CM(valve_1_position[n], time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
            position_2 = CM(valve_2_position[n], time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
            interface.setValvePosition(valve_name, position_1)
            interface.setValvePosition(valve_name_2, position_2)
            n += 1
            if n == 4:
                first_time = False
        else:
            pass'''
        '''
        if ((time.time() - start_time) > 10 * n):
            n += 1
            print("Valve position is {0} and flow is {1}".format(calc_position, interface.getPumpFlow(pump).value))
            calc_position = calc_position - 0.05
            if calc_position >= 0.0:
                position = CM(calc_position, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                interface.setValvePosition(valve_name, position)


            else:
                if first_time:
                    calc_position = 0.0
                    position = CM(calc_position, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                    interface.setValvePosition(valve_name_2, position)
                    first_time = False'''
            #if not_moved:
            #    not_moved = False
            #    #interface.setValvePosition(valve_name, half_position)

    #interface.stopPump(pump)
    #interface.setValvePosition(valve_name, full_position)

    raw_data = {"Time": time_passed, "Pump_Head": pump_head_response,
                "Pump_Flow": pump_flow_response, "Pump_RPM": pump_rpm_response,
                "Meter_Flow": sensor_flow_response, "Meter_Power": sensor_power_response,
                "Valve_Position": valve_position, "Meter_Flow_2": sensor_flow_response_2, "Meter_Power_2": sensor_power_response_2,
                "Valve_Position_2": valve_position_2, "Main_meter_flow": total_flow_response, "Main_meter_power": total_power_response}
    df = pd.DataFrame(raw_data, columns=["Time", "Pump_Head", "Pump_Flow", "Pump_RPM", "Meter_Flow",
                                         "Meter_Power", "Valve_Position", "Meter_Flow_2", "Meter_Power_2",
                                         "Valve_Position_2", "Main_meter_flow", "Main_meter_power"])
    print(df)
    df.to_csv('test_controller_1_2_1_S4.csv', index=False, columns=["Time", "Pump_Head", "Pump_Flow", "Pump_RPM", "Meter_Flow",
                                                                                                  "Meter_Power", "Valve_Position", "Meter_Flow_2", "Meter_Power_2",
                                                                                                "Valve_Position_2", "Main_meter_flow", "Main_meter_power"])
except (KeyboardInterrupt, SystemExit):
    raw_data = {"Time": time_passed, "Pump_Head": pump_head_response,
                "Pump_Flow": pump_flow_response, "Pump_RPM": pump_rpm_response,
                "Meter_Flow": sensor_flow_response, "Meter_Power": sensor_power_response,
                "Valve_Position": valve_position, "Meter_Flow_2": sensor_flow_response_2, "Meter_Power_2": sensor_power_response_2,
                "Valve_Position_2": valve_position_2, "Main_meter_flow": total_flow_response, "Main_meter_power": total_power_response}

    data_length = []
    for data in raw_data.values():
        data_length.append(len(data))

    min_length = min(data_length)
    print("the min length is ", min_length)
    for data in raw_data.keys():
        print("this length is ", len(raw_data[data]))
        diff = len(raw_data[data]) - min_length
        raw_data[data] = raw_data[data][:len(raw_data[data]) - diff]

    df = pd.DataFrame(raw_data, columns=["Time", "Pump_Head", "Pump_Flow", "Pump_RPM", "Meter_Flow",
                                         "Meter_Power", "Valve_Position", "Meter_Flow_2", "Meter_Power_2",
                                         "Valve_Position_2", "Main_meter_flow", "Main_meter_power"])
    print(df)
    df.to_csv('test_controller_1_2_1_S4.csv', index=False, columns=["Time", "Pump_Head", "Pump_Flow", "Pump_RPM", "Meter_Flow",
                                                                            "Meter_Power", "Valve_Position", "Meter_Flow_2", "Meter_Power_2",
                                                                            "Valve_Position_2", "Main_meter_flow", "Main_meter_power"])
except Exception:
    raw_data = {"Time": time_passed, "Pump_Head": pump_head_response,
                "Pump_Flow": pump_flow_response, "Pump_RPM": pump_rpm_response,
                "Meter_Flow": sensor_flow_response, "Meter_Power": sensor_power_response,
                "Valve_Position": valve_position, "Meter_Flow_2": sensor_flow_response_2, "Meter_Power_2": sensor_power_response_2,
                "Valve_Position_2": valve_position_2, "Main_meter_flow": total_flow_response, "Main_meter_power": total_power_response}
    data_length = []
    for data in raw_data.values():
        data_length.append(len(data))

    min_length = min(data_length)
    print("the min length is ", min_length)
    for data in raw_data.keys():
        print("this length is ", len(raw_data[data]))
        diff = len(raw_data[data]) - min_length
        raw_data[data] = raw_data[data][:len(raw_data[data]) - diff]

    df = pd.DataFrame(raw_data, columns=["Time", "Pump_Head", "Pump_Flow", "Pump_RPM", "Meter_Flow",
                                         "Meter_Power", "Valve_Position", "Meter_Flow_2", "Meter_Power_2",
                                         "Valve_Position_2", "Main_meter_flow", "Main_meter_power"])
    print(df)
    df.to_csv('test_controller_1_2_1_S4.csv', index=False, columns=["Time", "Pump_Head", "Pump_Flow", "Pump_RPM", "Meter_Flow",
                                                                            "Meter_Power", "Valve_Position", "Meter_Flow_2", "Meter_Power_2",
                                                                            "Valve_Position_2", "Main_meter_flow", "Main_meter_power"])
