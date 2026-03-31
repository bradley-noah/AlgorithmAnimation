import random
from collections import deque


class Edge:
    def __init__(self, to, cap, rev_idx):
        self.to      = to
        self.cap     = cap
        self.rev_idx = rev_idx


def build_graph(n, edge_list):
    graph = [[] for _ in range(n)]
    for frm, to, cap in edge_list:
        fwd = Edge(to, cap, len(graph[to]))
        rev = Edge(frm, 0, len(graph[frm]))
        graph[frm].append(fwd)
        graph[to].append(rev)
    return graph


def dinic(graph, source, sink):
    events   = []
    max_flow = 0
    n        = len(graph)

    def bfs():
        level = [-1] * n
        queue = deque([source])
        level[source] = 0
        while queue:
            v = queue.popleft()
            for edge in graph[v]:
                if edge.cap > 0 and level[edge.to] < 0:
                    level[edge.to] = level[v] + 1
                    queue.append(edge.to)
        return level

    def dfs(v, upTo, iter_, flow):
        if v == sink:
            return flow
        for i in range(iter_[v], len(graph[v])):
            edge = graph[v][i]
            if edge.cap > 0 and level[v] + 1 == level[edge.to]:
                d = dfs(edge.to, sink, iter_, min(flow, edge.cap))
                if d > 0:
                    edge.cap -= d
                    graph[edge.to][edge.rev_idx].cap += d
                    events.append(('flow', v, edge.to, d))
                    return d
            iter_[v] += 1
        return 0

    while True:
        level = bfs()
        events.append(('level', level[:]))
        if level[sink] < 0:
            break

        iter_ = [0] * n
        while True:
            f = dfs(source, sink, iter_, float('inf'))
            if f == 0:
                break
            max_flow += f
            events.append(('path', max_flow))

    events.append(('done', max_flow))
    return events, max_flow


def make_random_graph(n=6, n_edges=9, max_cap=10):
    edges = []
    possible = [(i, j) for i in range(n) for j in range(n) if i != j]
    if len(possible) > n_edges:
        edges_idx = random.sample(range(len(possible)), n_edges)
    else:
        edges_idx = range(len(possible))
    for idx in edges_idx:
        frm, to = possible[idx]
        cap = random.randint(1, max_cap)
        edges.append((frm, to, cap))
    return edges


if __name__ == "__main__":
    g = build_graph(6, [(0, 1, 10), (0, 2, 10), (1, 3, 4), (1, 4, 8), (2, 4, 9), (3, 5, 10), (4, 3, 6), (4, 5, 10)])
    events, flow = dinic(g, 0, 5)
    print(f"Max flow: {flow}")
    for e in events:
        print(e)
