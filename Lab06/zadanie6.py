import copy


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

    def find_eulerian_cycle(self):
        graph_prim = self.graph.copy()

        start_vertex = g.startVertex
        current_v = start_vertex
        euler_cycle = [start_vertex]

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

                        if is_connected(hmm):
                            euler_cycle.append(edge)
                            edges.remove(edge)
                            graph_prim[edge].remove(current_v)
                            current_v = edge
                            break
            else:
                break

        if is_connected(graph_prim):
            if check_degrees(self.graph):
                print(f"Graf jest eulerowski!: {euler_cycle}")
            else:
                print(f"Graf jest poleulerowski: {euler_cycle}")
        else:
            print(f"Graf nie jest eulerowski")

        return euler_cycle


def check_degrees(graph):
    for vertices in graph.values():
        if len(vertices) % 2 != 0:
            return False
    return True


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


g = Graph()

file_path = "krawedzie.txt"

try:
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.split(",")
            u, v, w = int(data[0]), int(data[1]), int(data[2])
            g.add_edge(u, v, w)

    start_vertex = 1
    g.startVertex = start_vertex

    euler_cycle = g.find_eulerian_cycle()

except FileNotFoundError:
    print(f"Plik {file_path} nie został znaleziony")
