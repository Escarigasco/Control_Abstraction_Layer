
import pickle
import sys
import time

_AVAILABLE_COMPONENTS = "available_components"
_BUSBARS = "busbar"
_COUNTER = "counter"
_CONTROLLER_NAME = "controller_name"
_DESCRIPTION = "description"
_GRAPH = "graph"
_INPUTS = "inputs"
_MATCH = 'match'
_PUMPS = 'Pumps_active'
_PUMP = "Pump"
_SENSORS = 'Sensors_active'
_SETPOINT = "setpoints"
_STATE = "state"
_VALVES = 'Valves_active'
_VALVES_TO_SHUT = 'Valves_to_shut'
_ACTUATE = "actuate"
_FINAL_BOOSTER = "final_booster"
_START_SOURCE = "start_source"
_MIDDLE_BOOSTER = "middle_booster"
_BEGIN_WITH = 0     # the tuple
_END_WITH = 1   # the tuple
_BIT_SHIFT = 1
_LAST_ELEMENT = -1
_INIT = "init"
_COMPONENTS = "components"
_SHUTTER = "shutter"


class logic(object):
    def __init__(self, comms, work_q, work_pauser, translator, interface):
        a = 0
        self.translator = translator
        self.comms = comms
        self.work_q = work_q
        self.work_pauser = work_pauser
        self.busy_busbars = {}
        self.interface = interface
        self.system_pumps = self.interface.get_system_pumps()
        self.system_valves = self.interface.get_system_valves()

    def switchboard_initialization(self, interface):
        system_pumps = self.system_pumps.keys()
        system_valves = self.system_valves.keys()
        translated_valves = []
        translated_pumps = []
        for valve in system_valves:
            translated_valves.append(self.translator.components(valve))
        for pump in system_pumps:
            translated_pumps.append(self.translator.components(pump))
        init_message = {_DESCRIPTION: _INIT, _PUMP: translated_pumps, _VALVES_TO_SHUT: translated_valves}
        feedback = self.comms.send(init_message)
        if not feedback:
            print("Uknown status of switchboard")
            sys.exit()

    '''logic --> the first one of the tuple boost the second one -- e.g. [(S2, S1),(S3,S2)] means that S3 boosts S2 that boosts S1'''
    def check_sources(self, system_input):
        source_evaluator = {}
        for configuration in system_input.keys():
            if (system_input[configuration]):
                if system_input[configuration]["boosted"]:
                    for couple in system_input[configuration]["boosted"]:
                        for source in couple:
                            source_evaluator[source] = 2
                    for couple in system_input[configuration]["boosted"]:
                        for source in couple:
                            if couple.index(source) == _BEGIN_WITH:
                                source_evaluator[source] = source_evaluator[source] << _BIT_SHIFT
                            else:
                                source_evaluator[source] = source_evaluator[source] >> _BIT_SHIFT
                    system_input[configuration][_MIDDLE_BOOSTER] = []
                    for source in source_evaluator.keys():
                        if source_evaluator[source] == 1:
                            system_input[configuration][_START_SOURCE] = source
                        elif source_evaluator[source] == 2:
                            system_input[configuration][_MIDDLE_BOOSTER].append(source)
                        elif source_evaluator[source] == 4:
                            system_input[configuration][_FINAL_BOOSTER] = source
                    system_input[configuration]["boosted"] = 'Y'
                else:
                    system_input[configuration]["boosted"] = 'N'
        return system_input

    def configurations_request_analyser(self, processed_configurations, system_input, mssgr):
        requested_configurations_names = []
        processed_configurations_names = []
        requested_configuration = {}
        for name in processed_configurations.keys():
            processed_configurations_names.append(name)
        for configuration in system_input.keys():
            if (system_input[configuration]):
                request_name = str(system_input[configuration]["sources"]) + str(system_input[configuration]["sinks"]) + str(system_input[configuration]["boosted"])
                requested_configurations_names.append(request_name)
                requested_configuration[request_name] = system_input[configuration]
        # First I check the ones I should destroy
        if processed_configurations_names:
            for name in processed_configurations_names:
                if (name in requested_configurations_names):
                    #print(processed_configurations[name][_INPUTS][_SETPOINT])
                    #print(requested_configuration[name][_SETPOINT])
                    if (processed_configurations[name][_INPUTS][_SETPOINT] != requested_configuration[name][_SETPOINT]):
                        self.set_point_changer(name, requested_configuration[name][_SETPOINT])
                        processed_configurations[name][_INPUTS][_SETPOINT] = requested_configuration[name][_SETPOINT]
                    else:
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
                        new_name = str(system_input[configuration]["sources"]) + str(system_input[configuration]["sinks"]) + str(system_input[configuration]["boosted"]) # the logic is to check the name matching and then also the inputs matching and do something about it
                        if (name == new_name):
                            processed_configurations[name][_INPUTS] = system_input[configuration]
                            processed_configurations[name][_STATE] = "Inactive"
                            processed_configurations[name][_MATCH] = "Unmatched"
                            processed_configurations[name][_GRAPH] = []
                            processed_configurations[name][_COUNTER] = 0
                            processed_configurations[name][_BUSBARS] = []
                            processed_configurations[name][_AVAILABLE_COMPONENTS] = []
        return processed_configurations

    def find_suitable_setup(self, processed_configurations, pb):
        self.work_pauser.put(False)

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
        '''this is slightly redundant as when a controller is shutted the pumps are turned off'''
        print("Let me shut down some pumps first")
        configuration_pumps = []
        translated_pumps = []
        for name in processed_configurations.keys():
            configuration_pumps += processed_configurations[name][_AVAILABLE_COMPONENTS][_PUMPS]
        configuration_pumps = [pump.ID for pump in configuration_pumps]
        print("These are the pumps I am going to use ", configuration_pumps)
        all_other_pumps = self.system_pumps.keys()
        pumps_to_shut = [pump for pump in all_other_pumps if pump not in configuration_pumps]
        print("These are the pumps to shut ", pumps_to_shut)
        for pump in pumps_to_shut:
            translated_pumps.append(self.translator.components(pump))
        init_message = {_DESCRIPTION: _SHUTTER, _PUMP: translated_pumps}
        feedback = self.comms.send(init_message)
        print(feedback)

        print("I actuate the suitable setup")
        actuating_message = {}
        valves_translated = []
        valves_to_shut_translated = []
        for name, attributes in processed_configurations.items():
            if (processed_configurations[name][_STATE] == "Inactive"):
                if (processed_configurations[name][_MATCH] == "Unmatched"):
                    for valve in processed_configurations[name][_AVAILABLE_COMPONENTS][_VALVES]:
                        valves_translated.append(self.translator.components(valve.ID))
                    for valve in processed_configurations[name][_AVAILABLE_COMPONENTS][_VALVES_TO_SHUT]:
                        valves_to_shut_translated.append(self.translator.components(valve.ID))
                    actuating_message = {_DESCRIPTION: _ACTUATE, _VALVES: valves_translated, _VALVES_TO_SHUT: valves_to_shut_translated}
                    #print(actuating_message[_VALVES])
                    #print(actuating_message[_VALVES_TO_SHUT])
