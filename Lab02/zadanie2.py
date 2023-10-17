import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def naive_cycle_c3_check(G):
    cycles = set()
    for node in G.nodes():
        neighbors = list(G.neighbors(node))
        if len(neighbors) >= 2:
            for neighbor1 in neighbors:
                for neighbor2 in neighbors:
                    if neighbor1 != neighbor2 and G.has_edge(neighbor1, neighbor2):
                        cycle = tuple(sorted([node, neighbor1, neighbor2]))
                        cycles.add(cycle)
    return [list(cycle) for cycle in cycles]


def adjacency_matrix(G):
    num_nodes = len(G.nodes())
    adj_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

    for edge in G.edges(data=True):
        i = edge[0]
        j = edge[1]

        adj_matrix[i][j] = 1
        adj_matrix[j][i] = 1

    return adj_matrix


def matrix_mult_cycle_c3_check(G):
    cycles = set()
    matrix = adjacency_matrix(G)
    c3 = np.dot(matrix, np.dot(matrix, matrix))
    for i in range(G.number_of_nodes()):
        if c3[i, i] > 0:
            neighbors = list(G.neighbors(i))
            for neighbor1 in neighbors:
                for neighbor2 in neighbors:
                    if neighbor1 != neighbor2 and G.has_edge(neighbor1, neighbor2):
                        cycle = tuple(sorted([i, neighbor1, neighbor2]))
                        cycles.add(cycle)
    return [list(cycle) for cycle in cycles]


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
nx.draw(G, nx.spring_layout(G), with_labels=True)
plt.show()

print("Wersja naiwna:")
cycle_c3 = naive_cycle_c3_check(G)
if cycle_c3:
    print(f"Znalezione unikalne cykle C3: {cycle_c3}")
else:
    print("Brak cykli C3.")

print("Wersja w oparciu o mnożenie macierzy:")
cycle_c3 = matrix_mult_cycle_c3_check(G)
if cycle_c3:
    print(f"Znalezione unikalne cykle C3: {cycle_c3}")
else:
    print("Brak cykli C3.")
