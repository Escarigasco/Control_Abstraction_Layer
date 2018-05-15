# rule engine to decide the pump to be used for governing the system
# it can potentially been used to select the best sensor for the parameter to be monitored
# even though pyKnow is meant to be action based, here is reformulate to be constriction based utilizing the enumerator to define the domain (space of solutions)
# -> utilizing the bitwise operation typical of the enumerator OR = | - AND = & - XOR = ^
from flags import Flags
from pyknow import *
_FIRST_OF_CLASS = 1


class Location(Flags):

    SOURCE = ['source']
    SINK = ['sink']
    BOOSTER = ['booster']


class Variable(Flags):

    TEMPERATURE = ["T"]
    ENERGY = ["Energy"]
    DPRESSURE = ["DP"]
    FLOW = ["F"]


class Pump_Mode(Flags):
    """this will also be the controller name"""
    OFF = ["OFF"]
    CONSTANT_SPEED = ["CONSTANT_SPEED"]
    CONSTANT_FREQUENCY = ["CONSTANT_FREQUENCY"]
    CONSTANT_HEAD = ["CONSTANT_HEAD"]
    CONSTANT_PRESSURE = ["CONSTANT_PRESSURE"]
    CONSTANT_FLOW = ["CONSTANT_FLOW"]
    CONSTANT_TEMP = ["CONSTANT_TEMP"]


class Actuator(Flags):
    VALVE = ["Valve"]
    PUMP = ["Pump"]


class Actuator_Location(Flags):
    SOURCE = ['source']
    SINK = ['sink']
    BOOSTER = ['booster']


class Sensor_Location(Flags):
    PUMP = ['Pump']
    ENERGY_METER = ['Meter']


class Sensors(Fact):
    """Info about the Sensor"""
    pass


class Pumps(Fact):
    """Info about the Pump"""
    pass


class Pump_Configurator(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.idx = 0

    @Rule(Pumps(sinks=P(lambda sink: sink >= 2), loc=Location.__all_flags__, obj='pump' << W()), salience=3)
    def use_sink_pump(self, pump):
        self.idx += 1
        pump.location = Location.__all_flags__ & Location.SINK
        pump.n_sources = 0
        self.modify(self.facts[self.idx], sources=pump.n_sources, loc=pump.location)
        print("we use the pump in the sinks")

    @Rule(Pumps(sources=P(lambda source: source > 0), loc=Location.__all_flags__, obj='pump' << W()), salience=2)
    def use_source_pump(self, pump):
        self.idx += 1
        pump.location = Location.__all_flags__ ^ Location.SINK
        Location.ALL_SOURCES = pump.location
        pump.n_sinks = 0
        self.modify(self.facts[self.idx], sinks=pump.n_sinks, loc=pump.location)
        print("we use the pump in the source")

    @Rule(Pumps(loc=Location.__all_flags__ ^ Location.SINK, boost='Y', obj='pump' << W()), salience=1)
    def use_booster_pump(self, pump):
        self.idx += 1
        pump.location = Location.ALL_SOURCES & Location.BOOSTER
        pump.n_sources = 0
        self.modify(self.facts[self.idx], sources=pump.n_sources, loc=pump.location)
        print("we use the pump in the booster")


class Pump(object):
    def __init__(self):
        self.location = []


class Sensor(object):
    def __init__(self):
        self.location = []
        self.variable = ""


class Actuator(object):
    def __init__(self):
        self.location = []


class rule_engine(object):

    def run(self, system_input):
        n_sources = len(system_input['sources'])
        n_sinks = len(system_input['sinks'])
        booster = system_input['boosted']
        feedback_variable = system_input['parameters']
        engine = Pump_Configurator()
        engine.reset()
        pump = Pump()
        sensor = Sensor()
        sensor.location = Location.__all_flags__
        sensor.variable = feedback_variable
        pump.location = Location.__all_flags__
        pump.n_sources = n_sources
        pump.n_sinks = n_sinks
        engine.declare(Pumps(sources=n_sources, sinks=n_sinks, boost=booster, loc=pump.location, obj=pump))
        #engine.declare(Sensors(loc=sensor.location, obj=sensor))
        engine.run()
        #print(sensor.location)
        return pump


if __name__ == "__main__":
        test = rule_engine()
        system_input = {"sinks": ["Sink_1H8"], "parameters": "Energy",
                        "setpoints": 30, "sources": ["Source_1DH6"],
                        "boosted": "Y"}
        selected_component = test.run(system_input)
        print(selected_component)
