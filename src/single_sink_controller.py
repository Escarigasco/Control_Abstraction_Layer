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
_MIN_SAT_VALVE = 0.25
_MAX_SAT_VALVE = 1
_TOLERANCE = -0.1
_FEEDFORWARD_KICK = 0.7
_DENSITY = 999
_Cp = 4.186
_HOUR_CONVERTER = 3600
_LITER_CONVERTER = 1000
_RPM_MAX = 3500
_PERCENT = 100
_PUMP = "pump"
_VALVE = "valve"
_MAX_HEAD = 6
_READING_CORRECTOR = 10


class controller_constant_curve(object):

    def PID_controller(self, inputs, process_ID, queue):
        inputs = pickle.loads(inputs)
        print(inputs)
        inputs = {'controller_name': "['Source_1BH4']['Sink_1DL3']N", 'description': 'creator',
                  'gain': '1', 'kp': '4', 'ki': '7', 'kd': '0', 'ki_valve': '0.07', 'pumps_of_circuit': ['Pump_Bay4', 'Pump_Bay3'],
                  'circulator': ['Pump_Bay4'], 'circulator_mode': '0', 'actuator': ['Pump_Bay4'], 'setpoint': [4],
                  'feedback_sensor': ['Bay_3'], 'valves': ['Bay_4L-Busbar_2R', 'Bay_4H-Busbar_1F', 'Bay_3H-Busbar_2F', 'Bay_3L-Busbar_1R'],
                  'actuator_valve': "Bay_3L-Busbar_1R"}
        print("Controller Constant Flow Started")
        interface = syslab.HeatSwitchBoard(_BUILDING_NAME)
        plt.show()
        plt.ion()
        self.xdata = []
        self.ydata = []
        f, self.ax1 = plt.subplots(1, 1)
        self.ax1.set_xlim(0, 100)
        self.ax1.set_ylim(-50, +50)
        self.ax1.set_xlabel('Time [s]', fontsize=10)
        self.ax1.set_ylabel('Thermal Power [kW]', fontsize=10)
        self.line, = self.ax1.plot(self.xdata, self.ydata, 'b-')

        self.line.set_xdata(self.xdata)
        self.line.set_ydata(self.ydata)
        self.plot_array = self.ax1
        self.line_array = self.line

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
        feedback_sensor = feedback_sensor[_BEGIN_WITH]
        actuator_valve = inputs['actuator_valve']
        actuators = inputs["actuator"]
        valves = inputs["valves"]
        setpoint = [float(n) for n in inputs["setpoint"]]
        setpoint = setpoint[_BEGIN_WITH]
        feedback_value = 0
        integral = _MIN_SAT_PUMP
        integral_valve = 0
        controller_output = [_BEGIN_WITH] * len(actuators)
        controller_output_percentage = [_BEGIN_WITH] * len(actuators)
        actuator_signal = 0
        actuator_signal_valve = 0
        error_value = 0
        CompositMess = 0


        title = "Time Response Signal Sensor " + feedback_sensor
        self.plot_array.set_title(title)


        shut_down_signal = 0
        shut_mess = CM(shut_down_signal, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        mode_C = PM(circulator_mode, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        mode_P = PM(circulator_mode_P, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        for pump in pumps_of_circuit:
            if pump not in actuators:
                print(circulator_mode)
                interface.setPumpControlMode(pump, mode_C)
                interface.stopPump(pump)
                time.sleep(0.2)
                print("Pump ", pump, "has been stopped")
        full_power_signal = 100
        full_power = CM(full_power_signal, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
        print(actuators)
        n = 0
        for pump in actuators:
            interface.startPump(pump)
            interface.setPumpControlMode(pump, mode_C)
            interface.setPumpSetpoint(pump, full_power)
            time.sleep(0.2)
            print("Pump ", pump, "was started")
            n += 1

        start_time = time.time()
        counter_time = time.time()
        counter_time_valve = time.time()
        signal.signal(signal.SIGTERM, self.signal_term_handler)
        time.sleep(30)
        while(1):

            #try:
                stop_time = time.time()
                if (not self.work_q.empty()):
                    received_setpoint = self.work_q.get()
                    setpoint = [float(n) for n in inputs["setpoint"]]
                    setpoint = setpoint[_BEGIN_WITH]
                    self.n = 0

                print("Control Thread {0} running".format(process_ID))

                feedback_value = interface.getThermalPower(feedback_sensor).value
                if not isinstance(feedback_value, float):
                    feedback_value = 0     # --->>> really bad though
                print("feedback taken from sensor {0} with setpoint {1} is kW {2}".format(feedback_sensor, setpoint, feedback_value))
                print("The error is {0}".format(setpoint - feedback_value))
                print("The integral for pump is {0} and the actuator signal for pump is {1}".format(integral, actuator_signal))
                print("The actuator signal for valve is ", actuator_signal_valve)
                print("Setpoint {0} was sent to actuator {1}".format(actuator_signal, actuators))
                print("The current FLow is ", interface.getFlow(feedback_sensor).value)
                print("The current RPM is ", interface.getPumpRPM("Pump_Bay4").value)
                print("I am actuating with valve ", valve_reg)

                self.ydata.append(feedback_value)  # Save as previous error.
                self.xdata.append(time.time() - start_time)
                #feedback_value[n] = 0
                self.update_line()

                if stop_time - counter_time > control_time:
                    if not valve_reg:
                        print("I am actuating with pump")
                        error_value = setpoint - feedback_value    # Calculate the error
                        if abs(error_value) > _FEEDFORWARD_KICK:
                            integral = self.feedforward(interface, setpoint, feedback_sensor, actuators)
                            actuator_signal = integral
                            CompositMess = CM(actuator_signal, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                            for actuator in actuators:
                                interface.setPumpSetpoint(actuator, CompositMess)
                        else:
                            integral = integral + ki * error_value              # Calculate integral
                            integral = self.anti_windup(integral, _PUMP)
                            print("The integral error is ", integral)
                            actuator_signal = kp * error_value + integral
                            actuator_signal = self.saturation(actuator_signal, _PUMP)
                            print("The actuator signal for pump is ", actuator_signal)
                            CompositMess = CM(actuator_signal, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                            for actuator in actuators:
                                interface.setPumpSetpoint(actuator, CompositMess)

                        counter_time = time.time()

                        if ((error_value < _TOLERANCE) and (actuator_signal <= _MIN_SAT_PUMP) and not valve_reg):
                            print("I am cheking if is the case of using the valves")
                            if first_call:
                                print("60s start from here")
                                start_time = time.time()
                                first_call = False
                            if (time.time() - start_time) >= control_time * 2:
                                print("Time to use the valve")
                                integral_valve = interface.getValvePosition(actuator_valve).value
                                valve_reg = True
                                control_time = 50
                                pressure_setpoint = 0
                                pressure_setpoint = CM(pressure_setpoint, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                                for actuator in actuators:
                                    interface.setPumpControlMode(actuator, mode_P)
                                    print("Pump {0} was set to {1}".format(actuator, mode_P))
                                    time.sleep(0.2)
                                    interface.setPumpSetpoint(actuator, pressure_setpoint)

                        else:
                            counter_time = time.time()
                            first_call = True

                    if valve_reg:
                        print("I am actuating with valve")
                        error_value = setpoint - feedback_value    # Calculate the error
                        integral_valve = integral_valve + ki_valve * error_value  # Calculate integral
                        integral_valve = self.anti_windup(integral_valve, _VALVE)
                        print("The valve integral error is ", integral_valve)
                        actuator_signal_valve = integral_valve
                        actuator_signal_valve = self.saturation(actuator_signal_valve, _VALVE)
                        print("The actuator signal for valve is ", actuator_signal_valve)
                        CompositMess_Valve = CM(actuator_signal_valve, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                        interface.setValvePosition(actuator_valve, CompositMess_Valve)
                        valve_position = interface.getValvePosition(actuator_valve).value
                        #counter_time = time.time()
                        if ((error_value > _TOLERANCE) and (actuator_signal <= _MIN_SAT_PUMP) and (valve_position >= 0.9)):
                                valve_reg = False
                                control_time = 25
                                first_call = True
                                curve_setpoint = CM(_MIN_SAT_PUMP, time.time() * _MULTIPLIER, _ZERO, _ZERO, _VALIDITY, _SOURCE)
                                for actuator in actuators:
                                    interface.setPumpControlMode(actuator, mode_C)
                                    time.sleep(0.2)
                                    interface.setPumpSetpoint(actuator, curve_setpoint)
                                    print("Pump {0} was set to {1}".format(actuator, mode_C))
                                    integral = _MIN_SAT_PUMP
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

    def feedforward(self, interface, setpoint, feedback_sensor, actuators):

        T_f = interface.getFwdTemperature(feedback_sensor).value
        T_r = interface.getBackTemperature(feedback_sensor).value
        Q_current = interface.getFlow(feedback_sensor).value
        DT = T_f - T_r
        print(T_f)
        print(T_r)
        print(DT)
        RPM_current = interface.getPumpRPM(actuators[_BEGIN_WITH]).value
        Q_needed = setpoint / (_Cp * _DENSITY * DT)
        Q_needed = Q_needed * _HOUR_CONVERTER * _LITER_CONVERTER
        RPM_needed = RPM_current * Q_needed / Q_current
        print("The RPM currently are ", RPM_current)
        print("The RPM needed are ", RPM_needed)
        RPM_percentage = (RPM_needed * _PERCENT) / _RPM_MAX
        if RPM_percentage < _MIN_SAT_PUMP:
            RPM_percentage = _MIN_SAT_PUMP
        elif RPM_percentage > _MAX_SAT_PUMP:
            RPM_percentage = _MAX_SAT_PUMP

        print("The RPM percentage is ", RPM_percentage)
        return RPM_percentage


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

        if (self.xdata):
                self.plot_array.set_xlim(max(self.xdata) - limits, max(self.xdata) + limits)
                self.plot_array.set_ylim(max(self.ydata) - limits, max(self.ydata) + limits)
                self.line_array.set_xdata(self.xdata)
                self.line_array.set_ydata(self.ydata)
                if len(self.xdata) > max_dimension:
                    del self.xdata[:removable]
                    del self.ydata[:removable]
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
