import copy
from random import randint


class Graph:
    def __init__(self):
        self.graph = {}
        self.visited_edges = {}

    def add_edge(self, u, v, weight):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []

        self.graph[u].append(v)
        self.graph[v].append(u)

    def chinese_postman(self):
        if is_connected(self.graph):
            if count_odd_degrees(self.graph) == 0:
                print(f"Graf jest eulerowski!")
                self.find_eulerian_cycle()
            elif count_odd_degrees(self.graph) == 2:
                print(f"Graf jest poleulerowski")
            else:
                print(f"Graf nie jest eulerowski")
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

file_path = "krawedzie3.txt"

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
