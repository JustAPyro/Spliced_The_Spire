import random
import networkx as nx
from matplotlib import pyplot as plt
from networkx import DiGraph

G = nx.grid_2d_graph(7, 15)
G.clear_edges()
D = DiGraph(G)


def get_uncrossed_successors(node, potential_successors):
    uncrossed = []
    for potential in potential_successors:
        if potential[0] == node[0]:
            uncrossed.append(potential)
        if potential[0] == node[0] - 1:
            if (node[0], node[1] + 1) not in D.successors((node[0] - 1, node[1])):
                uncrossed.append(potential)
        if potential[0] == node[0] + 1:
            if (node[0], node[1] + 1) not in D.successors((node[0] + 1, node[1])):
                uncrossed.append(potential)

    return uncrossed


def get_possible_successors(node):
    floor = node[1] + 1
    if floor > 14:
        raise RuntimeError("Tried to find successors for room on top floor")
    if node[0] == 0:
        return get_uncrossed_successors(node, [(0, floor), (1, floor)])
    if node[0] == 6:
        return get_uncrossed_successors(node, [(5, floor), (6, floor)])
    return get_uncrossed_successors(node,
            [(node[0] - 1, floor), (node[0], floor), (node[0] + 1, floor)])


def generate_random_path(node):
    if node[1] < 14:
        choice = random.choice(get_possible_successors(node))
        D.add_edge(node, choice)
        generate_random_path(choice)


start = random.randint(0, 6)
second_start = start
while second_start == start:
    second_start = random.randint(0, 6)
generate_random_path((start, 0))
generate_random_path((second_start, 0))
for _ in range(4):
    start = random.randint(0, 6)
    generate_random_path((start, 0))

# Casted to a list to get around a weird error (per guy on stackexchange)
D.remove_nodes_from(list(nx.isolates(D)))

for node in D.nodes:
    if node[1] == 0:
        D.nodes[node]["room"] = "Monster"
    if node[1] == 8:
        D.nodes[node]["room"] = "Treasure"
print(D.nodes(data=True))

plt.figure(figsize=(6, 6))
pos = {(x, y): (x, y) for x, y in D.nodes()}
labels = nx.get_node_attributes(D, 'room')
nx.draw(D, pos=pos,
        node_color='lightgreen',
        with_labels=True,
        node_size=600,
        labels=labels)
plt.show()