#                    sys.exit()
                    #if (complete):
                        #processed_configurations[name][_MATCH] = "Matched"
            else:
                print("Skipped")

        if actuating_message:
            complete = self.comms.send(actuating_message)
        self.work_pauser.put(True)
        time.sleep(5)                     # you need this to allow the online reader to get the new set up

        return processed_configurations

    def controller_starter(self, processed_configurations, pm, mssgr, latest_configuration_file_write):

        what_comes_out_the_cilinder = []
        print("I check the compatibility and start the controller")
        while not self.work_q.empty():
            what_comes_out_the_cilinder.append(self.work_q.get())
        if what_comes_out_the_cilinder:
            self.online_configuration = what_comes_out_the_cilinder[_LAST_ELEMENT]
        if (processed_configurations):
            for name, attributes in processed_configurations.items():
                if (processed_configurations[name][_STATE] == "Inactive"):
                    processed_configurations[name][_MATCH] = pm.run(processed_configurations[name][_GRAPH], self.online_configuration)
                    if (processed_configurations[name][_MATCH] == "Matched"):
                        print("Preparing Message")
                        processed_configurations[name][_STATE] = mssgr.run(processed_configurations[name][_AVAILABLE_COMPONENTS], processed_configurations[name][_INPUTS], name)
            #            if (processed_configurations[name][_STATE] == "Active"):
                    else:
                        print("There is no match between request and Switchboad setting. Configuration {0} deleted".format(processed_configurations[name]))

                else:
                    print("Skipped")
            #print(self.busy_busbars)
            self.print_on_file(latest_configuration_file_write, processed_configurations)
        return processed_configurations

    def controller_restarter(self, processed_configurations, pm, mssgr):
        print("I am restarting the processes")
        what_comes_out_the_cilinder = []
        if (processed_configurations):
            while not self.work_q.empty():
                what_comes_out_the_cilinder.append(self.work_q.get())
            if what_comes_out_the_cilinder:
                self.online_configuration = what_comes_out_the_cilinder[_LAST_ELEMENT]
            for name, attributes in processed_configurations.items():
                    processed_configurations[name][_MATCH] = pm.run(processed_configurations[name][_GRAPH], self.online_configuration)
                    if (processed_configurations[name][_MATCH] == "Matched"):
                        processed_configurations[name][_STATE] = mssgr.run(processed_configurations[name][_AVAILABLE_COMPONENTS], processed_configurations[name][_INPUTS], name)
                        self.busy_busbars[name] = processed_configurations[name][_BUSBARS]

            return processed_configurations

    def inactive_configuration_cleaner(self, processed_configurations, latest_configuration_file_write):
        processed_configurations_names = []
        for name in processed_configurations.keys():
            processed_configurations_names.append(name)
        for name in processed_configurations_names:
            if (processed_configurations[name][_STATE] == "Inactive"):
                self.busy_busbars.pop(name)
                processed_configurations.pop(name)
        if not processed_configurations:
            self.print_on_file(latest_configuration_file_write)
        return processed_configurations

    def check_the_match(self, processed_configurations, pm, mssgr):
        #print("I check the match and match won")
        what_comes_out_the_cilinder = []
        while not self.work_q.empty():
            what_comes_out_the_cilinder.append(self.work_q.get())
        if what_comes_out_the_cilinder:
            self.online_configuration = what_comes_out_the_cilinder[_LAST_ELEMENT]

        processed_configurations_names = []
        for name in processed_configurations.keys():
            processed_configurations_names.append(name)
        for name in processed_configurations_names:
            if (processed_configurations[name][_MATCH] == pm.run(processed_configurations[name][_GRAPH], self.online_configuration)):
                pass
            else:
                processed_configurations[name][_STATE] = mssgr.kill(processed_configurations[name][_INPUTS], name)
                if (processed_configurations[name][_STATE] == "Inactive"):
                    self.busy_busbars.pop(name)
                    processed_configurations.pop(name)

        return processed_configurations

    def set_point_changer(self, name, setpoint):
        print("I am changing the setpoint")
        new_setpoint = {_DESCRIPTION: _SETPOINT, _CONTROLLER_NAME: name, _SETPOINT: setpoint}
        print(new_setpoint)
        #sys.exit()
        feedback = self.comms.send(new_setpoint)
        print(feedback)

    def clear_everything(self, processed_configurations):
        processed_configurations_names = []
        for name in processed_configurations.keys():
            processed_configurations_names.append(name)
        for name in processed_configurations_names:
                self.busy_busbars.pop(name)
                processed_configurations.pop(name)

    def print_on_file(self, latest_configuration_file_write, processed_configurations=[]):
        if processed_configurations:
            latest_configuration_file_write.truncate(_BEGIN_WITH)  # redundant the load get rid of the contents anyway - no fundamental not to keep witing configurations onf the top of the other
            data = pickle.dump(processed_configurations, latest_configuration_file_write)
            #file.write(data)
        else:
            latest_configuration_file_write.truncate(_BEGIN_WITH)  # redundant the load get rid of the contents anyway - no fundamental not to keep witing configurations onf the top of the other
