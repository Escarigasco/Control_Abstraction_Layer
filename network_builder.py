import networkx as nx
from matplotlib import pyplot as plt
from valve import valve
from pump import pump
from pipeline import pipeline
from sink import sink
from source import source
import pandas as pd
import re


configuration_mat = pd.read_csv("static_config.csv")
configuration_mat.set_index("Object",inplace=True)
print(configuration_mat["Valve_52H"]["Valve_52H"])
#print(configuration_mat["Object"])
print(configuration_mat)
list_nodes = list(configuration_mat.columns.values[1:])  # 1: to avoid label 0
#print(list_nodes)
components_map = {}

print(list_nodes)
Sw_Bd = nx.Graph()

for node in list_nodes:
    if (re.match('Valve', node)):    # regular expression
        components_map[node] = valve(node)  # this is a redundancy as graph
        Sw_Bd.add_node(components_map[node])  # can be indexed as dictionary
    elif (re.match('Pump', node)):
        components_map[node] = pump(node)
        Sw_Bd.add_node(components_map[node], time='2pm')
    elif (re.match('Pipeline', node)):
        components_map[node] = pipeline(node)
        Sw_Bd.add_node(components_map[node])
    elif (re.match('Source', node)):
        components_map[node] = source(node)
        Sw_Bd.add_node(components_map[node])
    elif (re.match('Sink', node)):
        components_map[node] = sink(node)
        Sw_Bd.add_node(components_map[node])
    #print(Sw_Bd[components_map[node]])  # print node attribute

print(Sw_Bd.nodes.data())  # print node name and attributes

print("Nodes of graph: ")
print(Sw_Bd.nodes())
print("Edges of graph: ")
print(Sw_Bd.edges())

nx.draw(Sw_Bd, with_labels=False)
plt.savefig("path_graph_cities.png")
plt.show()
