import networkx as nx
from matplotlib import pyplot as plt


G = nx.grid_2d_graph(7, 15)


G.clear_edges()

# G.add_edge((0, 0), (1, 1))
# G.add_edge((1, 1), (1, 2))
# G.add_edge((1, 2), (1, 3))
# G.add_edge((1, 3), (2, 4))
# G.add_edge((2, 4), (1, 5))
# G.add_edge((1, 5), (2, 6))
# G.add_edge((2, 6), (3, 7))
# G.add_edge((3, 7), (3, 8))
# G.add_edge((3, 8), (2, 9))
# G.add_edge((2, 9), (3, 10))
# G.add_edge((3, 10), (4, 11))
# G.add_edge((4, 11), (4, 12))
# G.add_edge((4, 12), (3, 13))
# G.add_edge((3, 13), (4, 14))



print(G.edges)

plt.figure(figsize=(6, 6))
pos = {(x, y): (x, y) for x, y in G.nodes()}
nx.draw(G, pos=pos,
        node_color='lightgreen',
        with_labels=True,
        node_size=600)
plt.show()
