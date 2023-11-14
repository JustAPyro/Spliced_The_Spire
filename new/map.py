import random
import networkx as nx
from matplotlib import pyplot as plt

G = nx.grid_2d_graph(7, 15)
G.clear_edges()


def get_possible_successors(node):
    floor = node[1] + 1
    if floor > 14:
        raise RuntimeError("Tried to find successors for room on top floor")
    if node[0] == 0:
        return [(0, floor), (1, floor)]
    if node[0] == 6:
        return [(5, floor), (6, floor)]
    return [(node[0] - 1, floor), (node[0], floor), (node[0] + 1, floor)]


def generate_random_path(node):
    if node[1] < 14:
        choice = random.choice(get_possible_successors(node))
        G.add_edge(node, choice)
        generate_random_path(choice)


start = random.randint(0, 6)
generate_random_path((start, 0))

plt.figure(figsize=(6, 6))
pos = {(x, y): (x, y) for x, y in G.nodes()}
nx.draw(G, pos=pos,
        node_color='lightgreen',
        with_labels=True,
        node_size=600)
plt.show()
