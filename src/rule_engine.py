# rule engine to decide the pump to be used for governing the system
# it can potentially been used to select the best sensor for the parameter to be monitored
# even though pyKnow is meant to be action based, here is reformulate to be constriction based utilizing the enumerator to define the domain (space of solutions)
# -> utilizing the bitwise operation typical of the enumerator OR = | - AND = & - XOR = ^
from flags import Flags
from pyknow import *
_FIRST_OF_CLASS = 1


class Test_enum(Flags):
    pass


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


class Actuator_type(Flags):
    VALVE = ["Valve"]
    PUMP = ["Pump"]


class Actuator_Location(Flags):
    SOURCE = ['source']
    SINK = ['sink']
    BOOSTER = ['booster']


class Sensor_Location(Flags):
    PUMP = ['Pump']
    ENERGY_METER = ['Meter']
    SOURCE = ['source']
    SINK = ['sink']
    BOOSTER = ['booster']


class Sensors(Fact):
    """Info about the Sensor"""
    pass


class Pump_facts(Fact):
    """Info about the Pump"""
    pass


class Actuator_facts(Fact):
    """Info about the Pump"""
    pass


class Bays(Fact):
    """Info about the Pump"""
    pass


class Pump_Configurator(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.idx = 0
        self.pump = Pump()
        self.sensor = Sensor()
        self.actuator = Actuator_obj()
        self.sensor.location = Location.__all_flags__
        self.pump.location = Location.__all_flags__

    @DefFacts()
    def first(self):
        yield Actuator_facts(obj=self.actuator)
        yield Pump_facts(obj=self.pump)

    '''@Rule(Pumps(sinks=P(lambda sink: sink >= 2), loc=Location.__all_flags__, obj=MATCH.pump), salience=3)
    def use_sink_pump(self, pump):
        self.idx += 1
        pump.location = Location.__all_flags__ & Location.SINK
        pump.n_sources = 0
        self.modify(self.facts[self.idx], sources=pump.n_sources, loc=pump.location)
        print("we use the pump in the sinks")

    @Rule(Pumps(sources=P(lambda source: source > 0), loc=Location.__all_flags__, obj=MATCH.pump), salience=2)
    def use_source_pump(self, pump):
        self.idx += 1
        pump.location = Location.__all_flags__ ^ Location.SINK
        Location.ALL_SOURCES = pump.location
        pump.n_sinks = 0
        self.modify(self.facts[self.idx], sinks=pump.n_sinks, loc=pump.location)
        print(self.facts)
        print("we use the pump in the source")

    @Rule(Pumps(loc=Location.__all_flags__ ^ Location.SINK, boost='Y', obj=MATCH.pump), salience=1)
    def use_booster_pump(self, pump):
        self.idx += 1
        pump.location = Location.ALL_SOURCES & Location.BOOSTER
        pump.n_sources = 0
        self.modify(self.facts[self.idx], sources=pump.n_sources, loc=pump.location)
        print("we use the pump in the booster")'''

    '''@Rule(Actuator_facts(pumps=MATCH.n_pumps), Bays(bays=MATCH.n_bays), TEST(lambda n_pumps, n_bays: n_pumps == n_bays), Actuator_facts(obj=MATCH.actuator), Actuator_facts(obj_con=MATCH.controller))
    def actuator_selector_pump(self, actuator, controller):
        print("Actuator selection")
        actuator.type = actuator.type & Actuator_type.PUMP
        controller.type = controller.type & Pump_Mode.CONSTANT_FLOW
        self.declare(Actuator_facts(actuator_type=actuator.type))
        print(controller.type)
        print(actuator.type)

    @Rule(Actuator_facts(actuator_type=Actuator_type.PUMP), Bays(sources=MATCH.n_sources, sinks=MATCH.n_sinks), TEST(lambda n_sources, n_sinks: n_sources >= n_sinks), Actuator_facts(obj=MATCH.actuator))
    def Pump_Selector_Source(self, actuator):
        print("Pump selection")
        actuator.location = actuator.location ^ Location.SINK
        print(actuator.location)

    @Rule(Actuator_facts(actuator_type=Actuator_type.PUMP), Bays(sources=MATCH.n_sources, sinks=MATCH.n_sinks), TEST(lambda n_sources, n_sinks: n_sources < n_sinks), Actuator_facts(obj=MATCH.actuator))
    def Pump_Selector_Sink(self, actuator):
        print("Pump selection")
        actuator.location = actuator.location & Location.SINK
        print(actuator.location)'''

    @Rule(Actuator_facts(pumps_sources=MATCH.n_pumps_sources, pumps_sinks=MATCH.n_pumps_sinks),
          Actuator_facts(pumps_sources=P(lambda pumps_sources: pumps_sources > 0)),
          TEST(lambda n_pumps_sources, n_pumps_sinks: n_pumps_sources >= n_pumps_sinks),
          Actuator_facts(obj=MATCH.actuator),
          Bays(sources=MATCH.n_sources, sinks=MATCH.n_sinks),
          TEST(lambda n_sources, n_sinks: n_sources < n_sinks),
          Pump_facts(obj=MATCH.pump))
    def actuator_selector_valve(self, actuator, pump):
        print("Actuator selection")
        actuator.type = actuator.type & Actuator_type.VALVE
        pump.type = pump.type & Pump_Mode.CONSTANT_PRESSURE
        pump.location = pump.location ^ Location.SINK
        self.declare(Actuator_facts(actuator_type=actuator.type))
        print(pump.type)
        print(pump.location)
        print(actuator.type)
        #print(self.facts)

    @Rule(Actuator_facts(actuator_type=Actuator_type.VALVE))  # actuator_type=Actuator_type.VALVE))
    def just_a_consequence(self):
        print("Ti rimane da scegliere che valvola ")

    @Rule(Actuator_facts(pumps_sources=MATCH.n_pumps_sources, pumps_sinks=MATCH.n_pumps_sinks),
          TEST(lambda n_pumps_sources, n_pumps_sinks: n_pumps_sources <= n_pumps_sinks),
          Actuator_facts(obj=MATCH.actuator),
          Pump_facts(obj=MATCH.pump))
    def actuator_selector_pump(self, actuator, pump):
        print("Actuator selection")
        actuator.type = actuator.type & Actuator_type.PUMP
        pump.type = pump.type & Pump_Mode.CONSTANT_FLOW
        pump.location = Location.SINK
        self.declare(Pump_facts(pump_type=pump.type, pump_location=pump.location))
        print(pump.type)
        print(pump.location)

    @Rule(Pump_facts(pump_type=Pump_Mode.CONSTANT_FLOW),
          Actuator_facts(pumps_sources=P(lambda pumps_sources: pumps_sources == 1)),
          Actuator_facts(pumps_sinks=P(lambda pumps_sinks: pumps_sinks == 1)),
          Pump_facts(obj=MATCH.pump))
    def actuator_pump_location(self, pump):
        print("Actuator selection")
        pump.location = Location.__all_flags__ ^ Location.SINK
        self.declare(Pump_facts(pump_location=pump.location))
        print(pump.location)




class Pump(object):
    def __init__(self):
        self.location = Location.__all_flags__
        self.type = Pump_Mode.__all_flags__


class Sensor(object):
    def __init__(self):
        self.location = []
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
        feedback_variable = system_input['parameters']
        engine = Pump_Configurator()
        engine.reset()
        #engine.declare(Pumps(sources=n_sources, sinks=n_sinks, boost=booster, loc=pump.location, obj=pump))
        engine.declare(Bays(bays=n_bays))
        engine.declare(Bays(sources=n_sources, sinks=n_sinks))
        engine.declare(Actuator_facts(pumps=n_pumps, pumps_sources=n_pumps_sources, pumps_sinks=n_pumps_sinks))
        engine.declare(Actuator_facts(valves=n_valves, valves_sources=n_valves_sources, valves_sinks=n_valves_sinks))


        #engine.declare(Sensors(loc=sensor.location, obj=sensor))
        engine.run()

        #print(sensor.location)
        return "ciao"


if __name__ == "__main__":
        test = rule_engine()
        system_input = {"sinks": ["Sink_1H8"], "parameters": "Energy",
                        "setpoints": 30, "sources": ["Source_1C4"],
                        "boosted": "N"}
        available_components = {"Pumps_active": ["Pump_1C4", "Pump_1H8", "Pump_1H7"],
                                "Sensors_active": ["Sensor_1E4", "Sensor_1E7"],
                                "Valves_active": ["Valve_1H4", "Valve_1C4", "Valve_1H7", "Valve_1C7", "Valve_1H8", "Valve_1C8"],
                                "Pumps_in_sources": 1,
                                "Pumps_in_sinks": 0,
                                "Sensors_in_sources": 1,
                                "Sensors_in_sinks": 1,
                                "Valves_in_sources": 2,
                                "Valves_in_sinks": 4}
        selected_component = test.run(system_input, available_components)
        #print(selected_component.location)
