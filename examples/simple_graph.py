import networkx as nx
from aspartition import partition_graph

G = nx.Graph()
G.add_edge(1, 2, weight=6)
G.add_edge(1, 3, weight=2)
G.add_edge(3, 4, weight=1)
G.add_edge(3, 5, weight=7)
G.add_edge(3, 6, weight=9)
G.add_edge(1, 4, weight=3)

print(partition_graph(G, 3))