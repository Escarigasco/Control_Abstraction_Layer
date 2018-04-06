from matplotlib import pyplot as plt
import networkx as nx
from networkx.algorithms import isomorphism

_OFFSET_FIGURE = 6
_OFFSET_IDX = 1


class path_matcher(object):

    def __init__(self, online_configuration):

        self.online_configuration = online_configuration

    def run(self, possible_configurations, idx):
        short_list = []
        print("I start computing")

        print("try extracting subgraph")
        extracted_subgraph = self.online_configuration.subgraph(possible_configurations.nodes)
        print("subgraph extracted")
        if(set(extracted_subgraph.edges) == set(possible_configurations.edges)):
            print("Edges match")
            if (set(extracted_subgraph.nodes) == set(possible_configurations.nodes)):
                print("Nodes matches")
                print("Configuration {0} matches online reading - it is shown in figure {1} ".format(idx + _OFFSET_IDX, idx + _OFFSET_IDX))
                print("check isomorpishm")
                # DiGM = isomorphism.GraphMatcher(extracted_subgraph, possible_configurations)
                nx.is_isomorphic(extracted_subgraph, possible_configurations)
                print("isomorpishm confirmed \n")

                plt.figure(idx + _OFFSET_FIGURE)
                plt.title('Connected Subgraph of Online Configuration')
                nx.draw_kamada_kawai(extracted_subgraph, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
                return True
            else:
                plt.figure(idx + _OFFSET_FIGURE)
                plt.title('Disconnected Subgraph of Online Configuration')
                nx.draw_kamada_kawai(extracted_subgraph, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
                return False
        else:
            plt.figure(idx + _OFFSET_FIGURE)
            plt.title('Disconnected Subgraph of Online Configuration')
            nx.draw_kamada_kawai(extracted_subgraph, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
            return False

        '''print("check isomorpishm")
        DiGM = isomorphism.GraphMatcher(extracted_subgraph, self.possible_configurations[i])
        is_a_match = DiGM.is_isomorphic()
        if (is_a_match):
            print("Configuration {0} is compatible \n".format(i))
            short_list.append(self.possible_configurations[i])
        else:
            print("Configuration {0} is not achievable \n".format(i))'''

        # return short_list

# Yes or do it brute force and that's it for some reason it seams to crash using is_isomorphic
