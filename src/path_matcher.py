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

        print("I start computing")

        print("try extracting subgraph")
        extracted_subgraph = online_configuration.subgraph(possible_configurations.nodes)
        print("subgraph extracted")
        if(set(extracted_subgraph.edges) == set(possible_configurations.edges)):
            print("Edges match")
            if (set(extracted_subgraph.nodes) == set(possible_configurations.nodes)):
                print("Nodes matches")
                print("Configuration  matches online reading - it is shown in figure")
                print("check isomorpishm")
                # DiGM = isomorphism.GraphMatcher(extracted_subgraph, possible_configurations)
                nx.is_isomorphic(extracted_subgraph, possible_configurations)
                print("isomorpishm confirmed \n")

                '''plt.figure(idx + _OFFSET_FIGURE)
                #plt.figure()
                plt.clf()
                plt.title('Connected Subgraph of Online Configuration')
                nx.draw_kamada_kawai(extracted_subgraph, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
                plt.pause(0.001)'''
                return _MATCHED
            else:
                '''plt.figure(idx + _OFFSET_FIGURE)
                plt.clf()
                plt.title('Disconnected Subgraph of Online Configuration')
                nx.draw_kamada_kawai(extracted_subgraph, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
                plt.pause(0.001)'''
                return _UNMATCHED
        else:
            '''plt.figure(idx + _OFFSET_FIGURE)
            plt.clf()
            plt.title('Disconnected Subgraph of Online Configuration')
            nx.draw_kamada_kawai(extracted_subgraph, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)
            plt.pause(0.001)'''
            return _UNMATCHED
