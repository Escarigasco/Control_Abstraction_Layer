# import SWITCHBOARD_PYTHON_API
# remember that additional gain can be added by multiplying the error by a constant
# you could initialize this controller as a class when you initialize the logical layer and then call the method that start the thread every time you need it
'''THE CONTROL TIME WILL EVENTUALLY GO IN THE CONFIGURATION FILE AS IT WILL BE DIFFERENT FROM CONTANT PRESSURE TO CONSTANT FLOW OR WHATEVER'''
import matplotlib.pyplot as plt
from multiprocessing import Queue
import numpy
import pickle
import signal
import sys
import syslab
import syslab.core.datatypes.CompositeMeasurement as CM
import syslab.core.datatypes.HeatCirculationPumpMode as PM
import time
_BUILDING_NAME = "716-h1"
_CONTROL_TIME = 25
_ACQUISITION_TIME = 1
_MULTIPLIER = 0.000001
_OFF = "OFF"
_BEGIN_WITH = 0
_MINUTES_THRESHOLDS = 100
_SOURCE = 1
_VALIDITY = 1
_ZERO = 0
_MIN_SAT_PUMP = 41
_MAX_SAT_PUMP = 100
_MIN_SAT_VALVE = 0.3
_MAX_SAT_VALVE = 1
_TOLERANCE = 0.1


