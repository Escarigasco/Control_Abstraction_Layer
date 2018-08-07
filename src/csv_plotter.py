
import time
import matplotlib.pyplot as plt
import pandas as pd
import csv

df = pd.read_csv('Valve_Installed_Char_4to3.csv')
time_passed = df['Time']
pump_head_response = df['Pump_Head']
pump_flow_response = df['Pump_Flow']
pump_rpm_response = df['Pump_RPM']
sensor_flow_response = df['Meter_Flow']
sensor_power_response = df['Meter_Power']
valve_position = df['Valve_Position']
#sensor_flow_response_2 = df['Meter_Flow_2']
#sensor_power_response_2 = df['Meter_Power_2']
#valve_position_2 = df['Valve_Position_2']
#total_power = df["Main_meter_power"]
#total_flow = df["Main_meter_flow"]

'''
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
flow_s = plt.subplot(611)
flow_s.set_title("Flow time response")
flow_s.plot(time_passed, sensor_flow_response, 'r')

power = plt.subplot(612)
power.set_title("Thermal Power time response")
power.plot(time_passed, sensor_power_response, 'b')

power = plt.subplot(613)
power.set_title("Valve Position")
power.plot(time_passed, valve_position, 'b')

flow_s = plt.subplot(614)
flow_s.set_title("Flow time response_2")
flow_s.plot(time_passed, sensor_flow_response_2, 'r')

power = plt.subplot(615)
power.set_title("Thermal Power time response_2")
power.plot(time_passed, sensor_power_response_2, 'b')

power = plt.subplot(616)
power.set_title("Valve Position_2")
power.plot(time_passed, valve_position_2, 'b')



plt.figure(3)
#head = plt.subplot(311)
#head.set_title("Installed Characteristic - opening against pump sensor")
#head.plot(valve_position, pump_flow_response, 'k')

#plt.figure(2)
head = plt.subplot(411)
head.set_title("Installed Characteristic - opening against Energy sensor")
head.plot(valve_position, sensor_flow_response, 'b')

#plt.figure(2)
head = plt.subplot(412)
head.set_title("Power Response - opening against Energy sensor")
head.plot(valve_position, sensor_power_response, 'b')

#plt.figure(2)
head = plt.subplot(413)
head.set_title("Installed Characteristic - opening against Energy sensor")
head.plot(valve_position_2, sensor_flow_response_2, 'b')

#plt.figure(2)
head = plt.subplot(414)
head.set_title("Power Response - opening against Energy sensor")
head.plot(valve_position_2, sensor_power_response_2, 'b')

plt.figure(3)
#head = plt.subplot(311)
#head.set_title("Installed Characteristic - opening against pump sensor")
#head.plot(valve_position, pump_flow_response, 'k')

#plt.figure(2)
plt.figure(4)
head = plt.subplot(311)
head.set_title("Flow Response 1")
head.plot(time_passed, sensor_flow_response, 'b')

#plt.figure(2)
head = plt.subplot(312)
head.set_title("Flow Response 2")
head.plot(time_passed, sensor_flow_response_2, 'b')

#plt.figure(2)
head = plt.subplot(313)
head.set_title("Total Flow")
head.plot(time_passed, total_flow, 'b')

plt.figure(5)
head = plt.subplot(411)
head.set_title("Power Response 1")
head.plot(time_passed, sensor_power_response, 'b')

#plt.figure(2)
head = plt.subplot(412)
head.set_title("Power Response 2")
head.plot(time_passed, sensor_power_response_2, 'b')

#plt.figure(2)
head = plt.subplot(413)
head.set_title("Total Power")
head.plot(time_passed, total_power, 'b')

#plt.figure(2)
head = plt.subplot(414)
head.set_title("Power_1 against its flow")
head.plot(sensor_flow_response, sensor_power_response, 'b')'''

plt.figure(6)
head = plt.subplot(311)
head.set_title("Power Response 1")
head.plot(valve_position, sensor_flow_response, 'b')

#plt.figure(2)
head = plt.subplot(312)
head.set_title("Power_1 against its flow")
head.plot(valve_position, sensor_power_response, 'b')

#plt.figure(2)
head = plt.subplot(313)
head.set_title("Power_1 against its flow")
head.plot(sensor_flow_response, sensor_power_response, 'b')



#plt.ion()
plt.show()
plt.tight_layout()
plt.savefig('Valve_Installed_Char_4to3.pdf', dpi=1000)
