# rule engine to decide the pump to be used for governing the system
# it can potentially been used to select the best sensor for the parameter to be monitored
# even though pyKnow is meant to be action based, here is reformulate to be constriction based utilizing the enumerator to define the domain (space of solutions)
# -> utilizing the bitwise operation typical of the enumerator OR = | - AND = & - XOR = ^
from flags import Flags
from pyknow import *
_FIRST_OF_CLASS = 1
_SECOND_BEST = 2
_ALL_FLAGS_ACTUATOR_TYPE = 1
_ALL_FLAGS_PUMP_LOCATION_MODE = 2
_ALL_FLAGS_SENSOR_LOCATION_NUMBER = 3
_BOOSTED = "Y"


class Location(Flags):

    SOURCE = ['source']
    SINK = ['sink']


class Number(Flags):

    ONE = ["1"]
    TWO = ["2"]
    THREE = ["3"]


class Pump_Mode(Flags):
    """this will also be the controller name"""
    # OFF = ["OFF"] does this exist?
    CONSTANT_SPEED = ["PUMP_MODE_CONSTANT_SPEED"]               # 0
    CONSTANT_FREQUENCY = ["PUMP_MODE_CONSTANT_FREQUENCY"]       # 1
    CONSTANT_HEAD = ["PUMP_MODE_CONSTANT_HEAD"]                 # 2
    CONSTANT_PRESSURE = ["PUMP_MODE_CONSTANT_PRESSURE"]         # 3
    CONSTANT_FLOW = ["PUMP_MODE_CONSTANT_FLOW"]                 # 4
    CONSTANT_TEMP = ["PUMP_MODE_CONSTANT_TEMP"]                 # 5

class Actuator_type(Flags):
    VALVE = ["Valve"]
    PUMP = ["Pump"]


class System_facts(Fact):
    '''info about the System'''
    pass


class Sensors_facts(Fact):
    """Info about the Sensor"""
    pass


class Pump_facts(Fact):
    """Info about the Pump"""
    pass


class Actuator_facts(Fact):
    """Info about the Actuators"""
    pass


class Bays(Fact):
    """Info about the Bays"""
    pass


