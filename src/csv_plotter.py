
import time
import matplotlib.pyplot as plt
import pandas as pd
import csv

df = pd.read_csv('test_controller_1_2_1_S4.csv')
time_passed = df['Time']
pump_head_response = df['Pump_Head']
pump_flow_response = df['Pump_Flow']
pump_rpm_response = df['Pump_RPM']
sensor_flow_response = df['Meter_Flow']
sensor_power_response = df['Meter_Power']
valve_position = df['Valve_Position']
sensor_flow_response_2 = df['Meter_Flow_2']
sensor_power_response_2 = df['Meter_Power_2']
valve_position_2 = df['Valve_Position_2']
total_power = df["Main_meter_power"]
total_flow = df["Main_meter_flow"]

'''
plt.figure(1)
head = plt.subplot(611)
head.set_title("Flow 2 response")
head.plot(time_passed, sensor_flow_response, 'b')

head = plt.subplot(612)
head.set_title("Valve Position response")
head.plot(time_passed, valve_position, 'b')

#plt.figure(2)
head = plt.subplot(613)
head.set_title("Flow 2 response against Valve Position")
head.plot(valve_position, sensor_flow_response, 'b')

#plt.figure(2)
head = plt.subplot(614)
head.set_title("Flow  response")
head.plot(time_passed, sensor_flow_response_2, 'b')

#plt.figure(2)
head = plt.subplot(615)
head.set_title("Flow  response against Valve Position")
head.plot(valve_position, sensor_flow_response_2, 'b')


#plt.figure(2)
head = plt.subplot(616)
head.set_title("RPM Response")
head.plot(valve_position, pump_rpm_response, 'b')
'''



plt.figure(1)
head = plt.subplot(411)
head.set_title("Flow response")
head.plot(time_passed, sensor_flow_response, 'b')

head = plt.subplot(412)
head.set_title("Power response")
head.plot(time_passed, sensor_power_response, 'b')

#plt.figure(2)
head = plt.subplot(413)
head.set_title("Flow 2 response")
head.plot(time_passed, sensor_flow_response_2, 'b')

#plt.figure(2)
head = plt.subplot(414)
head.set_title("Power 2 Response")
head.plot(time_passed, sensor_power_response_2, 'b')


'''
plt.figure(3)
head = plt.subplot(511)
head.set_title("Valve Split Ratio over time")
head.plot(time_passed, valve_position * valve_position_2 ** (-1), 'b')

head = plt.subplot(512)
head.set_title("Valve 1 Response")
head.plot(time_passed, valve_position, 'b')

head = plt.subplot(513)
head.set_title("Valve 2 Response")
head.plot(time_passed, valve_position_2, 'b')

#plt.figure(2)
head = plt.subplot(514)
head.set_title("Ration Flow 1 / Flow 2 Response")
head.plot(time_passed, sensor_flow_response * sensor_flow_response_2 ** (-1), 'b')

#plt.figure(2)
head = plt.subplot(515)
head.set_title("Ration Flow 1 / Flow 2 against Valve Ratio")
head.plot(valve_position * valve_position_2 ** (-1), sensor_flow_response * sensor_flow_response_2 ** (-1), 'b')
'''




#plt.ion()
plt.show()
plt.tight_layout()
plt.savefig('Valve_Installed_Char_4to3.pdf', dpi=1000)
