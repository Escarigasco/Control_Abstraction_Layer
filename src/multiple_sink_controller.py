# import SWITCHBOARD_PYTHON_API
# remember that additional gain can be added by multiplying the error by a constant
# you could initialize this controller as a class when you initialize the logical layer and then call the method that start the thread every time you need it
'''THE CONTROL TIME WILL EVENTUALLY GO IN THE CONFIGURATION FILE AS IT WILL BE DIFFERENT FROM CONTANT PRESSURE TO CONSTANT FLOW OR WHATEVER'''
import matplotlib.pyplot as plt
from multiprocessing import Queue
import math
import numpy as np
import pickle
import signal
import sys
import syslab
import syslab.core.datatypes.CompositeMeasurement as CM
import syslab.core.datatypes.HeatCirculationPumpMode as PM
import time
_BUILDING_NAME = "716-h1"
'''actuator time constant'''
_INTEGRAL_TIME = 40
'''this is sensor time constant'''
_CONTROLLER_TIME_DELAY = 50
_ACQUISITION_TIME = 1
_MULTIPLIER = 0.000001
_OFF = "OFF"
_BEGIN_WITH = 0
_MINUTES_THRESHOLDS = 100
_SOURCE = 1
_VALIDITY = 1
_ZERO = 0
_MIN_SAT = 0.3
_MAX_SAT = 0.9
_MIN_WIN = -0.20
_MAX_WIN = 0.20
_PUMP_VARIATION = 20
_MAX_SUM = 1.4
_MIN_SUM = 0.7
_HOUR_CONVERTER = 3600
_LITER_CONVERTER = 1000
_DENSITY = 999
_Cp = 4.186


