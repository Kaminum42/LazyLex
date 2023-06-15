import string
import dill
from typing import Callable
from functools import partial

import dfa_simplify
import reg_to_words
import words_to_ast
import ast_to_nfa
import nfa_to_dfa
from automaton import Automaton
from lex_token import Token


class Analyser:
    def __init__(self):
        self.rules: list[tuple[Automaton, Callable[[str], Token]]] = []
        self.aux: dict[str: list[str]] = {}
        self.init_aux()

    def init_aux(self) -> None:
        self.aux[r"\d"] = list(string.digits)
        self.aux[r"\l"] = list(string.ascii_lowercase)
        self.aux[r"\u"] = list(string.ascii_uppercase)
        self.aux[r"\w"] = list(string.ascii_letters + string.digits + "_")
        self.aux[r"\s"] = list(string.whitespace)
        self.aux[r"\p"] = list(string.punctuation)
        self.aux[r"\P"] = list(string.printable)

        self.aux[r"\D"] = list(set(self.aux[r"\P"]) - set(self.aux[r"\d"]))
        self.aux[r"\L"] = list(set(self.aux[r"\P"]) - set(self.aux[r"\l"]))
        self.aux[r"\U"] = list(set(self.aux[r"\P"]) - set(self.aux[r"\u"]))
        self.aux[r"\W"] = list(set(self.aux[r"\P"]) - set(self.aux[r"\w"]))
        self.aux[r"\S"] = list(set(self.aux[r"\P"]) - set(self.aux[r"\s"]))

    def add_aux(self, aux_name: str, aux_base: str, aux_type: int, aux_str: str) -> None:
        if aux_type == 0:
            self.aux[aux_name] = list(set(self.aux[aux_base]).union(set(aux_str)))
        elif aux_type == 1:
            self.aux[aux_name] = list(set(self.aux[aux_base]) - set(aux_str))

    def add_rule(self, reg: str, eval_func: Callable[[str], Token]) -> None:
        words = reg_to_words.Analyser().analyse(reg)
        ast = words_to_ast.Analyser().analyse(words)
        nfa = ast_to_nfa.Analyser().analyse(ast)
        dfa = nfa_to_dfa.Analyser().analyse(nfa)
        simplest = dfa_simplify.Analyser().analyse(dfa)
        for aux_name, aux_str in self.aux.items():
            simplest.add_transfer_word(aux_name, aux_str)
        self.rules.append((simplest, eval_func))

    def single_step(self, expr: str) -> tuple[str, Token]:
        for rule in self.rules:
            try:
                matched = rule[0].dfa_match_prefix(expr)
                return matched, rule[1](matched)
            except ValueError:
                pass
        raise ValueError(f"无法为 {repr(expr)} 找到匹配的规则。")

    def analyse(self, expr: str) -> list[Token]:
        tokens = []
        while expr != "":
            matched, tok = self.single_step(expr)
            expr = expr[len(matched):]
            tokens.append(tok)
        return tokens


if __name__ == "__main__":
    analyser = Analyser()
    aux_list: list[tuple[str, int, str]] = []
    reg_list: list[str] = []

    lex_filename = input("输入词法文件路径(xxx.lex)：\n")
    with open(lex_filename, "r", encoding="utf-8") as file:
        # n = int(input("输入新增辅助规则数：\n"))
        n = int(file.readline().strip("\t\n"))
        for i in range(n):
            # name = input("输入辅助名(形如 '\\x')：\n")
            # aux_base = input("基于的辅助规则名：\n")
            # aux_type = int(input("添加/删除？(0/1)\n"))
            # aux = input("输入辅助规则：\n")
            name = file.readline().strip("\t\n")
            aux_bas = file.readline().strip("\t\n")
            aux_typ = int(file.readline().strip("\t\n"))
            aux = str(list(map(reg_to_words.Analyser.escape, file.readline().strip("\t\n"))))
            print(f"辅助规则{i} {repr(name)} 基于 {repr(aux_bas)} {['添加', '删除'][aux_typ]} {repr(aux)}")
            analyser.add_aux(name, aux_bas, aux_typ, aux)
        # m = int(input("输入规则数：\n"))
        m = int(file.readline().strip("\t\n"))
        for i in range(m):
            reg_str = file.readline().strip("\t\n")
            print(f"规则{i} {repr(reg_str)}")
            analyser.add_rule(reg_str, partial(lambda typ, val: (typ, val), i))

    pickle_filename = input("输入词法器模型路径(xxx.lexer)：\n")
    with open(pickle_filename, "wb") as file:
        dill.dump(analyser, file)
    print("词法器模型生成完毕。")
