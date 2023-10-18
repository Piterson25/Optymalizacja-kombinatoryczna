import numpy as np
import matplotlib.pyplot as plt
import networkx as nx


def naive_cycle_c3_check(adj_matrix):
    cycles = set()
    num_nodes = len(adj_matrix)
    for i in range(num_nodes):
        for j in range(num_nodes):
            if adj_matrix[i, j] == 1:
                for k in range(num_nodes):
                    if adj_matrix[j, k] == 1 and adj_matrix[i, k] == 1 and i != j and j != k and i != k:
                        cycle = tuple(sorted([i, j, k]))
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


def matrix_mult_cycle_c3_check(adj_matrix):
    cycles = set()
    num_nodes = len(adj_matrix)
    c3 = np.dot(adj_matrix, adj_matrix)
    for i in range(num_nodes):
        for j in range(num_nodes):
            if adj_matrix[i, j] > 0 and c3[i, j] > 0:
                for k in range(num_nodes):
                    if adj_matrix[j, k] == 1 and adj_matrix[i, k] == 1 and i != j and j != k and i != k:
                        cycle = tuple(sorted([i, j, k]))
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

adj_matrix = adjacency_matrix(G)
nx.draw(G, nx.spring_layout(G), with_labels=True)
plt.show()

print("Wersja naiwna:")
cycle_c3 = naive_cycle_c3_check(adj_matrix)
if cycle_c3:
    print(f"Znalezione unikalne cykle C3: {cycle_c3}")
else:
    print("Brak cykli C3.")

print("Wersja w oparciu o mnożenie macierzy:")
cycle_c3 = matrix_mult_cycle_c3_check(adj_matrix)
if cycle_c3:
    print(f"Znalezione unikalne cykle C3: {cycle_c3}")
else:
    print("Brak cykli C3.")
