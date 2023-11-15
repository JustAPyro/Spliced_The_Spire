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

nums = [x for x in range(0, 6)]
start = random.choice(nums)
nums.remove(start)
second_start = random.choice(nums)

generate_random_path((start, 0))
generate_random_path((second_start, 0))
for _ in range(4):
    start = random.randint(0, 6)
    generate_random_path((start, 0))

# Casted to a list to get around a weird error (per guy on stackexchange)
D.remove_nodes_from(list(nx.isolates(D)))

unfilled_nodes = []
for node in D.nodes:
    if node[1] == 0:
        D.nodes[node]["room"] = "Monster"
    elif node[1] == 8:
        D.nodes[node]["room"] = "Treasure"
    elif node[1] == 14:
        D.nodes[node]["room"] = "Rest"
    else:
        unfilled_nodes.append(node)

room_bucket = []
for _ in range(len(unfilled_nodes)):
    x = random.randint(1, 100)
    if x <= 45:  # 45% chance
        room_bucket.append("Monster")
    elif x <= 67:  # 22% chance
        room_bucket.append("Event")
    elif x <= 83:  # 16% chance
        room_bucket.append("Elite")
    elif x <= 95:  # 12% chance
        room_bucket.append("Rest")
    else:  # 5% chance
        room_bucket.append("Shop")

random.shuffle(room_bucket)


def rule1(node, room_type):
    return not (node[1] < 5 and (room_type == "Elite" or room_type == "Rest"))


def rule2(node, room_type):
    if room_type == "Elite":
        for successor in D.successors(node):
            if D.nodes[successor].get("room") == "Elite":
                return False
        for predecessor in D.predecessors(node):
            if D.nodes[predecessor].get("room") == "Elite":
                return False

    if room_type == "Shop":
        for successor in D.successors(node):
            if D.nodes[successor].get("room") == "Shop":
                return False
        for predecessor in D.predecessors(node):
            if D.nodes[predecessor].get("room") == "Shop":
                return False

    if room_type == "Rest":
        for successor in D.successors(node):
            if D.nodes[successor].get("room") == "Rest":
                return False
        for predecessor in D.predecessors(node):
            if D.nodes[predecessor].get("room") == "Rest":
                return False
    return True


def rule3(node, room_type):
    for predecessor in D.predecessors(node):
        for successor in D.successors(predecessor):
            if D.nodes[successor].get("room") == room_type:
                return False
    return True


def rule4(node, room_type):
    return not (node[1] == 13 and room_type == "Rest")


for node in list(unfilled_nodes):
    i = 0
    while i < len(room_bucket):
        if (rule1(node, room_bucket[i]) and rule2(node, room_bucket[i])
                and rule3(node, room_bucket[i]) and rule4(node, room_bucket[i])):
            D.nodes[node]["room"] = room_bucket.pop(i)
            unfilled_nodes.remove(node)
            break
        else:
            i += 1

print(unfilled_nodes)

# This might be needed if something is left unfilled at the end because nothing is left
# in room_bucket that follows the rules
if len(unfilled_nodes) > 0:
    # iterate through unfilled_nodes and fill with whatever passes the rules
    pass

plt.figure(figsize=(6, 6))
pos = {(x, y): (x, y) for x, y in D.nodes()}
labels = nx.get_node_attributes(D, 'room')
nx.draw(D, pos=pos,
        node_color='lightgreen',
        with_labels=True,
        node_size=600,
        labels=labels)
plt.show()
