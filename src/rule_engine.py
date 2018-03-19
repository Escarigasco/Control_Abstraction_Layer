from pyknow import *

class Light(Fact):
    """Info about the traffic light."""
    pass


class RobotCrossStreet(KnowledgeEngine):
    def __init__(self, test):
        self.obj = test
        super().__init__()

    @Rule(Light(variable='test_object' << W()), salience=1)
    def test_name(self, test_object):
        print("ciaone")
        if (test_object.size == 'L'):
            print(test_object.get_colour())

    @Rule(Light(color='green'))
    def green_light(self):
        print("Walk")
        self.obj.set_colour("red")

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

    def __init__(self, system_sensors, system_pumps, system_valves, system_connected_devices, system_bays, system_busbars, system_input, sensors_position, lines_valve_connection):
        print("I am here")
        newshirt = shirt()
        oldshirt = shirt()
        oldshirt.set_colour("lilla")
        engine = RobotCrossStreet(newshirt)
        engine.reset()
        color = 'green'
        engine.declare(Light(color=color))
        engine.declare(Light(variable=newshirt))
        engine.declare(Light(variable=oldshirt))
        print(engine.facts)
        engine.run()
