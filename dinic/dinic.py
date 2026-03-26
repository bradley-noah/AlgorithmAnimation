import random
from collections import deque


class Edge:
    def __init__(self, to, cap, rev_idx):
        self.to      = to
        self.cap     = cap
        self.rev_idx = rev_idx


def build_graph(n, edge_list):
    pass


def dinic(graph, source, sink):
    events   = []
    max_flow = 0
    return events, max_flow


def make_random_graph(n=6, n_edges=9, max_cap=10):
    pass


if __name__ == "__main__":
    pass