from flags import Flags
from pyknow import *
_FIRST_OF_CLASS = 1


class Location(Flags):

    SOURCE = ['source']
    SINK = ['sink']
    BOOSTER = ['booster']


class Sensors(Fact):
    """Info about the Sensor"""
    pass


class Pumps(Fact):
    """Info about the Sensor"""
    pass


class Pump_Configurator(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.idx = 0

    @Rule(Pumps(sinks=P(lambda sink: sink >= 2), loc=Location.__all_flags__, var='pump' << W()), salience=3)
    def use_sink_pump(self, pump):
        self.idx += 1
        pump.location = Location.__all_flags__ & Location.SINK
        pump.n_sources = 0
        self.modify(self.facts[self.idx], sources=pump.n_sources, loc=pump.location)
        print("we use the pump in the sinks")

    @Rule(Pumps(sources=P(lambda source: source > 0), loc=Location.__all_flags__, var='pump' << W()))
    def use_source_pump(self, pump):
        self.idx += 1
        pump.location = Location.__all_flags__ ^ Location.SINK
        Location.ALL_SOURCES = pump.location
        pump.n_sinks = 0
        self.modify(self.facts[self.idx], sinks=pump.n_sinks, loc=pump.location)
        print("we use the pump in the source")

    @Rule(Pumps(loc=Location.__all_flags__ ^ Location.SINK, boost='Y', var='pump' << W()))
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
    pass


class rule_engine(object):

    def run(self, system_input):
        '''parameter = 'energy'
        for n in Parameter:
            print(str(n))
            if (str(n) == parameter):
                test = n
                print(test)'''
        n_sources = len(system_input['sources'])
        n_sinks = len(system_input['sinks'])
        booster = system_input['boosted']
        engine = Pump_Configurator()
        engine.reset()
        pump = Pump()
        sens = Sensor()
        pump.location = Location.__all_flags__
        pump.n_sources = n_sources
        pump.n_sinks = n_sinks
        engine.declare(Pumps(sources=n_sources, sinks=n_sinks, boost=booster, loc=pump.location, var=pump))
        engine.run()

        return pump

    '''def build_solution_space(self, space):
        solution_space = space(_FIRST_OF_CLASS)
        for n in Location:
            solution_space = solution_space | n
        space.ALL = solution_space
        return solution_space'''

if __name__ == "__main__":
        test = rule_engine()
        test.run()
