import reg_to_words
from automaton import Automaton
from graphviz import Digraph


def visualize(auto: Automaton) -> None:
    g = Digraph()
    ns = auto.nodes()
    idx = {ns[i]: i for i in range(len(ns))}
    for i in range(len(ns)):
        n = ns[i]
        label = str(n.info)
        if n in auto.starts:
            label += "\nstart"
        if n in auto.ends:
            label += "\nend"
        g.node(f"{idx[n]}", label)
    for e in auto.edges():
        g.edge(f"{idx[e.n1]}", f"{idx[e.n2]}", reg_to_words.Analyser.unescape(e.info))
    g.view(directory="./visualize")
