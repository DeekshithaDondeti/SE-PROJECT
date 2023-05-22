import itertools

def tsp(path, graph, visited, cost, min_cost, min_path):

    if len(path) == len(graph):
        if cost < min_cost:
            min_cost = cost
            min_path = path
        return min_path, min_cost

    for node in range(len(graph)):
        if not visited[node]:
            visited[node] = True
            new_path = path + [node]
            new_cost = cost + graph[path[-1]][node]
            min_path, min_cost = tsp(new_path, graph, visited, new_cost, min_cost, min_path)
            visited[node] = False

    return min_path, min_cost

def traveling_salesman(graph, source):

    min_cost = float("inf")
    min_path = None
    visited = [False] * len(graph)

    visited[source] = True
    path, cost = tsp([source], graph, visited, 0, min_cost, min_path)
    visited[source] = False

    return path


graph = [[0, 8694.2, 7617.2, 7391.9], [8645.6, 0, 1351.7, 3018.1], [7808.8, 1397.6, 0, 2164], [7228.5, 3158.6, 2081.6, 0]]
print(traveling_salesman(graph,2))