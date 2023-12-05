import copy
from random import randint
import networkx as nx


class Graph:
    def __init__(self):
        self.graph = {}
        self.weights = {}
        self.visited_edges = {}

    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []

        self.graph[u].append(v)
        self.graph[v].append(u)
        self.weights[(u, v)] = weight
        self.weights[(v, u)] = weight

    def find_shortest_path(self, start_vertex, end_vertex):
        visited = set()
        path = []
        min_path = []

        def dfs_shortest_path(current_vertex, target_vertex):
            visited.add(current_vertex)
            path.append(current_vertex)

            if current_vertex == target_vertex:
                if not min_path or sum(self.weights[(path[i], path[i + 1])] for i in range(len(path) - 1)) < sum(
                        self.weights[(min_path[i], min_path[i + 1])] for i in range(len(min_path) - 1)):
                    min_path[:] = path[:]
                path.pop()
                visited.remove(current_vertex)
                return

            for neighbor in self.graph[current_vertex]:
                if neighbor not in visited:
                    dfs_shortest_path(neighbor, target_vertex)

            path.pop()
            visited.remove(current_vertex)

        dfs_shortest_path(start_vertex, end_vertex)
        return min_path[::-1]

    def chinese_postman(self):
        if is_connected(self.graph):
            if count_odd_degrees(self.graph) == 0:
                print(f"Graf jest eulerowski!")
                self.find_eulerian_cycle()
            elif count_odd_degrees(self.graph) == 2:
                print(f"Graf jest półeulerowski")
                self.find_eulerian_path()
            else:
                print(f"Graf nie jest eulerowski")
                self.not_eulerian()
                self.find_eulerian_cycle()
        else:
            print(f"Graf nie jest spójny!")

    def find_eulerian_cycle(self):
        graph_prim = copy.deepcopy(self.graph)

        current_v = randint(0, len(graph_prim) - 1)
        euler_cycle = [current_v]

        while len(graph_prim) > 0:
            if current_v in graph_prim:
                if len(graph_prim[current_v]) == 0:
                    break
                elif len(graph_prim[current_v]) == 1:
                    next_vec = graph_prim[current_v][0]
                    euler_cycle.append(next_vec)

                    del graph_prim[current_v]
                    graph_prim[next_vec].remove(current_v)
                    current_v = next_vec
                else:
                    edges = graph_prim[current_v]
                    for edge in edges:
                        hmm = copy.deepcopy(graph_prim)
                        hmm[current_v].remove(edge)
                        hmm[edge].remove(current_v)

                        if is_connected(hmm):
                            euler_cycle.append(edge)
                            edges.remove(edge)
                            graph_prim[edge].remove(current_v)
                            current_v = edge
                            break
                    if not edges:
                        del graph_prim[current_v]
            else:
                break

        print(f"Cykl Eulera: {euler_cycle}")

    def find_eulerian_path(self):
        graph_prim = copy.deepcopy(self.graph)
        weights = copy.deepcopy(self.weights)
        odd_degree_vertices = [vertex for vertex, neighbors in graph_prim.items() if len(neighbors) % 2 != 0]

        start_vertex, end_vertex = odd_degree_vertices
        euler_path = []
        current_v = start_vertex

        while len(graph_prim) > 0:
            if current_v in graph_prim:
                if len(graph_prim[current_v]) == 0:
                    break
                elif len(graph_prim[current_v]) == 1:
                    next_vec = graph_prim[current_v][0]
                    euler_path.append(next_vec)

                    del graph_prim[current_v]
                    graph_prim[next_vec].remove(current_v)
                    current_v = next_vec
                else:
                    edges = graph_prim[current_v]
                    for edge in edges:
                        hmm = copy.deepcopy(graph_prim)
                        hmm[current_v].remove(edge)
                        hmm[edge].remove(current_v)

                        if is_connected(hmm):
                            euler_path.append(edge)
                            edges.remove(edge)
                            del weights[(current_v, edge)]
                            del weights[(edge, current_v)]
                            graph_prim[edge].remove(current_v)
                            current_v = edge
                            break
                    if not edges:
                        del graph_prim[current_v]
            else:
                break

        euler_path.insert(0, start_vertex)
        shortest_path = self.find_shortest_path(start_vertex, end_vertex)
        print(f"Droga Eulera: {euler_path}")
        print(f"Najkrótsza ścieżka: {shortest_path}")
        print(f"Trasa listonosza: {euler_path + shortest_path[1:]}")

    def not_eulerian(self):
        graph_prim = copy.deepcopy(self.graph)
        weights = copy.deepcopy(self.weights)
        W = [vertex for vertex, neighbors in graph_prim.items() if len(neighbors) % 2 != 0]

        shortest_paths = {}

        G_prim = Graph()

        for i in range(len(W)):
            for j in range(i + 1, len(W)):
                start_vertex, end_vertex = W[i], W[j]
                shortest_path = self.find_shortest_path(start_vertex, end_vertex)
                shortest_path_length = sum(
                    self.weights[(shortest_path[i], shortest_path[i + 1])] for i in range(len(shortest_path) - 1))
                G_prim.add_edge(start_vertex, end_vertex, shortest_path_length)
                shortest_paths[(start_vertex, end_vertex)] = shortest_path
                print(
                    f"Najkrótsza ścieżka między {start_vertex} a {end_vertex}: {shortest_path} {shortest_path_length}")

        nxGraph = nx.Graph()
        for u, v in G_prim.weights:
            nxGraph.add_edge(u, v, weight=G_prim.weights[(u, v)])

        G = list(nx.algorithms.min_weight_matching(nxGraph))
        min_weight_matching_weights = {}
        for v in G:
            v = tuple(sorted(v))
            min_weight_matching_weights[v] = shortest_paths[v]
        print(f"Minimalne skojrzenie dokladne: {min_weight_matching_weights}")

        for e in min_weight_matching_weights:
            vertices = min_weight_matching_weights[e][::-1]
            for i in range(len(vertices)):
                if i + 1 < len(vertices):
                    if len(vertices) == 2:
                        self.add_edge(vertices[i], vertices[i + 1], weights[tuple(vertices)])
                    else:
                        self.add_edge(vertices[i], vertices[i + 1], weights[tuple([vertices[i], vertices[i + 1]])])


def count_odd_degrees(graph):
    odd_degrees = 0
    for vertices in graph.values():
        if len(vertices) % 2 != 0:
            odd_degrees += 1
    return odd_degrees


def is_connected(graph):
    if not graph:
        return True

    visited = set()

    def dfs(start):
        visited.add(start)
        for neighbor in graph.get(start, []):
            if neighbor not in visited:
                dfs(neighbor)

    dfs(next(iter(graph)))
    return len(visited) == len(graph)


G = Graph()

file_path = input("Podaj nazwę pliku z krawędziami: ")

try:
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.split(",")
            u, v, w = int(data[0]), int(data[1]), int(data[2])
            G.add_edge(u, v, w)
    G.chinese_postman()

except FileNotFoundError:
    print(f"Plik {file_path} nie został znaleziony")
