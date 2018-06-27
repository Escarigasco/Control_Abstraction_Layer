# import SWITCHBOARD_PYTHON_API
# remember that additional gain can be added by multiplying the error by a constant
# you could initialize this controller as a class when you initialize the logical layer and then call the method that start the thread every time you need it
'''THE CONTROL TIME WILL EVENTUALLY GO IN THE CONFIGURATION FILE AS IT WILL BE DIFFERENT FROM CONTANT PRESSURE TO CONSTANT FLOW OR WHATEVER'''
import pickle
import signal
import sys
import syslab
import syslab.core.datatypes.CompositeMeasurement as CM
import time
_BUILDING_NAME = "716-h1"
_CONTROL_TIME = 1
_MULTIPLIER = 1000000
_OFF = "OFF"
_FIRST_OF_CLASS = 0
_MINUTES_THRESHOLDS = 100


class controller_constant_flow(object):

    def PID_controller(self, inputs, process_ID, queue):
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
        circulator_mode = inputs["circulator_mode"]
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
        interface = syslab.HeatSwitchBoard(_BUILDING_NAME)
        shut_down_signal = 0
        shut_mess = CM(shut_down_signal, time.time() * _MULTIPLIER)
        for n in range(_FIRST_OF_CLASS, len(pumps_of_circuit)):
            #interface.setPumpControlMode(pumps_of_circuit[n], circulator_mode)
            #interface.setPumpSetpoint(pumps_of_circuit[n], shut_mess)
            print("mode set in pump ", pumps_of_circuit[n], "with setpoint to 0")

        signal.signal(signal.SIGTERM, self.signal_term_handler)
        while(1):

            try:
                time.sleep(_CONTROL_TIME)
                if (not self.work_q.empty()):
                    received_setpoint = self.work_q.get()
                    setpoint = [float(n) for n in received_setpoint]
                    self.n = 0
                    start_time = time.time()
                    self.threshold = [_FIRST_OF_CLASS] * len(feedback_sensor)

                if stopper:
                    print("Control Thread {0} is ready to be stopped".format(process_ID))
                    #signal.signal(signal.SIGTERM, self.signal_term_handler)
                    print(active_circuit)
                    if active_circuit:
                        self.shut_down_routine(circulators, valves)
                        active_circuit = False
                else:
                    print("Control Thread {0} running".format(process_ID))
                    for n in range(_FIRST_OF_CLASS, len(feedback_sensor)):
                        print(n)
                        feedback_value[n] = interface.getThermalPower(feedback_sensor[n]).value
                        print(interface.getThermalPower(feedback_sensor[n]))
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
                        CompositMess[n] = CM(actuator_signal[n], time.time() * _MULTIPLIER)
                        pre_error[n] = error_value[n]
                    for n in range(_FIRST_OF_CLASS, len(actuators)):
                        #interface.setPumpSetpoint(actuators[n], CompositMess[n])
                        print("Setpoint {0} was sent to actuator {1}".format(actuator_signal[n], actuators[n]))
                        error_development[n].append(error_value[n])
                        time_response[n].append(feedback_value[n])  # Save as previous error.
                    #signal.signal(signal.SIGTERM, self.signal_term_handler)
                    stopper = self.minutes_threshold([x / gain for x in error_value], start_time)

            except (KeyboardInterrupt, SystemExit):
                #interface.setPumpMode(actuators[_FIRST_OF_CLASS], _OFF) I don't think exist
                for circulator in circulators:
                    #interface.setPumpSetpoint(circulator, shut_mess)
                    print("Circulator {0} is now at zero flow".format(circulator))
                sys.exit(0)
            except Exception:
                '''there is the condition because it will keep except'''
                if active_circuit:
                    stopper = True
                    self.shut_down_routine(circulators, valves)
                    active_circuit = False

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

    def minutes_threshold(self, errors, start_time):
        stop_time = time.time()
        current_time = stop_time - start_time

        idx = 0
        if current_time >= (60 * self.n):
            self.n += 1
            for error in errors:
                self.thresholds[idx] += error
                idx += 1
            for threshold in self.thresholds:
                if threshold > _MINUTES_THRESHOLDS:
                    return True
        print("the minutes degree quantities are ", self.thresholds)
        return False

    def shut_down_routine(self, circulators, valves):
        shut_down_signal = 0
        CompositMess = CM(shut_down_signal, time.time() * _MULTIPLIER)
        for circulator in circulators:
            print("Circulators are off")
            #interface.setPumpSetpoint(circulator, CompositMess)
        for valve in valves:
            print("Valves are closed")
            #interface.setPumpSetpoint(valve, CompositMess)

if __name__ == "__main__":
    test = controller_constant_flow()
    input_for_controller = {"gain": 1, "kp": 2.58, "ki": 2.58, "kd": 0, "circulator": ['Pump_Bay8', 'Pump_Bay7'], "circulator_mode":
                            'PUMP_MODE_CONSTANT_FLOW', "actuator": ['Pump_Bay8', 'Pump_Bay7'], "setpoint": [1, 2],
                            "feedback_sensor": ['Bay_8', 'Bay_7']}
    inputs = pickle.dumps(input_for_controller)
    test.PID_controller(inputs, "test_controller")
