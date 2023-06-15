import itertools


class Node:
    def __init__(self, info=None):
        self.info = info

    def __str__(self):
        return str(self.info)


class Edge:
    def __init__(self, n1: Node, n2: Node, info=None):
        self.n1: Node = n1
        self.n2: Node = n2
        self.info = info

    def __str__(self):
        return f"{str(self.n1)} --{str(self.info)}-> {str(self.n2)}"


class Graph:
    def __init__(self):
        self.table: dict[Node: list[Edge]] = {}

    def __str__(self):
        ns = list(self.nodes())
        n_ls = [f"{i}: {ns[i]}" for i in range(len(self.table))]
        n_str = "\n".join(n_ls)
        es = self.edges()
        e_ls = [str(e) for e in es]
        e_str = "\n".join(e_ls)
        return "Nodes:\n" + n_str + "\nEdges:\n" + e_str

    def add_node(self, node: Node) -> None:
        if node not in self.table:
            self.table[node] = []

    def del_node(self, node: Node) -> None:
        if node in self.table:
            self.table.pop(node)

    def add_edge(self, edge: Edge) -> None:
        self.add_node(edge.n1)
        self.add_node(edge.n2)
        self.table[edge.n1].append(edge)

    def del_edge(self, edge: Edge) -> None:
        if edge in self.table[edge.n1]:
            self.table[edge.n1].remove(edge)

    def nodes(self) -> list[Node]:
        return list(self.table.keys())

    def edges(self, node: Node = None) -> list[Edge]:
        if node is None:
            return list(itertools.chain(*self.table.values()))
        return self.table[node]
