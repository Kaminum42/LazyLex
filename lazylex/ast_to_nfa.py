import traceback

from reg_ast import ASTNode
from graph import Node, Edge
from automaton import Automaton
import reg_to_words
import words_to_ast


class Analyser:
    def __init__(self):
        self.auto: Automaton = Automaton()
        self.cnt = 0

    def init(self) -> None:
        self.cnt = 0
        self.auto = Automaton()
        x, y = Node("x"), Node("y")
        self.auto.set_start(x)
        self.auto.set_end(y)
        self.auto.add_edge(Edge(x, y))
        self.auto.alphabet.append("ε")

    def build(self, ast: ASTNode, edge: Edge) -> None:
        n1, n2 = edge.n1, edge.n2

        if ast.value == "|":
            e1, e2 = Edge(n1, n2), Edge(n1, n2)
            self.auto.del_edge(edge)
            self.auto.add_edge(e1)
            self.auto.add_edge(e2)
            self.build(ast.children[0], e1)
            self.build(ast.children[1], e2)
        elif ast.value == ".":
            n = Node(self.cnt)
            self.cnt += 1
            e1, e2 = Edge(n1, n), Edge(n, n2)
            self.auto.del_edge(edge)
            self.auto.add_node(n)
            self.auto.add_edge(e1)
            self.auto.add_edge(e2)
            self.build(ast.children[0], e1)
            self.build(ast.children[1], e2)
        elif ast.value == "*":
            n = Node(self.cnt)
            self.cnt += 1
            e1, e2, e3 = Edge(n1, n, "ε"), Edge(n, n), Edge(n, n2, "ε")
            self.auto.del_edge(edge)
            self.auto.add_node(n)
            self.auto.add_edge(e1)
            self.auto.add_edge(e2)
            self.auto.add_edge(e3)
            self.build(ast.children[0], e2)
        else:
            edge.info = reg_to_words.Analyser.escape(ast.value)
            if edge.info not in self.auto.alphabet:
                self.auto.alphabet.append(edge.info)

    def analyse(self, ast: ASTNode) -> Automaton:
        self.init()
        start = self.auto.starts[0]
        edge = self.auto.edges(start)[0]
        self.build(ast, edge)
        return self.auto


if __name__ == "__main__":
    from automaton_visualize import visualize
    analyser = Analyser()
    expr_str = input("输入正规表达式：\n")
    words = reg_to_words.Analyser().analyse(expr_str)
    tree = words_to_ast.Analyser().analyse(words)
    try:
        auto = analyser.analyse(tree)
        print("状态转换图为：")
        print(auto)
        visualize(auto)
    except ValueError as err:
        print("匹配失败。")
        traceback.print_exc()
