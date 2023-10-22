import networkx as nx
import matplotlib.pyplot as plt

file_path = 'krawedzie.txt'
G = nx.Graph()
try:
    with open(file_path, 'r') as file:
        for line in file:
            current_line = line.strip().split(', ')
            i = int(current_line[0])
            j = int(current_line[1])
            G.add_edge(i, j)
except FileNotFoundError:
    print(f"Plik '{file_path}' nie istnieje.")


def dfs_tree(graph, start_node):
    visited = set()
    stack = [(start_node, None)]
    dfs_tree = nx.Graph()
    while stack:
        node, parent = stack.pop()
        if node not in visited:
            visited.add(node)
            if parent is not None:
                dfs_tree.add_edge(parent, node)
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    stack.append((neighbor, node))
    return dfs_tree


start_node = list(G.nodes())[0]
dfs_tree_result = dfs_tree(G, start_node)

print(f"Drzewo spinające DFS: {list(dfs_tree_result.edges())}")

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
nx.draw(dfs_tree_result, pos, edge_color='r', with_labels=True)
plt.show()
