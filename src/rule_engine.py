from pyknow import *

import networkx as nx
from networkx.algorithms import isomorphism
from matplotlib import pyplot as plt
#from enum import IntFlag, auto
from aenum import Enum, Flag, IntFlag, auto
import re


class Parameter(Flag):

    _init_ = 'value string'

    ENERGY = auto(), 'energy'
    TEMPERATURE = 2, 'temperature'
    PRESSURE = 3, 'pressure'

    def __str__(self):
        return self.string

    @classmethod
    def _missing_value_(cls, value):
        for member in cls:
            if member.string == value:
                return member


class Location(Flag):
    _init_ = 'value string'

    '''SOURCE = auto() # , 'Source'
    SINK = auto() # , 'Sink'
    BOOSTER = auto() # , 'Booster'
    ALL = SOURCE | SINK | BOOSTER'''

    SOURCE = 1, 'source'
    SINK = 2, 'sink'
    BOOSTER = 3, 'booster'

    def __str__(self):
        return self.string

    @classmethod
    def _missing_value_(cls, value):
        for member in cls:
            if member.string == value:
                return member


class Color(Flag):
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Flag):
    L = 1
    M = 2
    S = 3
    ALL = 4



class Shirt(Fact):
    """Info about the Sensor"""
    pass


class Sensors(Fact):
    """Info about the Sensor"""
    pass


class Pumps(Fact):
    """Info about the Sensor"""
    pass


class Shirt_Configurator(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.idx = 0

    @Rule(Sensors(color=Color.GREEN, variable='shirt' << W(), size=Size.ALL))  # , colour_list='cl' << W(), size='sl' << W()))
    def cautious(self, shirt):
        self.idx += 1
        print("Fire Rule 1")
        shirt.colour = Color.GREEN
        shirt.size = Size.L | Size.M
        print(self.facts)
        self.modify(self.facts[self.idx], size=shirt.size)
        print(self.facts)
        print("Exit Rule 1")

    @Rule(Sensors(color=Color.GREEN, variable='shirt' << W(), size=Size.M | Size.L))  # , colour_list='cl' << W(), size='sl' << W()))
    def check_size(self, shirt):
        self.idx += 1
        print("Fire Rule 2")
        print(self.facts)
        shirt.size = Size.ALL
        self.modify(self.facts[self.idx], size=shirt.size)
        print(self.facts)
        print("Exit Rule 2")

    @Rule(Sensors(param=Parameter.ENERGY, var='sensor' << W()))  # , colour_list='cl' << W(), size='sl' << W()))
    def check_parameter(self, sensor):
        sensor.variable = str(Parameter.ENERGY)
        print("it is ok")
        print(sensor.variable)

    @Rule(Pumps(sinks=P(lambda sink: sink >= 2),sources=P(lambda source: source > 0), var='pump' << W()))   # , colour_list='cl' << W(), size='sl' << W()))
    def use_sink_pump(self, pump):
        self.idx += 1
        pump.location = str(Location.SINK)
        pump.n_sources = 0
        self.modify(self.facts[self.idx], sources=pump.n_sources, loc=pump.location)
        print("we use the pump in the sinks")

    @Rule(Pumps(sinks=P(lambda sink: (sink < 2)and(sink > 0)), sources=P(lambda source: source > 0), var='pump' << W()))  # , colour_list='cl' << W(), size='sl' << W()))
    def use_source_pump(self, pump):
        self.idx += 1
        pump.location = str(Location.SOURCE), str(Location.BOOSTER)
        pump.n_sinks = 0
        self.modify(self.facts[self.idx], sinks=pump.n_sinks, loc=Location.SOURCE)
        print("we use the pump in the source")

    @Rule(Pumps(loc=Location.SOURCE, sources=P(lambda source: source > 0), boost='Y', var='pump' << W()))  # , colour_list='cl' << W(), size='sl' << W()))
    def use_booster_pump(self, pump):
        self.idx += 1
        pump.location = str(Location.BOOSTER)
        pump.n_sinks = 0
        pump.n_sources = 0
        self.modify(self.facts[self.idx], sources=pump.n_sources, loc=pump.location)
        print("we use the pump in the booster")


class Pump(object):
    def __init__(self):
        self.location = []



class Sensor(object):
    pass


class shirt(object):

    def __init__(self):
        self.name = "maietta"

    def __repr__(self):
        return "{0}".format(self.name)

    def __str__(self):
        return "{0}".format(self.name)


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
        engine = Shirt_Configurator()
        engine.reset()
        pump = Pump()
        sens = Sensor()
        # pump.location = Location.ALL
        pump.n_sources = n_sources
        pump.n_sinks = n_sinks
        engine.declare(Pumps(sources=n_sources, sinks=n_sinks, boost=booster, var=pump))
        engine.run()

        return pump

if __name__ == "__main__":
        test = rule_engine()
        test.run()
