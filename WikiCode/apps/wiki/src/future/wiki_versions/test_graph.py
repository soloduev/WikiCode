# В таком виде содержиться граф и его связи

graph = {
    1: [2],
    2: [3, 1],
    3: [11, 4, 2],
    4: [5,6,7, 3],
    5: [9, 4],
    6: [8, 4],
    7: [8, 13, 4],
    8: [10, 6, 7],
    9: [10, 5],
    10: [11, 9, 8],
    11: [12, 3, 10],
    12: [11],
    13: [7],
}

# В таком виде содержится информация о версии
vers = {
    1: {
        "id_user": 453,
        "commit_msg": 'Some message...',
        "comments": [],
        "diff": [],
        "date": 'some date...',
        "type": 'head(H), root(R), leaf(L), merge(M)',
        "seq": 'if this is head'
    },
    2: {
        # ...
    },
    # etc..
}

# Основные методы для графа:

# Нахождение наикротчайшего пути
def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not start in graph:
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


# Вывод всего графа для отладки
def print_graph(graph):
    for key, values in graph.items():
        for v in values:
            print(str(key) + " -> " + str(v))


# Добавление новой версии в граф
def append_version(graph, prev, new):
    graph[prev].append(new)
    graph[new] = [prev]


# Проверяет, является ли версия листом
def is_leaf(graph, version):
    links = graph[version]
    if len(graph) == 1:
        return True
    elif version != 1 and len(links) == 1:
        return True
    else:
        return False


# Слияние версий
def merge_versions(graph, versions, new):
    # Сначала проверяем все версии, являются ли они листами
    is_leafs = True
    for version in versions:
        if not is_leaf(graph, version):
            is_leafs = False
            break
    if is_leafs:
        graph[new] = []
        for version in versions:
            graph[version].append(new)
            graph[new].append(version)
        return True
    else:
        return False


append_version(graph, 13, 14)
append_version(graph, 14, 15)
print(is_leaf(graph, 14))
print(merge_versions(graph, [12, 15], 16))


print_graph(graph)
path = find_shortest_path(graph, 1, 14)
print(path)