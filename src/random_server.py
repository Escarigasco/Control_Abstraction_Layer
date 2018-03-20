import random


class random_server(object):
    def __init__(self, pumps, sensors, valves,):
        min_operating = 0
        max_operating = 100
        step = max_operating * 0.5

        for valve in valves.keys():
            setpoint = random.randint(min_operating, max_operating)
            valves[valve].set_status(setpoint)
            print(setpoint)

        for pump in pumps.keys():
            setpoint = random.randrange(min_operating, max_operating, step)
            pumps[pump].set_status(setpoint)

        for sensor in sensors.keys():
            setpoint = random.randrange(min_operating, max_operating, step)
            sensors[sensor].set_status(setpoint)
