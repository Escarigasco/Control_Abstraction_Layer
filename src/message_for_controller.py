
class message_for_controller(object):

        def __init__(self, unique, system_input, interface):
            system_valves = interface.get_system_valves()
            system_lines = interface.get_system_lines()
            system_pipes = interface.get_system_pipes()
            system_pumps = interface.get_system_pumps()
            system_sensors = interface.get_system_sensors()
            system_busbars = interface.build_busbars(system_pipes)
            system_connected_devices = interface.get_connected_devices()
            system_components = {**system_sensors, **system_busbars, **system_valves, **system_connected_devices, **system_valves, **system_pumps}
            object_nodes = {}

            nodes = list(unique.nodes)
            for node in nodes:
                object_nodes[node] = system_components[node]
                print(object_nodes[node])


            while(1):
                for successor in list(unique.successors(node)):
                    print("{0}\n".format(successor))
                    node = successor
                break
            # while(1):
                  #  node = unique.successors(node)






# deliver only the list of relevant component returning a dictionary stating the actuator and the feedback signal e.g. for the first use case will be pump x sensor and that's i
