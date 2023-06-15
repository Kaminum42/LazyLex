from typing import Optional
import traceback
import reg_to_words
from reg_ast import ASTNode


class Analyser:
    def __init__(self):
        self.expression: list[str] = []
        self.pointer: int = 0

    def error(self):
        raise ValueError(f"在 {''.join(self.expression[:self.pointer + 1])} 末尾处匹配失败。")

    def init(self) -> None:
        self.pointer = 0

    def analyse(self, expr: list[str]) -> ASTNode:
        self.init()
        self.expression = expr
        root = self.s()
        if self.pointer != len(self.expression):
            self.error()
        return root

    def match(self, ch: str) -> None:
        assert self.pointer < len(self.expression)
        if self.expression[self.pointer] != ch:
            self.error()
        self.pointer += 1

    def peek(self) -> str:
        if self.pointer < len(self.expression):
            return self.expression[self.pointer]
        else:
            return "\0"

    def s(self) -> ASTNode:
        left = self.t()
        right = self.s1()

        if not right:
            return left
        root = ASTNode(value="|", c_cnt=2)
        root.set_child(left, 0)
        root.set_child(right, 1)
        return root

    def s1(self) -> Optional[ASTNode]:
        if self.peek() == "|":
            self.match("|")
            left = self.t()
            right = self.s1()

            if not right:
                return left
            root = ASTNode(value="|", c_cnt=2)
            root.set_child(left, 0)
            root.set_child(right, 1)
            return root

    def t(self) -> ASTNode:
        left = self.u()
        right = self.t1()

        if not right:
            return left
        root = ASTNode(value=".", c_cnt=2)
        root.set_child(left, 0)
        root.set_child(right, 1)
        return root

    def t1(self) -> Optional[ASTNode]:
        if self.peek() == ".":
            self.match(".")
            left = self.u()
            right = self.t1()

            if not right:
                return left
            root = ASTNode(value=".", c_cnt=2)
            root.set_child(left, 0)
            root.set_child(right, 1)
            return root

    def u(self) -> ASTNode:
        left = self.v()
        right = self.u1()

        if not right:
            return left
        leaf = right
        while len(leaf.children) > 0:
            leaf = leaf.children[0]
        leaf.parent.set_child(left, 0)
        return right

    def u1(self) -> Optional[ASTNode]:
        if self.peek() == "*":
            self.match("*")
            parent = self.u1()
            if not parent:
                return ASTNode(value="*", c_cnt=1)
            parent.set_child(ASTNode(value="*", c_cnt=1), 0)
            return parent

    def v(self) -> ASTNode:
        if self.peek() == "(":
            self.match("(")
            child = self.s()
            self.match(")")
        else:
            child = self.c()
        return child

    def c(self) -> ASTNode:
        ch = self.peek()
        if ch not in "()|.*\0":
            self.match(ch)
            left = ASTNode(value=ch)
            right = self.c1()

            if not right:
                return left
            root = ASTNode(value=".", c_cnt=2)
            root.set_child(left, 0)
            root.set_child(right, 1)
            return root
        else:
            self.error()

    def c1(self) -> Optional[ASTNode]:
        ch = self.peek()
        if ch not in "()|.*\0":
            self.match(ch)
            left = ASTNode(value=ch)
            right = self.c1()

            if not right:
                return left
            root = ASTNode(value=".", c_cnt=2)
            root.set_child(left, 0)
            root.set_child(right, 1)
            return root


if __name__ == "__main__":
    analyser = Analyser()
    expr_str = input("输入正规表达式：\n")
    words = reg_to_words.Analyser().analyse(expr_str)
    try:
        tree = analyser.analyse(words)
        print("语法树（逆波兰式）为：")
        print(tree)
    except ValueError as err:
        print("匹配失败。")
        traceback.print_exc()
