import copy
import heapq

import networkx as nx


class Edge:
    def __init__(self, u, v, weight):
        if u < v:
            self.u = u
            self.v = v
        else:
            self.u = v
            self.v = u
        self.weight = weight

    def __str__(self):
        return f"Edge({self.u}, {self.v}, {self.weight})"


class Graph:
    def __init__(self):
        self.edges = []
        self.visited_edges = []

    def add_edge(self, u, v, weight):
        self.edges.append(Edge(u, v, weight))

    def get_weight(self, u, v):
        for edge in self.edges:
            if (edge.u == u and edge.v == v) or (edge.u == v and edge.v == u):
                return edge.weight
        return float('inf')

    def check_triangle(self):
        for edge1 in self.edges:
            for edge2 in self.edges:
                if edge1 != edge2:
                    if edge1.u > edge2.u:
                        edge1, edge2 = edge2, edge1

                    if edge1.weight + edge2.weight < self.get_weight(edge1.u, edge2.v) or \
                            edge1.weight + self.get_weight(edge1.v, edge2.v) < edge2.weight or \
                            edge2.weight + self.get_weight(edge1.u, edge2.u) < edge1.weight:
                        return False
        return True

    def is_complete(self):
        if not self.edges:
            return True

        vertices = set()
        for edge in self.edges:
            vertices.add(edge.u)
            vertices.add(edge.v)

        n = len(vertices)

        complete_graph_edges = n * (n - 1) // 2
        return len(self.edges) == complete_graph_edges

    def get_adjacency_list(self):
        adj_list = {}
        for edge in self.edges:
            if edge.u not in adj_list:
                adj_list[edge.u] = []
            if edge.v not in adj_list:
                adj_list[edge.v] = []
            adj_list[edge.u].append((edge.v, edge.weight))
            adj_list[edge.v].append((edge.u, edge.weight))
        return adj_list

    def minimum_spanning_tree(self):
        adj_list = self.get_adjacency_list()
        min_tree = []

        start_vertex = list(adj_list.keys())[0]
        visited = set([start_vertex])
        edges_heap = []

        for neighbor, weight in adj_list[start_vertex]:
            heapq.heappush(edges_heap, (weight, start_vertex, neighbor))

        while edges_heap:
            weight, u, v = heapq.heappop(edges_heap)
            if v not in visited:
                visited.add(v)
                min_tree.append(Edge(u, v, weight))

                for neighbor, weight in adj_list[v]:
                    if neighbor not in visited:
                        heapq.heappush(edges_heap, (weight, v, neighbor))

        return min_tree

    def christofides_algorithm(self):
        if not self.check_triangle():
            print("Warunek trójkąta dla wag krawędzi nie jest spełniony!")
            return

        if not self.is_complete():
            print(f"Graf nie jest pełny!")
            return

        print("Graf jest pełny")

        T = self.minimum_spanning_tree()
        print(f"\nMinimalne drzewo spinające T: {[(edge.u, edge.v) for edge in T]}")

        G_networkx = nx.Graph()

        for edge in T:
            G_networkx.add_edge(edge.u, edge.v, weight=edge.weight)

        O = [node for node, degree in G_networkx.degree() if degree % 2 != 0]

        print("\nZbiór O wierzchołki o nieparzystym stopniu z T:", O)

        subgraph = nx.Graph()
        for edge in self.edges:
            subgraph.add_edge(edge.u, edge.v, weight=edge.weight)

        subgraph = subgraph.subgraph(O)
        print(f"Podgraf G z wierzchołkami O: {subgraph.edges()}")

        M = list(nx.algorithms.min_weight_matching(subgraph))

        print("Zbiór M minimalnego skojarzenia doskonałego:", M)

        H = nx.MultiGraph()

        for edge in T:
            H.add_edge(edge.u, edge.v, weight=edge.weight)

        for u, v in M:
            H.add_edge(u, v)

        print(f"\nPodgraf po połączeniu zbioru M i T: {H.edges()}")

        try:
            eulerian_cycle = []
            for edge in list(nx.eulerian_circuit(H)):
                eulerian_cycle.append(edge[0])
            eulerian_cycle.append(eulerian_cycle[0])
            print(f"\nCykl Eulera w grafie H: {eulerian_cycle}")

            visited = set()
            hamiltonian_cycle = []

            for node in eulerian_cycle:
                if node not in visited:
                    hamiltonian_cycle.append(node)
                    visited.add(node)

            if len(hamiltonian_cycle) == len(set(H.nodes)):
                hamiltonian_cycle.append(hamiltonian_cycle[0])
                print(f"\nCykl Hamiltona z cyklu Eulera: {hamiltonian_cycle}")
            else:
                print("\nNie udało się stworzyć cyklu Hamiltona")
        except nx.NetworkXError:
            print("\nNie można znaleźć cyklu Eulera")


G = Graph()

file_path = "krawedzie.txt"

try:
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.split(",")
            u, v, weight = int(data[0]), int(data[1]), int(data[2])
            G.add_edge(u, v, weight)
    G.christofides_algorithm()

except FileNotFoundError:
    print(f"Plik {file_path} nie został znaleziony")
