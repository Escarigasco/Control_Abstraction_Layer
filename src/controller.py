import _thread
# import SWITCHBOARD_PYTHON_API
# remember that additional gain can be added by multiplying the error by a constant
# you could initialize this controller as a class when you initialize the logical layer and then call the method that start the thread every time you need it


class controller(object):

    def read_feedback():

        return value

    def PID_controller(inputs):
        error = []
        time_response = []
        kp = inputs["Kp"]
        kd = inputs["Ki"]
        ki = inputs["Kd"]
        gain = inputs["Gain"]
        circulators = inputs["circulator"]
        circulator_mode = inputs["Circulator_mode"]
        # INTERFACE = SWITCHBOARD_PYTHON_API()
        for n in len(circulators):
            print(n)
            # INTERFACE.SET_CIRCULATOR_MODE(circulators[n], circulator_mode[n])
        while(1):
            feedback_value =  # INTERFACE.read_feedback("SENSOR")                    # Get the feedback value
            setpoint = inputs["Setpoint"]                         # Get the set value

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
