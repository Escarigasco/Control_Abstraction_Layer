# import SWITCHBOARD_PYTHON_API
# remember that additional gain can be added by multiplying the error by a constant
# you could initialize this controller as a class when you initialize the logical layer and then call the method that start the thread every time you need it
'''THE CONTROL TIME WILL EVENTUALLY GO IN THE CONFIGURATION FILE AS IT WILL BE DIFFERENT FROM CONTANT PRESSURE TO CONSTANT FLOW OR WHATEVER'''
import matplotlib.pyplot as plt
import numpy
import pickle
import signal
import sys
import syslab
import syslab.core.datatypes.CompositeMeasurement as CM
import syslab.core.datatypes.HeatCirculationPumpMode as PM
import time
_BUILDING_NAME = "716-h1"
_CONTROL_TIME = 1
_MULTIPLIER = 0.000001
_OFF = "OFF"
_FIRST_OF_CLASS = 0
_MINUTES_THRESHOLDS = 100
_SOURCE = 1
_VALIDITY = 1
_ZERO = 0


class controller_constant_flow(object):

    def PID_controller(self, inputs, process_ID, queue):
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
        feedback_value = [_FIRST_OF_CLASS] * len(feedback_sensor)
        time_response = [_FIRST_OF_CLASS] * len(feedback_sensor)
        derivative = [_FIRST_OF_CLASS] * len(feedback_sensor)
        integral = [_FIRST_OF_CLASS] * len(feedback_sensor)
        windup_corrector = [_FIRST_OF_CLASS] * len(feedback_sensor)
        controller_output = [_FIRST_OF_CLASS] * len(actuators)
        controller_output_percentage = [_FIRST_OF_CLASS] * len(actuators)
        pre_error = [_FIRST_OF_CLASS] * len(feedback_sensor)
        actuator_signal = [_FIRST_OF_CLASS] * len(actuators)
        error_value = [_FIRST_OF_CLASS] * len(feedback_sensor)
        self.thresholds = [_FIRST_OF_CLASS] * len(feedback_sensor)
        CompositMess = [_FIRST_OF_CLASS] * len(actuators)
        error_development = [[] for n in range(len(feedback_sensor))]
        time_response = [[] for n in range(len(feedback_sensor))]

        for n in range(0, len(feedback_sensor)):
            title = "Time Response Signal Sensor " + feedback_sensor[n]
            self.plot_array[n].set_title(title)
        if len(feedback_sensor) < len(self.plot_array):
            title = "No more sensors"
            self.plot_array[-1].set_title(title)

        #interface = syslab.HeatSwitchBoard(_BUILDING_NAME)
        shut_down_signal = 0
        shut_mess = CM(shut_down_signal, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        for n in range(_FIRST_OF_CLASS, len(pumps_of_circuit)):
            print(circulator_mode)
            mode = PM(circulator_mode, time.time() * _MULTIPLIER)
            #interface.setPumpControlMode(pumps_of_circuit[n], mode)
            #interface.setPumpSetpoint(pumps_of_circuit[n], shut_mess)
            print("mode set in pump ", pumps_of_circuit[n], "with setpoint to 0")

        start_time = time.time()
        signal.signal(signal.SIGTERM, self.signal_term_handler)
        while(1):

            #try:
            time.sleep(_CONTROL_TIME)
            if (not self.work_q.empty()):
                received_setpoint = self.work_q.get()
                setpoint = [float(n) for n in received_setpoint]
                self.n = 0
                self.threshold = [_FIRST_OF_CLASS] * len(feedback_sensor)

            print("Control Thread {0} running".format(process_ID))
            for n in range(_FIRST_OF_CLASS, len(feedback_sensor)):
                print(n)
                #feedback_value[n] = interface.getThermalPower(feedback_sensor[n]).value
                #print(interface.getThermalPower(feedback_sensor[n]))
                feedback_value[n] = 1
                if feedback_value[n] == "NaN":
                    feedback_value[n] = 0     # --->>> really bad though
                print("feedback taken from sensor {0} with setpoint {1} ".format(feedback_sensor[n], setpoint[n]))
                #feedback_value[n] = 0
                print(feedback_value[n])
                error_value[n] = gain * (setpoint[n] - feedback_value[n])       # Calculate the error

                integral[n] = (integral[n] + error_value[n]) - windup_corrector[n]              # Calculate integral
                derivative[n] = error_value[n] - pre_error[n]           # Calculate derivative
                controller_output[n] = (kp * error_value[n]) + (ki * integral[n]) + (kd * derivative[n])  # Calculate the controller_output, pwm.
                windup_corrector[n] = self.controller_wind_up(actuator_signal[n], controller_output[n], ki)
                controller_output_percentage[n] = self.pump_setpoint_converter(controller_output[n])
                if (controller_output_percentage[n] > max):
                    actuator_signal[n] = 100  # Limit the controller_output to maximum 100.
                elif (controller_output_percentage[n] < min):
                    actuator_signal[n] = 1
                else:
                    actuator_signal[n] = controller_output_percentage[n]
                print("The actuator signal is ", actuator_signal[n])
                CompositMess[n] = CM(actuator_signal[n], time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                pre_error[n] = error_value[n]
            for n in range(_FIRST_OF_CLASS, len(actuators)):
                #interface.setPumpSetpoint(actuators[n], CompositMess[n])
                print("Setpoint {0} was sent to actuator {1}".format(actuator_signal[n], actuators[n]))
                self.ydata[n].append(feedback_value[n])  # Save as previous error.
                self.xdata[n].append(time.time() - start_time)
                error_development[n] = error_value[n]
                time_response[n] = feedback_value[n]  # Save as previous error.
            self.update_line(time_response, error_development, start_time)

            #except (KeyboardInterrupt, SystemExit):
                #interface.setPumpMode(actuators[_FIRST_OF_CLASS], _OFF) I don't think exist
            #    for circulator in circulators:
                    #interface.setPumpSetpoint(circulator, shut_mess)
            #        print("Circulator {0} is now at zero flow".format(circulator))
            #    sys.exit(0)
            #except Exception:
            #    '''there is the condition because it will keep except'''
            #    self.shut_down_routine(circulators, valves)

    def controller_wind_up(self, actuator_signal, controller_output, ki):
        error_saturation = actuator_signal - controller_output
        windup_corrector = error_saturation / ki
        return windup_corrector

    def signal_term_handler(self, signal, frame):
        print('got SIGTERM - the process was killed as the configuration was not matched any more')
        sys.exit(0)

    def pump_setpoint_converter(self, volume_flow):
        pump_max_volume_flow = 10 # this is correct
        volume_flow_in_percent = 100 * (volume_flow / pump_max_volume_flow)
        return volume_flow_in_percent

    def shut_down_routine(self, circulators, valves):
        shut_down_signal = 0
        CompositMess = CM(shut_down_signal, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        for circulator in circulators:
            print("Circulators are off")
            #interface.setPumpSetpoint(circulator, CompositMess)
        for valve in valves:
            print("Valves are closed")
            #interface.setPumpSetpoint(valve, CompositMess)

    def update_line(self, time_response, error_development, start_time):
        max_dimension = 50
        removable = 20
        limits = 20
        stop_time = time.time()
        stop_watch = stop_time - start_time
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
    test = controller_constant_flow()
    input_for_controller = {"gain": 1, "kp": 2.58, "ki": 2.58, "kd": 0, "circulator": ['Pump_Bay8', 'Pump_Bay7'], "circulator_mode":
                            'PUMP_MODE_CONSTANT_FLOW', "actuator": ['Pump_Bay8', 'Pump_Bay7'], "setpoint": [1, 2],
                            "feedback_sensor": ['Bay_8', 'Bay_7']}
    inputs = pickle.dumps(input_for_controller)
    test.PID_controller(inputs, "test_controller")
