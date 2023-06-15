import traceback

import reg_to_words
import words_to_ast
import ast_to_nfa
from graph import Node, Edge
from automaton import Automaton


class Analyser:
    def __init__(self):
        self.auto: Automaton = Automaton()
        self.table: list[list[set[Node]]] = []
        self.sets: list[set[Node]] = []
        self.build: Automaton = Automaton()

    def init(self, auto: Automaton):
        self.auto = auto
        self.table = []
        self.sets = []
        self.build = Automaton()

    def make_table(self):
        start = self.auto.epsilon_enclosure(set(self.auto.starts))
        self.table = [[start]]
        self.sets = [start]
        pointer = 0
        while pointer < len(self.table):
            for ch in self.auto.alphabet[1:]:
                self.table[pointer].append(set())
                t_set = self.auto.transfer_set(self.table[pointer][0], ch)
                self.table[pointer][-1] = t_set
                if len(t_set) != 0 and t_set not in self.sets:
                    self.sets.append(t_set)
                    self.table.append([t_set])
            pointer += 1

    def make_automaton(self):
        ns = [Node(i) for i in range(len(self.sets))]
        idx = {frozenset(self.sets[i]): i for i in range(len(self.sets))}

        for node in ns:
            self.build.add_node(node)

        for line in self.table:
            u = ns[idx[frozenset(line[0])]]
            for i in range(1, len(line)):
                ch = self.auto.alphabet[i]
                if len(line[i]) != 0:
                    v = ns[idx[frozenset(line[i])]]
                    self.build.add_edge(Edge(u, v, ch))

        self.build.starts = [ns[0]]

        ends = set(self.auto.ends)
        for s in self.sets:
            if not s.isdisjoint(ends):
                self.build.ends.append(ns[idx[frozenset(s)]])

        self.build.alphabet = self.auto.alphabet[1:]

    def analyse(self, auto: Automaton) -> Automaton:
        self.init(auto)
        self.make_table()
        self.make_automaton()
        return self.build


if __name__ == "__main__":
    from automaton_visualize import visualize
    analyser = Analyser()
    expr_str = input("输入正规表达式：\n")
    words = reg_to_words.Analyser().analyse(expr_str)
    tree = words_to_ast.Analyser().analyse(words)
    nfa = ast_to_nfa.Analyser().analyse(tree)
    try:
        dfa = analyser.analyse(nfa)
        print("状态转换图为：")
        print(dfa)
        visualize(dfa)
    except ValueError as err:
        print("匹配失败。")
        traceback.print_exc()
