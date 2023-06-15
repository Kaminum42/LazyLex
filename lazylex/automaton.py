from graph import Graph, Node, Edge
from queue import Queue


class Automaton(Graph):
    def __init__(self) -> None:
        super().__init__()
        self.starts: list[Node] = []
        self.ends: list[Node] = []
        self.alphabet: list[str] = []
        self.transfer_alphabet: dict[str: list[str]] = {}

    def __str__(self) -> str:
        ns = self.nodes()
        idx = {ns[i]: i for i in range(len(ns))}
        start_ls = [f"{idx[n]}" for n in self.starts]
        start_str = "\n".join(start_ls)
        end_ls = [f"{idx[n]}" for n in self.ends]
        end_str = "\n".join(end_ls)
        return super().__str__() + f"\nStarts:\n{start_str}\nEnds:\n{end_str}"

    def set_start(self, node: Node) -> None:
        if node not in self.table:
            self.add_node(node)
        if node not in self.starts:
            self.starts.append(node)

    def set_end(self, node: Node) -> None:
        if node not in self.table:
            self.add_node(node)
        if node not in self.ends:
            self.ends.append(node)

    def add_transfer_word(self, word: str, transferred: list[str]):
        self.transfer_alphabet[word] = transferred

    def match_char(self, edge: Edge, ch: str) -> bool:
        if ch == edge.info:
            return True
        if edge.info not in self.transfer_alphabet:
            return False
        return ch in self.transfer_alphabet[edge.info]

    def dfa_match(self, expr: str) -> None:
        node = self.starts[0]
        for ch in expr:
            found = False
            for e in self.edges(node):
                if self.match_char(e, ch):
                    node = e.n2
                    found = True
                    break
            if not found:
                raise ValueError(f"{repr(expr)} 匹配失败。")
        if node not in self.ends:
            raise ValueError(f"{repr(expr)} 匹配失败。")

    def dfa_match_prefix(self, expr: str) -> str:
        node = self.starts[0]
        s = ""
        for ch in expr:
            found = False
            for e in self.edges(node):
                if self.match_char(e, ch):
                    node = e.n2
                    found = True
                    s += ch
                    break
            if not found:
                break
        if node not in self.ends:
            raise ValueError(f"{repr(expr)} 匹配失败。")
        return s

    def epsilon_enclosure(self, s: set[Node]) -> set[Node]:
        vis: set[Node] = s.copy()
        q: Queue = Queue()
        for n in vis:
            q.put(n)
        while not q.empty():
            n = q.get()
            for e in self.edges(n):
                if e.info == "ε" and e.n2 not in vis:
                    q.put(e.n2)
                    vis.add(e.n2)
        return vis

    def transfer_set(self, s: set[Node], ch: str) -> set[Node]:
        j: set[Node] = set()
        for n in s:
            for e in self.edges(n):
                if e.info == ch:
                    j.add(e.n2)
        return self.epsilon_enclosure(j)
