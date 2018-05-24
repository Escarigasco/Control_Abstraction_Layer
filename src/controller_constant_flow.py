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
_CONTROL_TIME = 2
_MULTIPLIER = 1000000
_OFF = "OFF"
_FIRST_OF_CLASS = 0


class controller_constant_flow(object):

    def read_feedback():
        value = 0
        return value

    def PID_controller(self, inputs, process_ID):

        print("Control Process {0} started".format(process_ID))
        print("I am process", process_ID)
        inputs = pickle.loads(inputs)
        print(inputs)
        self.process_ID = process_ID
        max = 100
        min = 0
        kp = float(inputs["kp"])
        kd = float(inputs["kd"])
        ki = float(inputs["ki"])
        gain = float(inputs["gain"])
        circulators = inputs["circulator"]
        circulator_mode = inputs["circulator_mode"]
        feedback_sensor = inputs["feedback_sensor"]
        actuators = inputs["actuator"]
        setpoint = [float(n) for n in inputs["setpoint"]]
        print(inputs)
        feedback_value = [_FIRST_OF_CLASS] * len(feedback_sensor)
        time_response = [_FIRST_OF_CLASS] * len(feedback_sensor)
        derivative = [_FIRST_OF_CLASS] * len(actuators)
        integral = [_FIRST_OF_CLASS] * len(actuators)
        windup_corrector = [_FIRST_OF_CLASS] * len(actuators)
        controller_output = [_FIRST_OF_CLASS] * len(actuators)
        controller_output_percentage = [_FIRST_OF_CLASS] * len(actuators)
        pre_error = [_FIRST_OF_CLASS] * len(feedback_sensor)
        actuator_signal = [_FIRST_OF_CLASS] * len(actuators)
        error_value = [_FIRST_OF_CLASS] * len(feedback_sensor)
        CompositMess = [_FIRST_OF_CLASS] * len(actuators)
        error_development = [[] for n in range(len(feedback_sensor))]
        time_response = [[] for n in range(len(feedback_sensor))]
        #interface = syslab.HeatSwitchBoard(_BUILDING_NAME)
        shut_down_signal = 0
        for n in range(_FIRST_OF_CLASS, len(circulators)):
            #interface.setPumpMode(circulators[n], circulator_mode)
            print("mode set in pump ", circulators[n])

        while(1):
            #try:
                print("Control Thread {0} running".format(process_ID))
                time.sleep(_CONTROL_TIME)
                for n in range(_FIRST_OF_CLASS, len(feedback_sensor)):
                    print(n)
                    #feedback_value[n] = interface.getThermalPower(feedback_sensor[n]).value
                    #feedback_value = interface.getThermalPower(feedback_sensor[_FIRST_OF_CLASS]).value
                    print("feedback taken from sensor ", feedback_sensor[n])
                    feedback_value[n] = 0
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
                    print(CompositMess[n])
                    pre_error[n] = error_value[n]
                for n in range(_FIRST_OF_CLASS, len(actuators)):
                    #interface.setPumpSetpoint(actuators[n], CompositMess[n])
                    print("Setpoint {0} was sent to actuator {1}".format(actuator_signal[n], actuators[n]))
                    error_development[n].append(error_value[n])
                    time_response[n].append(feedback_value[n])  # Save as previous error.
                signal.signal(signal.SIGTERM, self.signal_term_handler)
            #except (KeyboardInterrupt, Exception, SystemExit):
            #    #interface.setPumpMode(actuators[_FIRST_OF_CLASS], _OFF) I don't think exist
            #    CompositMess = CM(shut_down_signal, time.time() * _MULTIPLIER)
            #    #interface.setPumpSetpoint(actuators[_FIRST_OF_CLASS], CompositMess)
            #    print("Circulators is now at zero flow")
            #    sys.exit(0)

    def controller_wind_up(self, actuator_signal, controller_output, ki):
        error_saturation = actuator_signal - controller_output
        windup_corrector = error_saturation / ki
        return windup_corrector

    def signal_term_handler(signal, frame):
        print("It has to be here to receive signal but doesn't effectively do anything this is not going to be printed but it handles the asynchronous interaction")
        #print('got SIGTERM - the process was killed as the configuration was not matched any more')
        #print("Circulators is now at zero flow")
        # interface.setPumpSetpoint(circulators, actuator_signal)
        #sys.exit(0)

    def pump_setpoint_converter(self, volume_flow):
        pump_max_volume_flow = 10 # this is correct
        volume_flow_in_percent = 100 * (volume_flow / pump_max_volume_flow)
        return volume_flow_in_percent


if __name__ == "__main__":
    test = controller_constant_flow()
    input_for_controller = {"gain": 1, "kp": 2.58, "ki": 2.58, "kd": 0, "circulator": ['Pump_Bay8', 'Pump_Bay7'], "circulator_mode":
                            'PUMP_MODE_CONSTANT_FLOW', "actuator": ['Pump_Bay8', 'Pump_Bay7'], "setpoint": [1, 2],
                            "feedback_sensor": ['Bay_8', 'Bay_7']}
    inputs = pickle.dumps(input_for_controller)
    test.PID_controller(inputs, "test_controller")
