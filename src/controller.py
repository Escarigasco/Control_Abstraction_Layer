# import SWITCHBOARD_PYTHON_API
# remember that additional gain can be added by multiplying the error by a constant
# you could initialize this controller as a class when you initialize the logical layer and then call the method that start the thread every time you need it
import _thread
import pickle
import sys
import time


class controller(object):

    def read_feedback():
        value = 0
        return value

    def PID_controller(self, inputs, thread_ID):
        print("Control Thread {0} started".format(thread_ID))
        print(thread_ID)
        inputs = pickle.loads(inputs)
        print(inputs)
        error = []
        time_response = []
        kp = inputs["kp"]
        kd = inputs["ki"]
        ki = inputs["kd"]
        gain = inputs["gain"]
        circulators = inputs["circulator"]
        circulator_mode = inputs["circulator_mode"]
        integral = 0
        pre_error = 0
        # INTERFACE = SWITCHBOARD_PYTHON_API()
        #for n in len(circulators):
            #print(n)
            # INTERFACE.SET_CIRCULATOR_MODE(circulators[n], circulator_mode[n])
        while(1):
            try:
                print("Control Thread {0} running".format(thread_ID))
                time.sleep((thread_ID + 2))
                feedback_value = 5  # INTERFACE.read_feedback("SENSOR")                    # Get the feedback value
                setpoint = inputs["setpoint"]                         # Get the set value

                error_value = gain * (setpoint - feedback_value)       # Calculate the error
                integral = integral + error_value              # Calculate integral
                derivative = error_value - pre_error           # Calculate derivative

                output = (kp * error_value) + (ki * integral) + (kd * derivative)  # Calculate the output, pwm.

                if (output > 100):
                    output = 100  # Limit the output to maximum 255.
                elif (output < 1):
                    output = 1

                error.append(error_value)
                time_response.append(feedback_value)  # Save as previous error.
            except (KeyboardInterrupt, SystemExit, Exception):
                print("Thread Stopped")
                _thread.exit()
                sys.exit()


if __name__ == "__main__":
    test = controller()
    input_for_controller = {"gain": 1, "kp": 2.58, "ki": 2.58, "kd": 0, "circulator": "Pump", "circulator_mode": "constant m", "actuator": "pump", "setpoint": 50, "feedback": 'sensors'}
    test.PID_controller(input_for_controller)
