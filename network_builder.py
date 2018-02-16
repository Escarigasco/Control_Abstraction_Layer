import networkx as nx
from matplotlib import pyplot as plt
from Valve import Valve
from Pump import Pump
from Pipeline import Pipeline
from Sink import Sink
from Source import Source

import pandas as pd
import re


configuration_mat = pd.read_csv("static_config.csv")
list_nodes = list(configuration_mat.columns.values[1:])
components_map = {}

print(list_nodes)
Sw_Bd = nx.Graph()


for node in list_nodes:
    if (re.match('Valve', node)):
        components_map[node] = Valve(node)
        Sw_Bd.add_node(components_map[node])
    elif (re.match('Pump', node)):
        components_map[node] = Pump(node)
        Sw_Bd.add_node(components_map[node])
    elif (re.match('Pipeline', node)):
        components_map[node] = Pipeline(node)
        Sw_Bd.add_node(components_map[node])
    elif (re.match('Source', node)):
        components_map[node] = Source(node)
        Sw_Bd.add_node(components_map[node])
    elif (re.match('Sink', node)):
        components_map[node] = Sink(node)
        Sw_Bd.add_node(components_map[node])

print("Nodes of graph: ")
print(Sw_Bd.nodes())
print("Edges of graph: ")
print(Sw_Bd.edges())

nx.draw(Sw_Bd, with_labels=False)
plt.savefig("path_graph_cities.png")
plt.show()
