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
'''actuator time constant'''
_INTEGRAL_TIME = 40
'''this is sensor time constant'''
_PROPORTIONAL_TIME = 40
_ACQUISITION_TIME = 1
_MULTIPLIER = 0.000001
_OFF = "OFF"
_FIRST_OF_CLASS = 0
_MINUTES_THRESHOLDS = 100
_SOURCE = 1
_VALIDITY = 1
_ZERO = 0
_MIN_SAT = 0.20
_MAX_SAT = 1
_MIN_WIN = -0.20
_MAX_WIN = 0.20


class controller_constant_pressure(object):

    def PID_controller(self, inputs, process_ID, queue):
        print("Controller Constant Pressure Started")
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
        start_time = time.time()
        self.n = 0
        self.work_q = queue
        stopper = False
        active_circuit = True
        print("Control Process {0} started".format(process_ID))
        print("I am process", process_ID)
        inputs = pickle.loads(inputs)
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
        valves = inputs["valves"]
        setpoint = [float(n) for n in inputs["setpoint"]]
        feedback_value = [float(_FIRST_OF_CLASS)] * len(feedback_sensor)
        time_response = [_FIRST_OF_CLASS] * len(feedback_sensor)
        derivative = [_FIRST_OF_CLASS] * len(feedback_sensor)
        integral = [float(_FIRST_OF_CLASS)] * len(feedback_sensor)
        windup_corrector = [_FIRST_OF_CLASS] * len(feedback_sensor)
        controller_output = [float(_FIRST_OF_CLASS)] * len(actuators)
        controller_output_percentage = [_FIRST_OF_CLASS] * len(actuators)
        pre_error = [_FIRST_OF_CLASS] * len(feedback_sensor)
        actuator_signal = [float(_FIRST_OF_CLASS)] * len(actuators)
        error_value = [float(_FIRST_OF_CLASS)] * len(feedback_sensor)
        self.thresholds = [_FIRST_OF_CLASS] * len(feedback_sensor)
        CompositMess = [_FIRST_OF_CLASS] * len(actuators)

        n = 0
        for actuator in actuators:
            controller_output[n] = interface.getValvePosition(actuator).value
            n += 1
        for n in range(0, len(feedback_sensor)):
            title = "Time Response Signal Sensor " + feedback_sensor[n]
            self.plot_array[n].set_title(title)
        if len(feedback_sensor) < len(self.plot_array):
            title = "No more sensors"
            self.plot_array[-1].set_title(title)

        shut_down_signal = 0
        shut_mess = CM(shut_down_signal, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        mode = PM(circulator_mode, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        for pump in pumps_of_circuit:
            if pump not in circulators:
                print(circulator_mode)
                interface.stopPump(pump)
                time.sleep(0.2)
                print("Pump ", pump, "has been stopped")
        full_power_signal = 100
        flow_limit_signal = 9
        full_power = CM(full_power_signal, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        flow_limit = CM(flow_limit_signal, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        for pump in circulators:
            interface.startPump(pump)
            interface.setPumpControlMode(pump, mode)
            interface.setPumpSetpoint(pump, full_power)
            interface.setMaxFlowLimit(pump, flow_limit)
            time.sleep(0.2)
            print("Pump ", pumps_of_circuit[n], "was started")

        start_time = time.time()
        integral_start = time.time()
        proportional_start = time.time()
        signal.signal(signal.SIGTERM, self.signal_term_handler)
        while(1):

            #try:
                stop_time = time.time()
                if (not self.work_q.empty()):
                    received_setpoint = self.work_q.get()
                    setpoint = [float(n) for n in received_setpoint]
                    self.n = 0
                    self.threshold = [_FIRST_OF_CLASS] * len(feedback_sensor)

                print("Control Thread {0} running".format(process_ID))
                for n in range(_FIRST_OF_CLASS, len(feedback_sensor)):
                    print(n)
                    #feedback_value[n] = 1
                    feedback_value[n] = float(interface.getThermalPower(feedback_sensor[n]).value)
                    #print(float(interface.getThermalPower(feedback_sensor[n]).value))
                    if not isinstance(feedback_value[n], float):
                        feedback_value[n] = 0     # --->>> really bad though
                        print("It was nan")
                    print("feedback taken from sensor {0} with setpoint {1} is kW {2}".format(feedback_sensor[n], setpoint[n], feedback_value[n]))
                    print("The actuator signal is {0}".format(actuator_signal[n]))
                    print("Setpoint {0} was sent to actuator {1}".format(actuator_signal[n], actuators[n]))
                    self.ydata[n].append(feedback_value[n])  # Save as previous error.
                    self.xdata[n].append(time.time() - start_time)
                    #feedback_value[n] = 0
                    print(feedback_value[n])
                    self.update_line()

                if stop_time - proportional_start > _PROPORTIONAL_TIME:
                    for n in range(_FIRST_OF_CLASS, len(feedback_sensor)):
                        error_value[n] = setpoint[n] - feedback_value[n]    # Calculate the error
                        #print("The integral error is ", integral[n])
                        #controller_output[n] = kp * error_value[n] + ki * integral[n]
                        '''this below is the real PID action as the controller action is really related to the errorr'''
                        print("this is the error ", error_value[n])
                        integral[n] = integral[n] + ki * error_value[n]  # - windup_corrector[n]              # Calculate integral
                        integral[n] = self.anti_windup(integral[n])
                        controller_output[n] = self.saturation(controller_output[n] + kp * error_value[n] + integral[n])
                        print("The proportional action is ", kp * error_value[n])
                        print("The integral action is ", integral[n])
                        print("this is the controller output ", controller_output[n])
                        actuator_signal[n] = controller_output[n]
                        print("The actuator signal is ", actuator_signal[n])
                        CompositMess[n] = CM(actuator_signal[n], time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                        interface.setValvePosition(actuators[n], CompositMess[n])
                    proportional_start = time.time()

                #if stop_time - integral_start > _INTEGRAL_TIME:
                #    for n in range(_FIRST_OF_CLASS, len(feedback_sensor)):
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
        if integral_error > _MAX_WIN:
            integral_error = integral_error - (integral_error - _MAX_SAT)
        elif integral_error < _MIN_WIN:
            integral_error = integral_error + (_MIN_SAT - integral_error)
        else:
            pass
        return integral_error

    def saturation(self, actuator_signal):
        min = 0.2
        max = 1
        if actuator_signal <= min:
            actuator_signal = _MIN_SAT
        elif actuator_signal >= max:
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