class Pump_Configurator(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.idx = 0
        self.pump = Pump_obj()
        self.sensor = Sensor_obj()
        self.actuator = Actuator_obj()

    @DefFacts()
    def first(self):
        yield Actuator_facts(actuator_type=Actuator_type.__all_flags__)
        yield Pump_facts(pump_mode=Pump_Mode.__all_flags__, pump_location=Location.__all_flags__)
        yield Sensors_facts(sensor_location=Location.__all_flags__, sensor_number=Number.__no_flags__)
        yield Actuator_facts(obj=self.actuator)
        yield Pump_facts(obj=self.pump)
        yield Sensors_facts(obj=self.sensor)

    # Rule that choose the valve as actuator
    '''@Rule(Actuator_facts(pumps_sources=MATCH.n_pumps_sources, pumps_sinks=MATCH.n_pumps_sinks),
          Actuator_facts(pumps_sources=P(lambda pumps_sources: pumps_sources > 0)),
          TEST(lambda n_pumps_sources, n_pumps_sinks: n_pumps_sources >= n_pumps_sinks),
          Actuator_facts(obj=MATCH.actuator),
          Bays(sources=MATCH.n_sources, sinks=MATCH.n_sinks),
          TEST(lambda n_sources, n_sinks: n_sources < n_sinks),
          Pump_facts(obj=MATCH.pump))
    def actuator_selector_valve(self, actuator, pump):
        print("Actuator selection")
        actuator.type = actuator.type & Actuator_type.VALVE
        pump.mode = pump.mode & Pump_Mode.CONSTANT_PRESSURE
        pump.location = pump.location ^ Location.SINK
        actuator.location = Location.SINK  # to be change in reality
        actuator.number = _SECOND_BEST
        self.declare(Actuator_facts(actuator_type=actuator.type, actuator_location=actuator.location))
        self.declare(Pump_facts(pump_mode=pump.mode, pump_location=pump.location))
        self.retract(_ALL_FLAGS_ACTUATOR_TYPE)
        print(self.facts)

    # Rule that should select which valve
    @Rule(Actuator_facts(actuator_type=Actuator_type.VALVE))  # actuator_type=Actuator_type.VALVE))
    def just_a_consequence(self):
        print("Ti rimane da scegliere che valvola ")

    # this is only to select the actuator type
    @Rule(Actuator_facts(pumps_sources=MATCH.n_pumps_sources, pumps_sinks=MATCH.n_pumps_sinks),
          OR(TEST(lambda n_pumps_sources, n_pumps_sinks: n_pumps_sources <= n_pumps_sinks),
          Actuator_facts(pumps_sinks=P(lambda pumps_sinks: pumps_sinks == 0))),
          Actuator_facts(obj=MATCH.actuator),
          Actuator_facts(actuator_type=Actuator_type.__all_flags__),
          Pump_facts(obj=MATCH.pump),
          Pump_facts(pump_mode=Pump_Mode.__all_flags__, pump_location=Location.__all_flags__))
    def actuator_selector_pump(self, actuator, pump):
        print("Actuator selection when pump is selected")
        actuator.type = actuator.type & Actuator_type.PUMP
        pump.mode = pump.mode & Pump_Mode.CONSTANT_FLOW
        pump.location = Location.SINK
        actuator.location = pump.location
        actuator.number = _SECOND_BEST
        self.declare(Pump_facts(pump_mode=pump.mode, pump_location=pump.location))
        self.declare(Actuator_facts(actuator_type=actuator.type, actuator_location=actuator.location))
        self.retract(_ALL_FLAGS_ACTUATOR_TYPE)
        self.retract(_ALL_FLAGS_PUMP_LOCATION_MODE)

    @Rule(Pump_facts(pump_mode=Pump_Mode.CONSTANT_FLOW),
          Actuator_facts(pumps_sources=P(lambda pumps_sources: pumps_sources == 1)),
          Actuator_facts(pumps_sinks=P(lambda pumps_sinks: 1 >= pumps_sinks >= 0)),
          Actuator_facts(obj=MATCH.actuator),
          Pump_facts(obj=MATCH.pump))
    def actuator_pump_location(self, pump, actuator):
        print("Actuator selection when pump is selected and is in source")
        pump.location = Location.__all_flags__ ^ Location.SINK
        actuator.location = pump.location
        actuator.number = _FIRST_OF_CLASS
        self.declare(Pump_facts(pump_location=pump.location))
        self.declare(Actuator_facts(actuator_location=actuator.location))'''

    # you need .MATCH to assign the variable and then pass it as argument
    # the lamba function is of the type (lambda arguments: function)
    # the P() is to self test the variable against some value
    # the TEST is to compare two different MATCHED variables


    @Rule(Sensors_facts(sensor_location=Location.__all_flags__, sensor_number=Number.__no_flags__),
          Actuator_facts(actuator_location=P(lambda actuator_location: actuator_location != Location.__all_flags__)),
          Bays(sources=MATCH.n_sources, sinks=MATCH.n_sinks),
          Actuator_facts(obj=MATCH.actuator),
          Sensors_facts(obj=MATCH.sensor))
    def sensor_selection(self, sensor, actuator, n_sinks):
        print("Sensor selection")
        sensor.location = Location.SINK
        sensor.number = n_sinks

    @Rule(Bays(sources=MATCH.n_sources, sinks=MATCH.n_sinks),
          Actuator_facts(obj=MATCH.actuator))
    def actuator_number(self, actuator, n_sinks):
        print("Now I will tell you how many actuators")
        actuator.number = n_sinks

    @Rule(Bays(sources=MATCH.n_sources, sinks=MATCH.n_sinks),
          TEST(lambda n_sources, n_sinks: n_sources > n_sinks),
          Actuator_facts(actuator_type=Actuator_type.__all_flags__),
          Pump_facts(pump_mode=Pump_Mode.__all_flags__, pump_location=Location.__all_flags__),
          Actuator_facts(obj=MATCH.actuator),
          Pump_facts(obj=MATCH.pump), salience=1)
    def sources_larger_than_sinks(self, actuator, pump, n_sinks):
        print("sources larger than sinks")
        actuator.type = actuator.type & Actuator_type.VALVE
        pump.mode = pump.mode & Pump_Mode.CONSTANT_PRESSURE
        pump.location = pump.location & Location.SOURCE
        actuator.location = actuator.location & Location.SINK
        # sensor.location = sensor.location & Location.SINK
        self.declare(Actuator_facts(actuator_location=actuator.location))
        self.retract(_ALL_FLAGS_ACTUATOR_TYPE)
        self.retract(_ALL_FLAGS_PUMP_LOCATION_MODE)

    @Rule(Bays(sources=MATCH.n_sources, sinks=MATCH.n_sinks),
          TEST(lambda n_sources, n_sinks: n_sinks >= n_sources),
          Actuator_facts(actuator_type=Actuator_type.__all_flags__),
          Pump_facts(pump_mode=Pump_Mode.__all_flags__, pump_location=Location.__all_flags__),
          Actuator_facts(obj=MATCH.actuator),
          Pump_facts(obj=MATCH.pump), salience=1)
    def sources_smaller_equal_than_sinks(self, actuator, pump, n_sinks):
        print("sources smaller equal than sinks")
        actuator.type = actuator.type & Actuator_type.PUMP
        pump.mode = pump.mode & Pump_Mode.CONSTANT_FLOW
        pump.location = pump.location & Location.SINK
        actuator.location = actuator.location & Location.SINK
        # sensor.location = sensor.location & Location.SINK
        self.declare(Actuator_facts(actuator_location=actuator.location))
        self.declare(Actuator_facts(actuator_type=actuator.type))
        self.retract(_ALL_FLAGS_ACTUATOR_TYPE)
        self.retract(_ALL_FLAGS_PUMP_LOCATION_MODE)

    @Rule(Actuator_facts(pumps_sources=MATCH.n_pumps_sources, pumps_sinks=MATCH.n_pumps_sinks),
          AND(TEST(lambda n_pumps_sources, n_pumps_sinks: n_pumps_sinks < n_pumps_sources),
          Actuator_facts(actuator_type=Actuator_type.PUMP)),
          Actuator_facts(obj=MATCH.actuator),
          Pump_facts(obj=MATCH.pump))
    def more_pumps_in_sources(self, actuator, pump, n_sinks):
        print("pumps in sources are more")
        actuator.type = actuator.type & Actuator_type.VALVE
        pump.mode = pump.mode & Pump_Mode.CONSTANT_PRESSURE
        pump.location = pump.location & Location.SOURCE
        actuator.location = actuator.location & Location.SINK
        # sensor.location = sensor.location & Location.SINK

    @Rule(Bays(sources=MATCH.n_sources, sinks=MATCH.n_sinks),
          Bays(sources=P(lambda n_sources: n_sources == _FIRST_OF_CLASS)),
          TEST(lambda n_sources, n_sinks: n_sinks == n_sources),
          Actuator_facts(actuator_type=Actuator_type.PUMP),
          Actuator_facts(obj=MATCH.actuator),
          Pump_facts(obj=MATCH.pump))
    def more_pumps_in_sources(self, actuator, pump, n_sinks):
        print("if it is one to one we prefer the source")
        actuator.location = Location.SOURCE
        pump.location = Location.SOURCE
        # sensor.location = sensor.location & Location.SINK

    @Rule(System_facts(boosted=P(lambda booster: booster == _BOOSTED)),
          #Actuator_facts(actuator_type=P(lambda actuator_type: actuator_type != Actuator_type.__all_flags__)),
          Actuator_facts(obj=MATCH.actuator),
          Pump_facts(obj=MATCH.pump),
          Bays(sources=MATCH.n_sources, sinks=MATCH.n_sinks))
    def is_it_booster(self, actuator, pump, n_sinks):
        print("I am the booster to hell")
        actuator.type = Actuator_type.PUMP
        pump.mode = Pump_Mode.CONSTANT_FLOW
        pump.location = Location.SINK
        actuator.location = Location.SINK
        self.reset()
        self.declare(Actuator_facts(actuator_type=actuator.type))
        self.declare(Bays(sources=_FIRST_OF_CLASS, sinks=n_sinks))
        self.run()                                                       # very nice move







class Pump_obj(object):
    def __init__(self):
        self.location = Location.__all_flags__
        self.mode = Pump_Mode.__all_flags__


class Sensor_obj(object):
    def __init__(self):
        self.location = Location.__all_flags__
        self.variable = ""


class Actuator_obj(object):
    def __init__(self):
        self.location = Location.__all_flags__
        self.type = Actuator_type.__all_flags__


class rule_engine(object):

    def run(self, system_input, available_components):
        print(available_components)
        n_sources = len(system_input['sources'])
        n_sinks = len(system_input['sinks'])
        n_pumps = len(available_components["Pumps_active"])
        n_pumps_sources = available_components["Pumps_in_sources"]
        n_pumps_sinks = available_components["Pumps_in_sinks"]
        n_valves = len(available_components["Valves_active"])
        n_valves_sources = available_components["Valves_in_sources"]
        n_valves_sinks = available_components["Valves_in_sinks"]
        n_sensors = len(available_components["Sensors_active"])
        n_sensors_sources = available_components["Sensors_in_sources"]
        n_sensors_sinks = available_components["Sensors_in_sinks"]
        n_bays = n_sinks + n_sources
        booster = system_input['boosted']
        print(booster)
        feedback_variable = system_input['parameters']
        engine = Pump_Configurator()
        engine.reset()
        # engine.declare(Pumps(sources=n_sources, sinks=n_sinks, boost=booster, loc=pump.location, obj=pump))
        # engine.declare(Bays(bays=n_bays))
        engine.declare(Bays(sources=n_sources, sinks=n_sinks))
        engine.declare(Actuator_facts(pumps_sources=n_pumps_sources, pumps_sinks=n_pumps_sinks))
        engine.declare(Actuator_facts(valves=n_valves, valves_sources=n_valves_sources, valves_sinks=n_valves_sinks))
        engine.declare(System_facts(boosted=booster))
        # engine.declare(Sensors(loc=sensor.location, obj=sensor))
        engine.run()

        print("the pump runs in ", engine.pump.mode)
        print("the pump is in ", engine.pump.location)
        print("the actuator is the ", engine.actuator.type)
        print("the actuator/s are located in ", engine.actuator.location)
        print("the actuator needed are ", engine.actuator.number)
        print("the sensor/s are located in ", engine.sensor.location)
        print("the sensors needed are ", engine.sensor.number)
        ideal_components = {"Ideal_Pump": engine.pump,
                            "Ideal_Actuator": engine.actuator,
                            "Ideal_Sensor": engine.sensor}
        return ideal_components


if __name__ == "__main__":
        test = rule_engine()
        system_input = {"sinks": ["Sink_1H7"], "parameters": "Energy",
                        "setpoints": 30, "sources": ["Source_1C4"],
                        "boosted": "N"}
        available_components = {"Pumps_active": ["Pump_1C4", "Pump_1H7"],
                                "Sensors_active": ["Sensor_1E4", "Sensor_1E7"],
                                "Valves_active": ["Valve_1H4", "Valve_1C4", "Valve_1H7", "Valve_1C7", "Valve_1H8", "Valve_1C8"],
                                "Pumps_in_sources": 1,
                                "Pumps_in_sinks": 1,
                                "Sensors_in_sources": 1,
                                "Sensors_in_sinks": 1,
                                "Valves_in_sources": 2,
                                "Valves_in_sinks": 4}
        selected_component = test.run(system_input, available_components)
        #print(selected_component.location)

        '''Satisfied Cases:
        1 source - 1 sink
        1 source - 2 sinks
        2 sources - 2 sinks
        3 sources - 1 sink -- also booster
        3 sources - 2 sinks -- also booster
'''

# with double source and one sink you control with the valve at the sink and not with the pumps at the source .. can you imagine the feedback? Avresti un hunting bestiale. In realtà sta cosa di due sources in parallelo è sbagliata
