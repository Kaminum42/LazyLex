import traceback

import reg_to_words
import words_to_ast
import ast_to_nfa
import nfa_to_dfa
from graph import Node, Edge
from automaton import Automaton


class Analyser:
    def __init__(self):
        self.auto: Automaton = Automaton()
        self.sets: list[set[Node]] = []

    def init(self, auto: Automaton) -> None:
        self.auto: Automaton = auto
        self.sets: list[set[Node]] = []
        ends = set(auto.ends)
        non_ends: set[Node] = set(auto.nodes()) - ends
        if len(non_ends) > 0:
            self.sets.append(non_ends)
        if len(ends) > 0:
            self.sets.append(ends)

    def index(self) -> dict[Node: int]:
        idx: dict[Node: int] = {}
        for i in range(len(self.sets)):
            for n in self.sets[i]:
                idx[n] = i
        return idx

    def encode(self, node: Node, idx: dict[Node: int]) -> tuple[frozenset[int], ...]:
        ls = []
        for ch in self.auto.alphabet:
            t_set = self.auto.transfer_set({node}, ch)
            from_set = frozenset([idx[out] for out in t_set])
            ls.append(from_set)
        return tuple(ls)

    def divide(self, s: set[Node], idx: dict[Node: int]) -> dict[tuple[frozenset[int], ...]: list[Node]]:
        division: dict[tuple[frozenset[int], ...]: list[Node]] = {}
        for n in s:
            code = self.encode(n, idx)
            if code not in division:
                division[code] = []
            division[code].append(n)
        return division

    def analyse(self, auto: Automaton) -> Automaton:
        self.init(auto)

        news: list[set[Node]]
        finish: bool = False
        while not finish:
            news = []
            finish = True
            idx = self.index()
            for s in self.sets:
                division = self.divide(s, idx)
                news.extend(map(set, division.values()))
                if len(division) > 1:
                    finish = False
            self.sets = news
        return self.build()

    def build(self) -> Automaton:
        build: Automaton = Automaton()
        idx = self.index()

        for i in range(len(self.sets)):
            build.add_node(Node(i))
        ns = build.nodes()

        for s in self.sets:
            n = s.pop()
            s.add(n)
            for e in self.auto.edges(n):
                build.add_edge(Edge(ns[idx[n]], ns[idx[e.n2]], e.info))

        for n in self.auto.starts:
            build.starts.append(ns[idx[n]])
        build.starts = list(set(build.starts))

        for n in self.auto.ends:
            build.ends.append(ns[idx[n]])
        build.ends = list(set(build.ends))

        build.alphabet = self.auto.alphabet
        return build


if __name__ == "__main__":
    from automaton_visualize import visualize
    analyser = Analyser()
    expr_str = input("输入正规表达式：\n")
    words = reg_to_words.Analyser().analyse(expr_str)
    tree = words_to_ast.Analyser().analyse(words)
    nfa = ast_to_nfa.Analyser().analyse(tree)
    dfa = nfa_to_dfa.Analyser().analyse(nfa)
    try:
        simplest = analyser.analyse(dfa)
        print("状态转换图为：")
        print(simplest)
        visualize(simplest)
    except ValueError as err:
        print("匹配失败。")
        traceback.print_exc()