class controller_constant_pressure(object):

    def PID_controller(self, inputs, process_ID, queue):
        inputs = pickle.loads(inputs)
        print(inputs)
        inputs = {'controller_name': "['Source_1BH4']['Sink_1DL3']['Sink_1DL2']N", 'description': 'creator',
                  'gain': '1', 'kp': '0', 'ki': '0.07', 'kd': '0', 'ki_valve': '0.07', 'pumps_of_circuit': ['Pump_Bay4', 'Pump_Bay3'],
                  'circulator': ['Pump_Bay4'], 'circulator_mode': '4', 'actuator': ['Bay_2L-Busbar_1R', 'Bay_3L-Busbar_1R'], 'setpoint': [5, 3],
                  'feedback_sensor': ['Bay_2', 'Bay_3'], 'valves': ['Bay_4L-Busbar_2R', 'Bay_4H-Busbar_1F', 'Bay_3H-Busbar_2F', 'Bay_3L-Busbar_1R'],
                  'sources_meters': ['Bay_4']}
        print("Controller Constant Pressure Started")
        interface = syslab.HeatSwitchBoard(_BUILDING_NAME)
        plt.show()
        plt.ion()
        self.xdata = [[], []]
        self.ydata = [[], []]
        f, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.ax1.set_xlim(0, 100)
        self.ax1.set_ylim(-50, +50)
        self.ax1.set_xlabel('Time [s]', fontsize=10)
        self.ax1.set_ylabel('Thermal Power [kW]', fontsize=10)
        self.ax2.set_xlim(0, 100)
        self.ax2.set_ylim(-50, +50)
        self.ax2.set_xlabel('Time [s]', fontsize=10)
        self.ax2.set_ylabel('Thermal Power [kW]', fontsize=10)
        self.line, = self.ax1.plot(self.xdata[0], self.ydata[0], 'r-')
        self.line2, = self.ax2.plot(self.xdata[1] * 2, self.ydata[1], 'b-')
        self.line.set_xdata(self.xdata)
        self.line.set_ydata(self.ydata)
        self.plot_array = [self.ax1, self.ax2]
        self.line_array = [self.line, self.line2]

        self.thresholds = []
        start_time = time.time()
        self.n = 0
        self.work_q = queue
        first_call = True
        print("Control Process {0} started".format(process_ID))
        print("I am process", process_ID)
        #inputs = pickle.loads(inputs)
        print(inputs)
        self.process_ID = process_ID
        max = 100
        min = 0
        pumps_of_circuit = inputs["pumps_of_circuit"]
        kp = float(inputs["kp"])
        kd = float(inputs["kd"])
        ki = float(inputs["ki"])
        gain = float(inputs["gain"])
        circulators = inputs["circulator"]
        circulator_mode = int(inputs["circulator_mode"])
        print(circulator_mode)
        feedback_sensor = inputs["feedback_sensor"]
        actuators = inputs["actuator"]

        setpoint = [float(n) for n in inputs["setpoint"]]
        feedback_value = [float(_BEGIN_WITH)] * len(feedback_sensor)
        integral = [float(_BEGIN_WITH)] * len(feedback_sensor)

        half = 0.5
        half = CM(half, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        for actuator in actuators:
            interface.setValvePosition(actuator, half)

        for n in range(0, len(integral)):
            integral[n] = 0.5  # interface.getValvePosition(actuators[n]).value


        controller_output = [float(_BEGIN_WITH)] * len(actuators)
        actuator_signal = [float(_BEGIN_WITH)] * len(actuators)
        error_value = [float(_BEGIN_WITH)] * len(feedback_sensor)
        self.thresholds = [_BEGIN_WITH] * len(feedback_sensor)
        CompositMess = [_BEGIN_WITH] * len(actuators)
        historical_position = [_BEGIN_WITH] * len(actuators)
        '''
        n = 0
        for actuator in actuators:
            controller_output[n] = interface.getValvePosition(actuator).value
            n += 1'''
        for n in range(0, len(feedback_sensor)):
            title = "Time Response Signal Sensor " + feedback_sensor[n]
            self.plot_array[n].set_title(title)
        if len(feedback_sensor) < len(self.plot_array):
            title = "No more sensors"
            self.plot_array[-1].set_title(title)

        shut_down_signal = 0

        mode = PM(circulator_mode, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        for pump in pumps_of_circuit:
            if pump not in circulators:
                print(circulator_mode)
                interface.stopPump(pump)
                time.sleep(0.2)
                print("Pump ", pump, "has been stopped")

        #optimum_pressure = self.find_optimum_pressure(circulators, interface, sources_meters)
        optimum_pressure = 100
        optimum_pressure = CM(optimum_pressure, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        for pump in circulators:
            interface.startPump(pump)
            interface.setPumpControlMode(pump, mode)
            interface.setPumpSetpoint(pump, optimum_pressure)
            #interface.setMaxFlowLimit(pump, flow_limit)
            time.sleep(0.2)
            print("Pump ", pumps_of_circuit[n], "was started")

        time.sleep(30)
        start_time = time.time()

        proportional_start = time.time()
        signal.signal(signal.SIGTERM, self.signal_term_handler)
        counter = 0
        counter_min = 0
        check_valves = True
        while(1):

            #try:
                stop_time = time.time()
                if (not self.work_q.empty()):
                    received_setpoint = self.work_q.get()
                    setpoint = [float(n) for n in received_setpoint]
                    self.n = 0
                    self.threshold = [_BEGIN_WITH] * len(feedback_sensor)

                print("Control Thread {0} running".format(process_ID))
                for n in range(_BEGIN_WITH, len(feedback_sensor)):
                    print(n)
                    #feedback_value[n] = 1
                    feedback_value[n] = float(interface.getThermalPower(feedback_sensor[n]).value)

                    if not isinstance(feedback_value[n], float):
                        feedback_value[n] = 0     # --->>> really bad though
                        print("It was nan")
                    print("The Pumps are running at setpoint ", optimum_pressure.value)
                    print("feedback taken from sensor {0} with setpoint {1} is kW {2}".format(feedback_sensor[n], setpoint[n], feedback_value[n]))
                    print("The actuator signal is {0}".format(actuator_signal[n]))
                    print("Setpoint {0} was sent to actuator {1}".format(actuator_signal[n], actuators[n]))
                    print("The control output for ", actuators[n], " is ", controller_output[n])
                    print("The integral for ", actuators[n], " is ", integral[n])
                    self.ydata[n].append(feedback_value[n])  # Save as previous error.
                    self.xdata[n].append(time.time() - start_time)

                    historical_position[n] = interface.getValvePosition(actuators[n]).value
                    self.update_line()

                if stop_time - proportional_start > _CONTROLLER_TIME_DELAY:
                    for n in range(_BEGIN_WITH, len(feedback_sensor)):
                        error_value[n] = setpoint[n] - feedback_value[n]    # Calculate the error

                        '''this below is the real PID action as the controller action is really related to the errorr'''
                        print("The Pumps are running at setpoint ", optimum_pressure)
                        print("this is the error ", error_value[n])
                        integral[n] = integral[n] + ki * error_value[n]  # - windup_corrector[n]              # Calculate integral
                        integral[n] = self.anti_windup(integral[n])
                        print("The integral for ", actuators[n], " is ", integral[n])
                        controller_output[n] = kp * error_value[n] + integral[n]
                        print("The proportional action is ", kp * error_value[n])
                        print("The integral action is ", integral[n])
                        print("this is the controller output ", controller_output[n])

                    controller_output = self.apply_corrector_factor(historical_position, controller_output, ki, feedback_sensor, interface)
                    integral = controller_output
                    #time.sleep(2)
                    for n in range(_BEGIN_WITH, len(feedback_sensor)):
                        actuator_signal[n] = self.saturation(controller_output[n])
                        print("The actuator signal is corrected with corrector is  ", actuator_signal[n])
                        CompositMess[n] = CM(actuator_signal[n], time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                        interface.setValvePosition(actuators[n], CompositMess[n])
                    proportional_start = time.time()

                #if (sum(controller_output) > _MAX_SUM):
                if check_valves:
                    for output in integral:
                        if output >= _MAX_SAT:
                            counter += 1
                        elif output <= _MIN_SAT:
                            counter_min += 1
                print("counter ", counter)
                print("counter_min ", counter_min)

                if (counter >= 1 or counter_min >= 1):
                    check_valves = False
                    if first_call:
                        print("60s start from here")
                        start_time = time.time()
                        first_call = False
                    if (time.time() - start_time) >= _CONTROLLER_TIME_DELAY * 2:
                        print("I am adjusting pump setpoint")
                        for pump in circulators:
                            optimum_pressure = optimum_pressure.value + counter * _PUMP_VARIATION - counter_min * _PUMP_VARIATION
                            if optimum_pressure > 100:
                                optimum_pressure = 100
                            elif optimum_pressure < 0:
                                optimum_pressure = 0
                            optimum_pressure = CM(optimum_pressure, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                            print("Pump {0} was reduced to {1}".format(pump, optimum_pressure))
                            for pump in circulators:
                                interface.setPumpSetpoint(pump, optimum_pressure)
                        start_time = time.time()
                        counter = 0
                        counter_min = 0
                        check_valves = True
                else:
                    first_call = True



                #if stop_time - integral_start > _INTEGRAL_TIME:
                #    for n in range(_BEGIN_WITH, len(feedback_sensor)):
                #        error_value[n] = setpoint[n] - feedback_value[n]    # Calculate the error
                #        integral[n] = integral[n] + ki * error_value[n]  # - windup_corrector[n]              # Calculate integral
                #        integral[n] = self.anti_windup(integral[n])
                #        controller_output[n] = controller_output[n] + integral[n]
                #        print("The integral action is ", integral[n])
                #        print("this is the controller output ", controller_output[n])

                #        '''this below is the real PID action as the controller action is really related to the errorr'''
                #        actuator_signal[n] = controller_output[n]
                #        actuator_signal[n] = self.saturation(actuator_signal[n])
                #        print("The actuator signal is ", actuator_signal[n])

                #        CompositMess[n] = CM(actuator_signal[n], time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                #        interface.setValvePosition(actuators[n], CompositMess[n])
                #    integral_start = time.time()'''

                time.sleep(_ACQUISITION_TIME)

            #except (KeyboardInterrupt, SystemExit):
            #    for circulator in circulators:
            #        interface.stopPump(pump)
            #        print("Circulator {0} is now at zero flow".format(circulator))
            #    sys.exit(0)
            #except Exception:
            #    '''there is the condition because it will keep except'''
                #self.shut_down_routine(pumps_of_circuit, valves, interface)
            #    sys.exit(0)

    def anti_windup(self, integral_error):
        '''to be confirmed if we want a minimum of wind up tolerance'''
        if integral_error > _MAX_SAT:
            integral_error = integral_error - (integral_error - _MAX_SAT)
        elif integral_error < _MIN_SAT:
            integral_error = integral_error + (_MIN_SAT - integral_error)
        else:
            pass
        return integral_error

    def saturation(self, actuator_signal):
        if actuator_signal <= _MIN_SAT:
            actuator_signal = _MIN_SAT
        elif actuator_signal >= _MAX_SAT:
            actuator_signal = _MAX_SAT
        return actuator_signal

    def signal_term_handler(self, signal, frame):
        print('got SIGTERM - the process was killed as the configuration was not matched any more')
        sys.exit(0)

    def pump_setpoint_converter(self, volume_flow):
        pump_max_volume_flow = 10 # this is correct
        volume_flow_in_percent = 100 * (volume_flow / pump_max_volume_flow)
        return volume_flow_in_percent

    def shut_down_routine(self, pumps_of_circuit, valves, interface):
        shut_down_signal = 0
        CompositMess = CM(shut_down_signal, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        for pump in pumps_of_circuit:
            print("Circulators are off")
            interface.stopPump(pump)
        for valve in valves:
            print("Valves are closed")
            #interface.setPumpSetpoint(valve, CompositMess)

    def update_line(self):
        max_dimension = 50
        removable = 20
        limits = 10
        n = 0
        #print(len(self.xdata[0]))
        for plot in self.plot_array:
            if (self.xdata[n]):
                    plot.set_xlim(max(self.xdata[n]) - limits, max(self.xdata[n]) + limits)
                    plot.set_ylim(max(self.ydata[n]) - limits, max(self.ydata[n]) + limits)
                    self.line_array[n].set_xdata(self.xdata[n])
                    self.line_array[n].set_ydata(self.ydata[n])
                    if len(self.xdata[n]) > max_dimension:
                        del self.xdata[n][:removable]
                        del self.ydata[n][:removable]
            n += 1

        plt.draw()
        plt.pause(1e-17)

    '''if you set the pressure at the top you are fine because you will be running over the last rpm and at the point that meet the system curve'''
    def find_optimum_pressure(self, circulators, interface, sources_meters):
        print("I am looking for the optimum")
        pressure = 95
        try_flow = 0
        cumulative_flow = 0
        while pressure < 100:
            pressure += 5
            print("The pump setpoint is ", pressure)
            for pump in circulators:
                CompositPressure = CM(pressure, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                interface.setPumpSetpoint(pump, CompositPressure)
            time.sleep(1)
            for meter in sources_meters:
                cumulative_flow += interface.getFlow(meter).value
                print("the cumulative flow is ", cumulative_flow)
            if cumulative_flow > try_flow:
                try_flow = cumulative_flow
                optimum_pressure = pressure
                print("the optimum_pressure is ", optimum_pressure)
            cumulative_flow = 0

        return optimum_pressure

    '''if you set the pressure at the top you are fine because you will be running over the last rmp'''
    def apply_corrector_factor(self, hist_position, control_output, ki, feedback_sensors, interface):
        print("This are the new position ", control_output)
        #time.sleep(3)
        DT = []
        corrector_factor = []
        total_flow = 0
        for sensor in feedback_sensors:
            total_flow += interface.getFlow(sensor).value
            T_f = interface.getFwdTemperature(sensor).value
            T_r = interface.getBackTemperature(sensor).value
            DT.append(T_f - T_r)

        total_flow = total_flow / (_LITER_CONVERTER * _HOUR_CONVERTER)
        print("I am looking for corrector factor")
        kvs = 1.6

        for n in range(_BEGIN_WITH, len(control_output)):
            control_output[n] = self.saturation(control_output[n])

        differences = [_BEGIN_WITH] * len(hist_position)

        print("This are the hisrotical position ", hist_position)
        print("This are the new position ", control_output)
        n = 0
        for n in range(_BEGIN_WITH, len(hist_position)):
            differences[n] = hist_position[n] - control_output[n]
        print("This are the differences ", differences)
        trend = np.prod(differences)
        VP_1i = hist_position[0]
        VP_2i = hist_position[1]
        VP_1f = control_output[0]
        VP_2f = control_output[1]
        n = 0
        corrector_factor.append((math.sqrt(1 / (kvs**2 * VP_2i**2)) / (math.sqrt(1 / (kvs**2 * VP_1i**2)) + math.sqrt(1 / (kvs**2 * VP_2i**2))) -
                                 math.sqrt(1 / (kvs**2 * VP_2f**2)) / (math.sqrt(1 / (kvs**2 * VP_1f**2)) + math.sqrt(1 / (kvs**2 * VP_2f**2)))))
        corrector_factor.append((math.sqrt(1 / (kvs**2 * VP_1i**2)) / (math.sqrt(1 / (kvs**2 * VP_1i**2)) + math.sqrt(1 / (kvs**2 * VP_2i**2))) -
                                 math.sqrt(1 / (kvs**2 * VP_1f**2)) / (math.sqrt(1 / (kvs**2 * VP_1f**2)) + math.sqrt(1 / (kvs**2 * VP_2f**2)))))
        if trend < 0:
            print("One is closing and the other opening")
            n = 0
            for n in range(_BEGIN_WITH, len(differences)):
                if (differences[n] < 0):
                    DP = float(total_flow * _Cp * _DENSITY * DT[n] * corrector_factor[n])
                    control_output[n] = control_output[n] + (DP * ki)
                    print("I am applying the correction ", DP)
            print("The corrector factor is {0}".format(corrector_factor))
        if ((trend > 0) and (differences[0] > 0)):
            print("They are both opening but the lowest should be reduced")
            n = 0
            index = differences.index(max(differences))
            for n in range(_BEGIN_WITH, len(differences)):
                if n == index:
                    DP = float(total_flow * _Cp * _DENSITY * DT[n] * corrector_factor[n])
                    control_output[n] = control_output[n] + (DP * ki)
                    print("I am applying the correction ", DP)
        print("The flow total was ", total_flow)
        print("The DT was ", DT)
        print("This are the new adjusted position ", control_output)
        #time.sleep(3)
        for n in range(_BEGIN_WITH, len(control_output)):
            control_output[n] = self.saturation(control_output[n])

        return control_output


if __name__ == "__main__":
    test = controller_constant_pressure()
    '''input_for_controller = {'controller_name': "['Source_1BH4']['Sink_1H7']N", 'description': 'creator',
                            'gain': '1.5', 'kp': '0.2', 'ki': '0.1', 'kd': '0', 'pumps_of_circuit': ['Pump_Bay4', 'Pump_Bay7'],
                            'circulator': ['Pump_Bay4'], 'circulator_mode': '3', 'actuator': ['Bay_7L-Busbar_2R'],
                            'setpoint': [1], 'feedback_sensor': ['Bay_7'], 'valves': ['Bay_4L-Busbar_2R', 'Bay_4H-Busbar_1F', 'Bay_7H-Busbar_2F', 'Bay_7L-Busbar_1R']}'''
    '''input_for_controller = {'controller_name': "['Source_1BH4']['Source_1DH6']['Sink_1H7']N", 'description': 'creator',
                            'gain': '1.5', 'kp': '0.2', 'ki': '0.1', 'kd': '0', 'pumps_of_circuit': ['Pump_Bay4', 'Pump_Bay6', 'Pump_Bay7'],
                            'circulator': ['Pump_Bay4', 'Pump_Bay6'], 'circulator_mode': '3', 'actuator': ['Bay_7L-Busbar_2R'],
                            'setpoint': [1], 'feedback_sensor': ['Bay_7'], 'valves': ['Bay_4L-Busbar_2R', 'Bay_4H-Busbar_1F', 'Bay_7H-Busbar_2F', 'Bay_7L-Busbar_1R']}'''
    input_for_controller = {'controller_name': "['Source_1BH4']['Source_1DH6']['Sink_1H7']['Sink_1H8']N", 'description': 'creator',
                            'gain': '1.5', 'kp': '0.2', 'ki': '0.1', 'kd': '0', 'pumps_of_circuit': ['Pump_Bay4', 'Pump_Bay6', 'Pump_Bay7', 'Pump_Bay8'],
                            'circulator': ['Pump_Bay4', 'Pump_Bay6'], 'circulator_mode': '3', 'actuator': ['Bay_7L-Busbar_2R', 'Bay_8L-Busbar_2R'],
                            'setpoint': [1, 1], 'feedback_sensor': ['Bay_7', 'Bay_8'], 'valves': ['Bay_4L-Busbar_2R', 'Bay_4H-Busbar_1F', 'Bay_7H-Busbar_2F', 'Bay_7L-Busbar_1R']}


    queue = Queue()
    inputs = pickle.dumps(input_for_controller)
    test.PID_controller(inputs, input_for_controller['controller_name'], queue)
