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



        print("I start computing")

        for n in self.possible_configurations[1]:
            print(n)
        #print(self.possible_configurations[0].edges)
        #print(nx.compose(self.possible_configurations[0], self.online_configuration))

        G = self.online_configuration.subgraph(self.possible_configurations[0].nodes)
        plt.figure(6)
        nx.draw_circular(G, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)


        H = self.online_configuration.edge_subgraph(self.possible_configurations[1].edges)
        plt.figure(7)
        nx.draw_circular(H, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)

        I = self.online_configuration.subgraph(self.possible_configurations[2].nodes)
        plt.figure(8)
        nx.draw_circular(I, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)


        L = self.online_configuration.edge_subgraph(self.possible_configurations[3].edges)
        plt.figure(9)
        nx.draw_circular(L, font_size=8, node_size=40, alpha=0.5, node_color="blue", with_labels=True)


        print("I start computing")
        DiGM = isomorphism.GraphMatcher(G, self.possible_configurations[0])
        print("done with inizialization")
        is_good = DiGM.subgraph_is_isomorphic()
        print(is_good)

        print("I start computing")
        DiGM = isomorphism.GraphMatcher(H, self.possible_configurations[1])
        print("done with inizialization")
        is_good = DiGM.subgraph_is_isomorphic()
        print(is_good)


        print("I start computing")
        DiGM = isomorphism.GraphMatcher(I, self.possible_configurations[2])
        print("done with inizialization")
        is_good = DiGM.subgraph_is_isomorphic()
        print(is_good)

        print("I start computing")
        DiGM = isomorphism.GraphMatcher(L, self.possible_configurations[3])
        print("done with inizialization")
        is_good = DiGM.subgraph_is_isomorphic()
        print(is_good)

        plt.show()
