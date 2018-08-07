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
meter_2 = "Bay_7"
main_meter = "Bay_4"
full_power = 1000
half = 0.5
full = 1
full_power = CM(full_power, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
half_position = CM(half, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
#full_position = CM(full, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
not_moved = True
valve_name = "Bay_3L-Busbar_2R"
valve_name_2 = "Bay_7L-Busbar_1R"
#interface.startPump(pump)
#interface.setPumpSetpoint(pump, full_power)
calc_position = 1
print("Starting the loop")
n = 1
#time.sleep(120)
while (time.time() - start_time) < 300:
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
    if ((time.time() - start_time) > 10 * n):
        n += 1
        print("Valve position is {0} and flow is {1}".format(calc_position, interface.getPumpFlow(pump).value))
        calc_position = calc_position - 0.05
        if calc_position >= 0.0:
            position = CM(calc_position, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
            interface.setValvePosition(valve_name_2, position)
        else:
            pass
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
df.to_csv('Valve_Installed_Char_4to3to7_ConstantP.csv', index=False, columns=["Time", "Pump_Head", "Pump_Flow", "Pump_RPM", "Meter_Flow",
                                                                              "Meter_Power", "Valve_Position", "Meter_Flow_2", "Meter_Power_2",
                                                                              "Valve_Position_2", "Main_meter_flow", "Main_meter_power"])

#df = pd.read_csv('Step_Load_Bay_3.csv', index_col=0)
plt.figure(1)
head = plt.subplot(611)
head.set_title("Head time response")
head.plot(time_passed, pump_head_response, 'k')

flow = plt.subplot(612)
flow.set_title("Flow time response")
flow.plot(time_passed, pump_flow_response, 'r')

rpm = plt.subplot(613)
rpm.set_title("RPM time response")
rpm.plot(time_passed, pump_rpm_response, 'b')

flow_s = plt.subplot(614)
flow_s.set_title("Flow time response")
flow_s.plot(time_passed, sensor_flow_response, 'r')

power = plt.subplot(615)
power.set_title("Thermal Power time response")
power.plot(time_passed, sensor_power_response, 'b')

power = plt.subplot(616)
power.set_title("Valve Position")
power.plot(time_passed, valve_position, 'b')

plt.figure(2)
flow_s = plt.subplot(311)
flow_s.set_title("Flow time response_2")
flow_s.plot(time_passed, sensor_flow_response_2, 'r')

power = plt.subplot(312)
power.set_title("Thermal Power time response_2")
power.plot(time_passed, sensor_power_response_2, 'b')

power = plt.subplot(313)
power.set_title("Valve Position_2")
power.plot(time_passed, valve_position_2, 'b')

plt.show()
plt.tight_layout()
plt.savefig('myfig.pdf', dpi=300)
