import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.graph = nx.DiGraph() if directed else nx.Graph()

    def edge_exists(self, u, v):
        try:
            return self.graph.has_edge(u, v)
        except ValueError:
            print(f"Nie poprawne wierzchołki")
            return False

    def vertex_exists(self, v):
        try:
            return self.graph.has_node(v)
        except ValueError:
            print(f"Nie poprawny wierzchołek")
            return False

    def add_edge(self, u, v):
        try:
            u = int(u)
            v = int(v)
            if not self.vertex_exists(u) or not self.vertex_exists(v):
                print(f"Przynajmniej jeden wierzchołek nie istnieje")
                return
            self.graph.add_edge(u, v)
        except ValueError:
            print(f"Nie poprawne wierzchołki")
            return

    def remove_edge(self, u, v):
        try:
            u = int(u)
            v = int(v)
            if not self.edge_exists(u, v):
                print(f"Przynajmniej jeden wierzchołek nie istnieje")
                return
            self.graph.remove_edge(u, v)
        except ValueError:
            print(f"Nie poprawne wierzchołki")
            return

    def add_vertex(self, v):
        try:
            self.graph.add_node(int(v))
        except ValueError:
            print(f"Nie poprawny wierzchołek")
            return

    def remove_vertex(self, v):
        try:
            v = int(v)
            if not self.vertex_exists(v):
                print(f"Wierzchołek {v} nie istnieje")
                return
            self.graph.remove_node(v)
        except ValueError:
            print(f"Nie poprawny wierzchołek")
            return

    def vertex_degree(self, v):
        try:
            v = int(v)
            if not self.vertex_exists(v):
                print(f"Wierzchołek {v} nie istnieje")
                return None, None

            if self.directed:
                return self.graph.in_degree(v), self.graph.out_degree(v)
            else:
                return self.graph.degree(v), None
        except ValueError:
            print(f"Nie poprawny wierzchołek")
            return None, None

    def min_max_degree(self):
        if len(self.graph) == 0:
            print("Graf jest pusty")
            return None

        degrees = list(self.graph.degree())
        return min(degrees, key=lambda x: x[1]), max(degrees, key=lambda x: x[1])

    def count_even_odd_degrees(self):
        if len(self.graph) == 0:
            print("Graf jest pusty")
            return None

        degrees = [deg for _, deg in self.graph.degree()]
        even_count = sum(1 for deg in degrees if deg % 2 == 0)
        odd_count = sum(1 for deg in degrees if deg % 2 == 1)
        return even_count, odd_count

    def sorted_degrees(self):
        if len(self.graph) == 0:
            print("Graf jest pusty.")
            return None

        degrees = [deg for _, deg in self.graph.degree()]
        return sorted(degrees, key=lambda x: x, reverse=True)

    def draw_graph(self):
        pos = nx.spring_layout(self.graph)
        if self.directed:
            nx.draw(self.graph, pos, with_labels=True, arrows=True, arrowsize=20)
        else:
            nx.draw(self.graph, pos, with_labels=True, arrows=False)
        plt.show()

    def change_graph_type(self):
        self.directed = not self.directed

    def adjacency_matrix(self):
        num_nodes = len(self.graph.nodes())
        adj_matrix = np.zeros((num_nodes, num_nodes), dtype=int)

        for edge in self.graph.edges(data=True):
            i = edge[0]
            j = edge[1]

            if self.directed:
                adj_matrix[i][j] = 1
            else:
                adj_matrix[i][j] = 1
                adj_matrix[j][i] = 1

        return adj_matrix


graph = Graph(True)
file_name = "krawedzie.txt"
try:
    with open(file_name, 'r') as file:
        for line in file:
            current_line = line.strip().split(', ')
            i = int(current_line[0])
            j = int(current_line[1])
            graph.graph.add_edge(i, j)
except FileNotFoundError:
    print(f"Plik '{file_name}' nie istnieje. Tworzę nowy pusty graf.")

while True:
    print("1. Dodaj krawędź")
    print("2. Usuń krawędź")
    print("3. Dodaj wierzchołek")
    print("4. Usuń wierzchołek")
    print("5. Stopień wierzchołka")
    print("6. Stopień minimalny i maksymalny")
    print("7. Liczba wierzchołków stopnia parzystego i nieparzystego")
    print("8. Posortowane stopnie wierzchołków")
    print("9. Zmiana typu grafu (skierowany/nieskierowany)")
    print("10. Macierz sasiedztwa")
    print("Wyswietl - Przedstaw graficznie graf")
    print("Zakoncz - Wyjście z programu")
    choice = input("Wybierz opcję: ")

    if choice == '1':
        u = input("Podaj pierwszy wierzchołek: ")
        v = input("Podaj drugi wierzchołek: ")
        graph.add_edge(u, v)
    elif choice == '2':
        u = input("Podaj pierwszy wierzchołek: ")
        v = input("Podaj drugi wierzchołek: ")
        graph.remove_edge(u, v)
    elif choice == '3':
        v = input("Podaj wierzchołek: ")
        graph.add_vertex(v)
    elif choice == '4':
        v = input("Podaj wierzchołek: ")
        graph.remove_vertex(v)
    elif choice == '5':
        v = input("Podaj wierzchołek: ")
        in_degree, out_degree = graph.vertex_degree(v)
        if out_degree:
            print(f"Stopień wejściowy: {in_degree}, Stopień wyjściowy: {out_degree}")
        else:
            print(f"Stopień wierzchołka: {in_degree}")
    elif choice == '6':
        min_degree, max_degree = graph.min_max_degree()
        print(f"Stopień minimalny: {min_degree[1]}, Stopień maksymalny: {max_degree[1]}")
    elif choice == '7':
        even_count, odd_count = graph.count_even_odd_degrees()
        print(f"Liczba wierzchołków stopnia parzystego: {even_count}")
        print(f"Liczba wierzchołków stopnia nieparzystego: {odd_count}")
    elif choice == '8':
        sorted_degrees = graph.sorted_degrees()
        print(f"Posortowane stopnie wierzchołków: {sorted_degrees}")
    elif choice == '9':
        graph.change_graph_type()
        print("Typ grafu został zmieniony.")
    elif choice == '10':
        adjacency = graph.adjacency_matrix()
        print("Macierz sąsiedztwa:")
        for row in adjacency:
            print(row)
    elif choice.lower() == 'wyswietl':
        graph.draw_graph()
    elif choice.lower() == 'zakoncz':
        break
    else:
        print("Nieprawidłowa opcja, spróbuj ponownie")
