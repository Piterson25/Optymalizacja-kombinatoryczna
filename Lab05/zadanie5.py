import networkx as nx
import matplotlib.pyplot as plt
import math


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def print_solution(self, dist):
        print("Wierzchołek\t\tDystans od źródła")
        for i in range(self.V):
            print(f"{i}\t\t\t\t{dist[i]}")

    def bellman_ford(self):
        max_vertex = max(max(edge[:2]) for edge in self.graph)
        dist = [math.inf] * (max_vertex + 1)
        pred = [-1] * (max_vertex + 1)
        dist[0] = 0

        for _ in range(max_vertex):
            for u, v, w in self.graph:
                if dist[u] != math.inf:
                    new_dist = dist[u] + w
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        pred[v] = u

        for u, v, w in self.graph:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                print("Graf zawiera ujemny cykl")
                return

        path = [max_vertex]
        current = max_vertex
        while pred[current] != -1:
            path.append(pred[current])
            current = pred[current]
        path.reverse()

        print(f"Ścieżka po wierzchołkach: {path}")

        self.print_solution(dist)

    def create_networkx_graph(self):
        G = nx.DiGraph()
        for u, v, w in self.graph:
            G.add_edge(u, v, weight=w)
        return G


g = Graph(0)

file_path = input("Podaj nazwę pliku z krawędziami: ")

try:
    with open(file_path, "r") as file:
        lines = file.readlines()
        vertices = set()
        for line in lines:
            data = line.split(",")
            u, v, w = int(data[0]), int(data[1]), int(data[2])
            vertices.add(u)
            vertices.add(v)
            g.add_edge(u, v, w)
        g.V = len(vertices)

    G = g.create_networkx_graph()
    pos = nx.planar_layout(G)
    nx.draw(G, pos, with_labels=True, arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

    g.bellman_ford()


except FileNotFoundError:
    print(f"Plik {file_path} nie został znaleziony")
