# Class that implement the iso_morphic algorithm to check the compatibility of the online configuration with the user inputs

from matplotlib import pyplot as plt
import networkx as nx
from networkx.algorithms import isomorphism

_OFFSET_FIGURE = 6
_OFFSET_IDX = 1
_MATCHED = "Matched"
_UNMATCHED = "Unmatched"


class path_matcher(object):

    def __init__(self):

        #self.online_configuration = online_configuration
        plt.ion()
        plt.show()

    def run(self, possible_configurations, online_configuration):

        #print("I start computing the isomorphism", end="\r")

        # print("try extracting subgraph")
        extracted_subgraph = online_configuration.subgraph(possible_configurations.nodes)
        # print("subgraph extracted")
        if(set(extracted_subgraph.edges) == set(possible_configurations.edges)):
            # print("Edges match")
            if (set(extracted_subgraph.nodes) == set(possible_configurations.nodes)):
                # print("Nodes matches")
                #print("Configuration  matches online reading - it is shown in figure")
                #print("check isomorpishm")
                # DiGM = isomorphism.GraphMatcher(extracted_subgraph, possible_configurations)
                nx.is_isomorphic(extracted_subgraph, possible_configurations)

                print("isomorpishm confirmed", end="\r")

                return _MATCHED
            else:

                return _UNMATCHED
        else:

            return _UNMATCHED
