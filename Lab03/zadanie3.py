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


def dfs(graph, start_node):
    visited = set()
    tab = []

    def dfs_recursive(node, parent):
        visited.add(node)

        if parent is not None:
            tab.append([parent, node])
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                dfs_recursive(neighbor, node)

    dfs_recursive(start_node, None)

    if len(tab) == graph.number_of_edges():
        print("Graf jest spójny! :)")
    else:
        print("Graf nie jest spójny! :(")

    return tab


start_node = int(input("Podaj początkowy wierzchołek: "))
dfs_array = dfs(G, start_node)

print(f"Drzewo spinające DFS: {dfs_array}")

dfs_tree = nx.Graph()
for pair in dfs_array:
    dfs_tree.add_edge(pair[0], pair[1])

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True)
nx.draw(dfs_tree, pos, edge_color='r', with_labels=True)
plt.show()
