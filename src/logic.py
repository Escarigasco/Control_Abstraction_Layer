_AVAILABLE_COMPONENTS = "available_components"
_BOOSTER_NAME = "Source_1BH4"
_BUSBARS = "busbar"
_COUNTER = "counter"
_DESCRIPTION = "description"
_GRAPH = "graph"
_INPUTS = "inputs"
_MATCH = 'match'
_PUMPS = 'Pumps_active'
_SENSORS = 'Sensors_active'
_STATE = "state"
_VALVES = 'Valves_active'
_ACTUATE = "actuate"


class logic(object):
    def __init__(self, comms, work_q, translator):
        a = 0
        self.translator = translator
        self.comms = comms
        self.work_q = work_q
        self.busy_busbars = {}

    def check_sources(self, system_input):
        for configuration in system_input.keys():
            if (system_input[configuration]):
                for source in system_input[configuration]["sources"]:
                    if (source == _BOOSTER_NAME):
                        system_input[configuration]["boosted"] = 'N'
            return system_input

    def find_suitable_setup(self, processed_configurations, pb):
        print("I look for a suitable setup")
        for name, attributes in processed_configurations.copy().items():
            if (processed_configurations[name][_STATE] == "Inactive"):
                if (processed_configurations[name][_MATCH] == "Unmatched"):
                    suitable_setup = pb.run(processed_configurations[name][_INPUTS], self.busy_busbars)
                    if suitable_setup:
                        processed_configurations[name][_GRAPH] = suitable_setup[_GRAPH]
                        processed_configurations[name][_AVAILABLE_COMPONENTS] = suitable_setup[_AVAILABLE_COMPONENTS]
                        processed_configurations[name][_BUSBARS] = suitable_setup[_BUSBARS]
                        self.busy_busbars[name] = suitable_setup[_BUSBARS]
                    else:
                        print("Configuration {0} is not actuable - request deleted".format(processed_configurations[name]))
                        processed_configurations.pop(name)
            else:
                print("Skipped")

        return processed_configurations

    def actuate_suitable_setup(self, processed_configurations):
        print("I actuate the suitable setup")
        actuating_message = {}
        valves_translated = []
        for name, attributes in processed_configurations.items():
            if (processed_configurations[name][_STATE] == "Inactive"):
                if (processed_configurations[name][_MATCH] == "Unmatched"):

                    for valve in processed_configurations[name][_AVAILABLE_COMPONENTS][_VALVES]:
                        valves_translated.append(self.translator.components(valve.ID))
                    actuating_message = {_DESCRIPTION: _ACTUATE, _VALVES: valves_translated}
                    complete = self.comms.send(actuating_message)
                    if (complete):
                        processed_configurations[name][_MATCH] = "Matched"
            else:
                print("Skipped")

        return processed_configurations

    def check_compatibility(self, processed_configurations, pm, mssgr):
        print("I check the compatibility and start the controller")
        if (not self.work_q.empty()):
            print("la queue non è vuota!")
            self.online_configuration = self.work_q.get()
        if (processed_configurations):
            for name, attributes in processed_configurations.items():
                if (processed_configurations[name][_STATE] == "Inactive"):
                    processed_configurations[name][_MATCH] = pm.run(processed_configurations[name][_GRAPH], self.online_configuration)
                    if (processed_configurations[name][_MATCH] == "Matched"):
                        print("Preparing Message")
                        processed_configurations[name][_STATE] = mssgr.run(processed_configurations[name][_AVAILABLE_COMPONENTS], processed_configurations[name][_INPUTS], name)
                        # if (processed_configurations[name][_STATE] == "Inactive"):
                        #    processed_configurations[name][_COUNTER] = 1
                else:
                    print("Skipped")

        return processed_configurations

    def configurations_checker(self, processed_configurations, system_input, mssgr):
        requested_configurations_names = []
        processed_configurations_names = []
        for name in processed_configurations.keys():
            processed_configurations_names.append(name)
        for configuration in system_input.keys():
            if (system_input[configuration]):
                requested_configurations_names.append(str(system_input[configuration]["sources"]) + str(system_input[configuration]["sinks"]))
        # First I check the ones I should destroy
        if processed_configurations_names:
            for name in processed_configurations_names:
                if (name in requested_configurations_names):
                    #TODO the change of setpoint
                    pass
                else:
                    if (processed_configurations[name][_STATE] == "Active"):
                        print("Kill started process")
                        processed_configurations[name][_STATE] = mssgr.kill(processed_configurations[name][_INPUTS], name)
                        if (processed_configurations[name][_STATE] == "Inactive"):
                            self.busy_busbars.pop(name)
                            processed_configurations.pop(name)

        for name in requested_configurations_names:
            if (name in processed_configurations_names):
                pass
            else:
                for configuration in system_input.keys():
                    if (system_input[configuration]):
                        new_name = str(system_input[configuration]["sources"]) + str(system_input[configuration]["sinks"])  # the logic is to check the name matching and then also the inputs matching and do something about it
                        if (name == new_name):
                            processed_configurations[name][_INPUTS] = system_input[configuration]
                            processed_configurations[name][_STATE] = "Inactive"
                            processed_configurations[name][_MATCH] = "Unmatched"
                            processed_configurations[name][_GRAPH] = []
                            processed_configurations[name][_COUNTER] = 0
                            processed_configurations[name][_BUSBARS] = []
                            processed_configurations[name][_AVAILABLE_COMPONENTS] = []

        print(processed_configurations)
        return processed_configurations
