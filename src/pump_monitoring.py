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
time_passed = []
meter = "Bay_4"
#half_head = 4
#half_power = CM(half_head, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
#mode = PM(constant_pressure, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
#interface.setPumpControlMode(pump, mode)
interface.startPump(pump)
#interface.setPumpSetpoint(pump, half_power)

print("Starting the loop")
while (time.time() - start_time) < 2:
    time.sleep(0.001)
    pump_head_response.append(interface.getPumpHead(pump).value)
    pump_flow_response.append(interface.getPumpFlow(pump).value)
    pump_rpm_response.append(interface.getPumpRPM(pump).value)
    sensor_power_response.append(interface.getThermalPower(meter).value)
    sensor_flow_response.append(interface.getFlow(meter).value)
    time_passed.append(time.time() - start_time)
interface.stopPump(pump)

raw_data = {"Time": time_passed, "Pump_Head": pump_head_response,
            "Pump_Flow": pump_flow_response, "Pump_RPM": pump_rpm_response,
            "Meter_Flow": sensor_flow_response, "Meter_Power": sensor_power_response}
df = pd.DataFrame(raw_data, columns=["Time", "Pump_Head", "Pump_Flow", "Pump_RPM", "Meter_Flow", "Meter_Power"])

print(df)
df.to_csv('3.3_pressure.csv', index=False, columns=["Time", "Pump_Head", "Pump_Flow", "Pump_RPM", "Meter_Flow", "Meter_Power"])


plt.figure(1)
head = plt.subplot(511)
head.set_title("Head time response")
head.plot(time_passed, pump_head_response, 'k')

flow = plt.subplot(512)
flow.set_title("Flow time response")
flow.plot(time_passed, pump_flow_response, 'r')

rpm = plt.subplot(513)
rpm.set_title("RPM time response")
rpm.plot(time_passed, pump_rpm_response, 'b')

flow_s = plt.subplot(514)
flow_s.set_title("Flow time response")
flow_s.plot(time_passed, sensor_flow_response, 'r')

power = plt.subplot(515)
power.set_title("Thermal Power time response")
power.plot(time_passed, sensor_power_response, 'b')

plt.show()
