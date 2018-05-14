# import SWITCHBOARD_PYTHON_API
# remember that additional gain can be added by multiplying the error by a constant
# you could initialize this controller as a class when you initialize the logical layer and then call the method that start the thread every time you need it
import pickle
import signal
import sys
import syslab
import syslab.core.datatypes.CompositeMeasurement as CM
import time
_BUILDING_NAME = "716-h1"
_CONTROL_TIME = 2
_MULTIPLIER = 1000000

class controller(object):

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
        error = []
        time_response = []
        kp = float(inputs["kp"])
        kd = float(inputs["kd"])
        ki = float(inputs["ki"])
        gain = float(inputs["gain"])
        circulators = inputs["circulator"]
        circulator_mode = inputs["circulator_mode"]
        feedback_sensor = inputs["feedback_sensor"]
        setpoint = float(inputs["setpoint"])
        integral = 0
        pre_error = 0
        windup_corrector = 0
        actuator_signal = 0
        interface = syslab.HeatSwitchBoard(_BUILDING_NAME)
        shut_down_signal = 0
        # interface.setPumpMode(circulators[n], circulator_mode[n])
        # for n in len(circulators):
            # print(n)

        while(1):
            try:
                print("Control Thread {0} running".format(process_ID))
                time.sleep(_CONTROL_TIME)
                feedback_value = interface.getThermalPower(feedback_sensor).value

                #print(feedback_value)
                print(interface.getThermalPower(feedback_sensor))
                feedback_value = 0
                error_value = gain * (setpoint - feedback_value)       # Calculate the error
                integral = (integral + error_value) - windup_corrector              # Calculate integral
                derivative = error_value - pre_error           # Calculate derivative

                controller_output = (kp * error_value) + (ki * integral) + (kd * derivative)  # Calculate the controller_output, pwm.

                windup_corrector = self.controller_wind_up(actuator_signal, controller_output, ki)

                controller_output_percentage = self.pump_setpoint_converter(controller_output)

                if (controller_output_percentage > max):
                    actuator_signal = 100  # Limit the controller_output to maximum 255.
                elif (controller_output_percentage < min):
                    actuator_signal = 1
                else:
                    actuator_signal = controller_output_percentage
                print(actuator_signal)
                CompositMess = CM(actuator_signal, time.time() * _MULTIPLIER)
                print(CompositMess)
                # interface.setPumpSetpoint(circulators, CompositMess)
                error.append(error_value)
                time_response.append(feedback_value)  # Save as previous error.
                signal.signal(signal.SIGTERM, self.signal_term_handler)
            except (KeyboardInterrupt, Exception, SystemExit):
                CompositMess = CM(actuator_signal, time.time() * _MULTIPLIER)
                # interface.setPumpSetpoint(circulators, CompositMess)
                print("Circulators is now at zero flow")
                sys.exit(0)

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
        pump_max_volume_flow = 10
        volume_flow_in_percent = 100 * (volume_flow / pump_max_volume_flow)
        return volume_flow_in_percent


if __name__ == "__main__":
    test = controller()
    input_for_controller = {"gain": 1, "kp": 2.58, "ki": 2.58, "kd": 0, "circulator": "Pump", "circulator_mode": "constant m", "actuator": "pump", "setpoint": 50, "feedback_sensor": 'Bay_4'}
    inputs = pickle.dumps(input_for_controller)
    test.PID_controller(inputs, "test_controller")
