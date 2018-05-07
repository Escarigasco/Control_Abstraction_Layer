import random


class random_server(object):
    def __init__(self, pumps, sensors, valves):
        min_operating = 0
        max_operating = 100
        step = max_operating * 0.5

        for valve in valves.keys():
            setpoint = random.randint(min_operating, max_operating)
            valves[valve].set_status(setpoint)


class read_current_status(object):
    def __init__(self, pumps, sensors, valves):
        # INTERFACE = SWITCHBOARD_PYTHON_API()
        for valve in valves.keys():
            setpoint = 1  # INTERFACE.GET_VALVE_POSITION(VALVE_NAME)
            valves[valve].set_status(setpoint)
