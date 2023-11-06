def find_minimum_spanning_tree(n, edges):
    mst = set()

    startVertex = 0
    mst.add(startVertex)

    total_weight = 0

    if not is_connected(n, edges, startVertex):
        return "graf niespójny - brak drzewa spinającego"

    while len(mst) < n:
        minEdge, minWeight = findMinEdge(edges, mst)

        if minEdge is not None:
            total_weight += minWeight
            mst.add(minEdge)

    return total_weight


def is_connected(n, edges, startVertex):
    visited = [False] * n
    stack = [startVertex]

    while stack:
        current_vertex = stack.pop()
        visited[current_vertex] = True

        for u, v, _ in edges:
            if u == current_vertex and not visited[v]:
                stack.append(v)
            if v == current_vertex and not visited[u]:
                stack.append(u)

    return all(visited)


def findMinEdge(edges, mst):
    minEdge = None
    minWeight = float('inf')

    for edge in edges:
        u, v, w = edge[0], edge[1], edge[2]
        if ((u in mst and v not in mst) or (v in mst and u not in mst)) and w < minWeight:
            minEdge = v if u in mst else u
            minWeight = w

    return minEdge, minWeight


test_cases = int(input())
results = []

for _ in range(test_cases):
    nm_line = input().split(',')
    n = int(nm_line[0].split('=')[1])
    m = int(nm_line[1].split('=')[1])

    edges = []
    edge_str = input().split(' ')
    for i in edge_str:
        e_str = i.strip('{').split(',')
        u = int(e_str[0])
        v = int(e_str[1].split(',')[0].split('}')[0])
        w = int(e_str[1].split(',')[0].split('}')[1])

        edges.append((u, v, w))

    results.append(find_minimum_spanning_tree(n, edges))

for result in results:
    print(result)
