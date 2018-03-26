from object_tracker import object_tracker
from random_server import random_server
import networkx as nx
from networkx.algorithms import isomorphism
from matplotlib import pyplot as plt


class path_matcher(object):

    def __init__(self, online_configuration, possible_configurations):

        self.online_configuration = online_configuration
        self.possible_configurations = possible_configurations

    def run(self):
        a = 0
        for possible_config in self.possible_configurations:
            DiGM = isomorphism.GraphMatcher(self.online_configuration, possible_config)
            is_good = DiGM.subgraph_is_isomorphic()
            print(is_good)
            print(DiGM)
