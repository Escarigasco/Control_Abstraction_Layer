# import SWITCHBOARD_PYTHON_API
# remember that additional gain can be added by multiplying the error by a constant
# you could initialize this controller as a class when you initialize the logical layer and then call the method that start the thread every time you need it
import pickle
import sys
import syslab
import time
_BUILDING_NAME = "716-h1"
_CONTROL_TIME = 1


class controller(object):

    def read_feedback():
        value = 0
        return value

    def PID_controller(self, inputs, thread_ID):
        print("Control Process {0} started".format(thread_ID))
        print("I am process", thread_ID)
        inputs = pickle.loads(inputs)
        print(inputs)
        self.thread_ID = thread_ID
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
        feedback = inputs["feedback"]
        setpoint = float(inputs["setpoint"])
        integral = 0
        pre_error = 0
        windup_corrector = 0
        actuator_signal = 0
        # interface = syslab.HeatSwitchBoard(_BUILDING_NAME)
        # interface.setPumpMode(circulators[n], circulator_mode[n])
        # for n in len(circulators):
            # print(n)

        while(1):
            try:
                print("Control Thread {0} running".format(thread_ID))
                time.sleep(_CONTROL_TIME)
                feedback_value = 5  # interface.getThermalPower(feedback)                    # Get the feedback value
                                        # Get the set value

                error_value = gain * (setpoint - feedback_value)       # Calculate the error
                integral = (integral + error_value) - windup_corrector              # Calculate integral
                derivative = error_value - pre_error           # Calculate derivative

                controller_output = (kp * error_value) + (ki * integral) + (kd * derivative)  # Calculate the controller_output, pwm.

                windup_corrector = self.controller_wind_up(actuator_signal, controller_output, ki)

                if (controller_output > max):
                    actuator_signal = 100  # Limit the controller_output to maximum 255.
                elif (controller_output < min):
                    actuator_signal = 1
                else:
                    actuator_signal = controller_output

                # interface.setPumpSetpoint(circulators, actuator_signal)
                error.append(error_value)
                time_response.append(feedback_value)  # Save as previous error.

            except (KeyboardInterrupt, SystemExit, Exception):

                # interface.interface.setPumpSetpoint(circulators, shut_down_signal)
                print("Circulators is now at zero flow")
                print("Process Error. Stopped")
                sys.exit()

    def controller_wind_up(self, actuator_signal, controller_output, ki):
        error_saturation = actuator_signal - controller_output
        windup_corrector = error_saturation / ki
        return windup_corrector


if __name__ == "__main__":
    test = controller()
    input_for_controller = {"gain": 1, "kp": 2.58, "ki": 2.58, "kd": 0, "circulator": "Pump", "circulator_mode": "constant m", "actuator": "pump", "setpoint": 50, "feedback": 'sensors'}
    inputs = pickle.dumps(input_for_controller)
    test.PID_controller(inputs, "test_controller")
