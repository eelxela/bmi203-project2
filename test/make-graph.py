import matplotlib.pyplot as plt
from networkx.generators import random_graphs
import networkx as nx
import pathlib

folder = pathlib.Path(__file__).resolve().parent
graph = random_graphs.erdos_renyi_graph(8, p=0.2, seed=100, directed=True)
nx.write_adjlist(graph, folder / "erdosrenyi.adjlist")

# write graph picture
options = {"node_color": "white", "edgecolors": "black", "linewidths": 2}

# pos = nx.spring_layout(graph, k=0.01, iterations=1, scale=2)
nx.draw_networkx(graph, **options)
plt.savefig(folder / "erdosrenyi.png")
