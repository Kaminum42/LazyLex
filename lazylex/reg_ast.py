class ASTNode:
    def __init__(self, parent: "ASTNode" = None, parent_idx: int = 0, value: str = "", c_cnt: int = 0) -> None:
        if parent is None:
            parent = self
        self.parent: "ASTNode" = parent
        self.parent_idx: int = parent_idx
        self.children: list["ASTNode"] = []
        self.value: str = value
        self.extend_children_count_to(c_cnt)

    def __str__(self) -> str:
        return self.reverse_polish()

    def reverse_polish(self) -> str:
        if not self.value:
            return ""
        elif not self.children:
            return f"{self.value}"
        arg_str = " ".join(map(ASTNode.reverse_polish, self.children))
        return f"({self.value} {arg_str})"

    def extend_children_count_to(self, cnt: int) -> None:
        lack_cnt = max(cnt - len(self.children), 0)
        extend_list = [ASTNode(parent=self, parent_idx=len(self.children) + i) for i in range(lack_cnt)]
        self.children.extend(extend_list)

    def set_child(self, node: "ASTNode", idx: int) -> None:
        self.extend_children_count_to(idx + 1)
        self.children[idx] = node
        node.parent, node.parent_idx = self, idx
