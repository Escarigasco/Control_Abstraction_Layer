from pyknow import *
import networkx as nx
from networkx.algorithms import isomorphism
from matplotlib import pyplot as plt


class Light(Fact):
    """Info about the traffic light."""
    pass


class Busbar(Fact):
    """Info about the traffic light."""
    pass


class Valve(Fact):
    """Info about the traffic light."""
    pass


class RobotCrossStreet(KnowledgeEngine):

    def __init__(self, graph):
        self.graph = graph
        super().__init__()

    @Rule(Busbar(busbar='device' << W(), ID='1H'),
          #Busbar(ID='1H'),
          Valve(valve='valve' << W(), connection='1H', status=1))
    def select_busbar(self, device, valve):
        self.graph.add_edges_from([(device.get_name(), valve.get_name())])




    @Rule(Light(variable='test_object' << W()), salience=1)
    def test_name(self, test_object):
        print("ciaone")
        if (test_object.size == 'L'):
            print(test_object.get_colour())

    @Rule(Light(color='green'))
    def green_light(self):
        print("Walk")


    @Rule(Light(color='red'))
    def red_light(self):
        print("Don't walk")

    @Rule('light' << Light(color=L('yellow') | L('blinking-yellow')))
    def cautious(self, light):
        print("Be cautious because light is", light["color"])


class shirt(object):
    def __init__(self):
        self.name = "maietta"
        self.colour = "green"
        self.size = "L"

    def set_colour(self, colour):
        self.colour = colour
        print(self.colour)

    def get_colour(self):
        return(self.colour)

    def __repr__(self):
        return "{0}".format(self.name)

    def __str__(self):
        return "{0}".format(self.name)


class rule_engine(object):

    def __init__(self, interface):
        print("I am here")
        self.interface = interface

    def run(self):
        Graph = nx.DiGraph()
        engine = RobotCrossStreet(Graph)
        engine.reset()
        system_bays = self.interface.get_hydraulic_bays()
        system_pumps = self.interface.get_system_pumps()
        system_sensors = self.interface.get_system_sensors()
        system_valves = self.interface.get_system_valves()
        system_connectors = self.interface.get_system_connectors()
        system_lines = self.interface.get_system_lines()
        system_pipes = self.interface.get_system_pipes()
        system_connected_devices = self.interface.get_connected_devices()
        system_bays = self.interface.get_hydraulic_bays()
        system_busbars = self.interface.build_busbars(system_pipes)

        for busbar in system_busbars.keys():
            engine.declare(Busbar(busbar=system_busbars[busbar], ID=system_busbars[busbar].get_name()))
            Graph.add_node(busbar)
        for valve in system_valves.keys():
            engine.declare(Valve(valve=system_valves[valve], connection=system_valves[valve].get_connection(), status=system_valves[valve].get_status()))
            Graph.add_node(valve)


        newshirt = shirt()
        oldshirt = shirt()
        oldshirt.set_colour("lilla")


        color = 'green'
        engine.declare(Light(color=color))
        engine.declare(Light(variable=newshirt))
        engine.declare(Light(variable=oldshirt))

        engine.run()
        nx.draw(Graph, with_labels=True)
        plt.show()
