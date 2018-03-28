from matplotlib import pyplot as plt
import networkx as nx
from networkx.algorithms import isomorphism

_OFFSET_FIGURE = 6


class path_matcher(object):

    def __init__(self, online_configuration, possible_configurations):

        self.online_configuration = online_configuration
        self.possible_configurations = possible_configurations

    def run(self):
        short_list = []

        print("I start computing")

        for i in range(0, (len(self.possible_configurations))):

            print("try extracting subgraph")
            extracted_subgraph = self.online_configuration.subgraph(self.possible_configurations[i].nodes)
            print("subgraph extracted")
            plt.figure(i + _OFFSET_FIGURE)
            plt.title('Subgraph {0}'.format(i))
            nx.draw_kamada_kawai(extracted_subgraph, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
            print("check isomorpishm")
            DiGM = isomorphism.GraphMatcher(extracted_subgraph, self.possible_configurations[i])
            is_a_match = DiGM.is_isomorphic()
            if (is_a_match):
                print("Configuration {0} is compatible \n".format(i))
                short_list.append(self.possible_configurations[i])
            else:
                print("Configuration {0} is not achievable \n".format(i))

        return short_list