class controller_constant_curve(object):

    def PID_controller(self, inputs, process_ID, queue):
        inputs = pickle.loads(inputs)
        print(inputs)
        inputs = {'controller_name': "['Source_1BH4']['Sink_1DL3']N", 'description': 'creator',
                  'gain': '1', 'kp': '4', 'ki': '7', 'kd': '0', 'ki_valve': '0.1', 'pumps_of_circuit': ['Pump_Bay6', 'Pump_Bay3', 'Pump_Bay4'],
                  'circulator': ['Pump_Bay4', 'Pump_Bay6'], 'circulator_mode': '0', 'actuator': ['Pump_Bay4', 'Pump_Bay6' ], 'setpoint': [4],
                  'feedback_sensor': ['Bay_3'], 'valves': ['Bay_4L-Busbar_2R', 'Bay_4H-Busbar_1F', 'Bay_3H-Busbar_2F', 'Bay_3L-Busbar_1R']}
        print("Controller Constant Flow Started")
        interface = syslab.HeatSwitchBoard(_BUILDING_NAME)
        plt.show()
        plt.ion()
        self.xdata = [[], []]
        self.ydata = [[], []]
        f, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.ax1.set_xlim(0, 100)
        self.ax1.set_ylim(-50, +50)
        self.ax2.set_xlim(0, 100)
        self.ax2.set_ylim(-50, +50)
        self.line, = self.ax1.plot(self.xdata[0], self.ydata[0], 'r-')
        self.line2, = self.ax2.plot(self.xdata[1] * 2, self.ydata[1], 'b-')
        self.line.set_xdata(self.xdata)
        self.line.set_ydata(self.ydata)
        self.plot_array = [self.ax1, self.ax2]
        self.line_array = [self.line, self.line2]

        self.thresholds = []
        control_time = 25
        start_time = time.time()
        self.n = 0
        self.work_q = queue
        first_call = True
        stopper = False
        active_circuit = True
        print("Control Process {0} started".format(process_ID))
        print("I am process", process_ID)
        self.process_ID = process_ID
        max = 100
        min = 0
        valve_reg = False
        pumps_of_circuit = inputs["pumps_of_circuit"]
        kp = float(inputs["kp"])
        kd = float(inputs["kd"])
        ki = float(inputs["ki"])
        ki_valve = float(inputs["ki_valve"])
        gain = float(inputs["gain"])
        circulators = inputs["circulator"]
        circulator_mode = int(inputs["circulator_mode"])
        circulator_mode_P = 4
        print(circulator_mode)
        feedback_sensor = inputs["feedback_sensor"]
        actuators = inputs["actuator"]
        valves = inputs["valves"]
        setpoint = [float(n) for n in inputs["setpoint"]]
        feedback_value = [_BEGIN_WITH] * len(feedback_sensor)
        time_response = [_BEGIN_WITH] * len(feedback_sensor)
        derivative = [_BEGIN_WITH] * len(feedback_sensor)
        integral = [_BEGIN_WITH] * len(feedback_sensor)
        integral[_BEGIN_WITH] = _MIN_SAT_PUMP
        integral_valve = [_BEGIN_WITH] * len(feedback_sensor)
        windup_corrector = [_BEGIN_WITH] * len(feedback_sensor)
        controller_output = [_BEGIN_WITH] * len(actuators)
        controller_output_percentage = [_BEGIN_WITH] * len(actuators)
        pre_error = [_BEGIN_WITH] * len(feedback_sensor)
        actuator_signal = [_BEGIN_WITH] * len(actuators)
        actuator_signal_valve = [_BEGIN_WITH] * len(actuators)
        error_value = [_BEGIN_WITH] * len(feedback_sensor)
        self.thresholds = [_BEGIN_WITH] * len(feedback_sensor)
        CompositMess = [_BEGIN_WITH] * len(actuators)

        for n in range(0, len(feedback_sensor)):
            title = "Time Response Signal Sensor " + feedback_sensor[n]
            self.plot_array[n].set_title(title)
        if len(feedback_sensor) < len(self.plot_array):
            title = "No more sensors"
            self.plot_array[-1].set_title(title)

        shut_down_signal = 0
        shut_mess = CM(shut_down_signal, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        mode_C = PM(circulator_mode, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        mode_P = PM(circulator_mode_P, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        for pump in pumps_of_circuit:
            if pump not in circulators:
                print(circulator_mode)
                interface.setPumpControlMode(pump, mode_C)
                interface.stopPump(pump)
                time.sleep(0.2)
                print("Pump ", pump, "has been stopped")
        half_power_signal = 50
        half_power = CM(half_power_signal, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        print(circulators)
        n = 0
        for pump in circulators:
            interface.startPump(pump)
            interface.setPumpControlMode(pump, mode_C)
            interface.setPumpSetpoint(pump, half_power)
            time.sleep(0.2)
            print("Pump ", pump, "was started")
            n += 1
        start_time = time.time()
        counter_time = time.time()
        counter_time_valve = time.time()
        signal.signal(signal.SIGTERM, self.signal_term_handler)
        time.sleep(12.5)
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
                    feedback_value[n] = interface.getThermalPower(feedback_sensor[n]).value
                    if not isinstance(feedback_value[n], float):
                        feedback_value[n] = 0     # --->>> really bad though
                    print("feedback taken from sensor {0} with setpoint {1} is kW {2}".format(feedback_sensor[n], setpoint[n], feedback_value[n]))
                    print("The error is {0}".format(error_value[n]))
                    print("The integral for pump is {0} and the actuator signal for pump is {1}".format(integral[n], actuator_signal[n]))
                    print("The actuator signal for valve is ", actuator_signal_valve[n])
                    print("Setpoint {0} was sent to actuator {1}".format(actuator_signal[n], actuators[n]))
                    #print("The integral error is ", integral[n])
                    #print("The actuator signal is ", actuator_signal[n])
                    #print("Setpoint {0} was sent to actuator {1}".format(actuator_signal[n], actuators[n]))
                    self.ydata[n].append(feedback_value[n])  # Save as previous error.
                    self.xdata[n].append(time.time() - start_time)
                    #feedback_value[n] = 0
                    self.update_line()

                if stop_time - counter_time > control_time:
                    if not valve_reg:
                        print("I am actuating with pump")
                        for n in range(_BEGIN_WITH, len(feedback_sensor)):
                            error_value[n] = setpoint[n] - feedback_value[n]    # Calculate the error
                            integral[n] = integral[n] + ki * error_value[n]  # - windup_corrector[n]              # Calculate integral
                            integral[n] = self.anti_windup(integral[n], "pump")
                            print("The integral error is ", integral[n])
                            actuator_signal[n] = kp * error_value[n] + integral[n]
                            actuator_signal[n] = self.saturation(actuator_signal[n], "pump")
                            print("The actuator signal for pump is ", actuator_signal[n])

                            CompositMess[n] = CM(actuator_signal[n], time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                            interface.setPumpSetpoint(actuators[n], CompositMess[n])
                        counter_time = time.time()

                        if (abs(error_value[n]) > _TOLERANCE) and (actuator_signal[n] <= _MIN_SAT_PUMP) and not valve_reg:
                            if first_call:
                                print("30s start from here")
                                start_time = time.time()
                                first_call = False
                            if (time.time() - start_time) >= 30:
                                print("I am heeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeer")
                                integral_valve[0] = interface.getValvePosition("Bay_3L-Busbar_1R").value
                                valve_reg = True
                                control_time = 45
                                interface.setPumpControlMode(actuators[n], mode_P)
                                print("Pump {0} was set to {1}".format(actuators[n], mode_P))
                                pressure_setpoint = CM(interface.getPumpHead(actuators[n]).value, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                                interface.setPumpSetpoint(actuators[n], pressure_setpoint)

                        else:
                            counter_time = time.time()
                            first_call = True

                    if valve_reg:
                        print("I am actuating with valve")
                        for n in range(_BEGIN_WITH, len(feedback_sensor)):
                            error_value[n] = setpoint[n] - feedback_value[n]    # Calculate the error
                            integral_valve[n] = integral_valve[n] + ki_valve * error_value[n]  # - windup_corrector[n]              # Calculate integral
                            integral_valve[n] = self.anti_windup(integral_valve[n], "valve")
                            print("The valve integral error is ", integral_valve[n])
                            actuator_signal_valve[n] = integral_valve[n]
                            actuator_signal_valve[n] = self.saturation(actuator_signal_valve[n], "valve")
                            print("The actuator signal for valve is ", actuator_signal_valve[n])
                            CompositMess_Valve = CM(actuator_signal_valve[n], time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                            interface.setValvePosition("Bay_3L-Busbar_1R", CompositMess_Valve)
                        valve_position = interface.getValvePosition("Bay_3L-Busbar_1R").value
                        #counter_time = time.time()
                        if ((error_value[n] > _TOLERANCE) and (actuator_signal[n] <= _MIN_SAT_PUMP) and (valve_position >= 0.9)):
                                valve_reg = False
                                control_time = 25
                                first_call = True
                                interface.setPumpControlMode(actuators[n], mode_C)
                                curve_setpoint = CM(_MIN_SAT_PUMP, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                                interface.setPumpSetpoint(actuators[n], curve_setpoint)
                                print("Pump {0} was set to {1}".format(actuators[n], mode_C))
                                integral[_BEGIN_WITH] = _MIN_SAT_PUMP
                        else:
                            counter_time = time.time()

                time.sleep(_ACQUISITION_TIME)

            #except (KeyboardInterrupt, SystemExit):
            #    for circulator in circulators:
            #        interface.stopPump(pump)
            #        print("Circulator {0} is now at zero flow".format(circulator))
            #    sys.exit(0)
            #except Exception:
            #    '''there is the condition because it will keep except'''
            #    self.shut_down_routine(pumps_of_circuit, valves, interface)

    def anti_windup(self, integral_error, actuator):
        '''to be confirmed if we want a minimum of wind up tolerance'''
        if (actuator == "pump"):
            if integral_error > _MAX_SAT_PUMP:
                integral_error = _MAX_SAT_PUMP  # integral_error - (integral_error - _MAX_SAT)
            elif integral_error < _MIN_SAT_PUMP:
                integral_error = _MIN_SAT_PUMP  #integral_error + (_MIN_SAT - integral_error)
            else:
                pass
        elif (actuator == "valve"):
            if integral_error > _MAX_SAT_VALVE:
                integral_error = _MAX_SAT_VALVE  # integral_error - (integral_error - _MAX_SAT)
            elif integral_error < _MIN_SAT_VALVE:
                integral_error = _MIN_SAT_VALVE  #integral_error + (_MIN_SAT - integral_error)
            else:
                pass

        return integral_error

    def saturation(self, actuator_signal, actuator):
        min_pump = 41
        max_pump = 100
        min_valve = 0.3
        max_valve = 1
        if (actuator == "pump"):
            if actuator_signal <= min_pump:
                actuator_signal = _MIN_SAT_PUMP
            elif actuator_signal >= max_pump:
                actuator_signal = _MAX_SAT_PUMP
            else:
                pass
        elif (actuator == "valve"):
            if actuator_signal <= min_valve:
                actuator_signal = _MIN_SAT_VALVE
            elif actuator_signal >= max_valve:
                actuator_signal = _MAX_SAT_VALVE
            else:
                pass

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


if __name__ == "__main__":
    test = controller_constant_curve()
    input_for_controller = {'controller_name': "['Source_1BH4']['Sink_1DL3']N", 'description': 'creator',
                            'gain': '1', 'kp': '5', 'ki': '8', 'kd': '0', 'ki_valve': '0.1', 'pumps_of_circuit': ['Pump_Bay4', 'Pump_Bay3'],
                            'circulator': ['Pump_Bay4'], 'circulator_mode': '0', 'actuator': ['Pump_Bay4'], 'setpoint': [3],
                            'feedback_sensor': ['Bay_4'], 'valves': ['Bay_4L-Busbar_2R', 'Bay_4H-Busbar_1F', 'Bay_3H-Busbar_2F', 'Bay_3L-Busbar_1R']}
    '''input_for_controller = {'controller_name': "['Source_1BH4']['Sink_1H7', 'Sink_1H8']N", 'description': 'creator',
                            'gain': '1', 'kp': '2.58', 'ki': '1', 'kd': '0', 'pumps_of_circuit': ['Pump_Bay4', 'Pump_Bay7', 'Pump_Bay8'],
                            'circulator': ['Pump_Bay7', 'Pump_Bay8'], 'circulator_mode': '0', 'actuator': ['Pump_Bay7', 'Pump_Bay8'], 'setpoint': [0.5, 0.5],
                            'feedback_sensor': ['Bay_7', 'Bay_8'], 'valves': ['Bay_4L-Busbar_2R', 'Bay_4H-Busbar_1F', 'Bay_7H-Busbar_2F', 'Bay_7L-Busbar_1R']}'''
    queue = Queue()
    inputs = pickle.dumps(input_for_controller)
    test.PID_controller(inputs, input_for_controller['controller_name'], queue)
