from iglsynth.game.game import *


def test_kripke():

    def label(graph, st, propositions):
        true_ap = set()
        for ap in propositions:
            if ap(graph, st):
                true_ap.add(ap)

        return true_ap

    a = AP(name="a", label_func=lambda graph, st, a, k: True if 0 <= st < 1 else False)
    b = AP(name="b", label_func=lambda graph, st, a, k: True if st > 1 else False)

    K = Kripke(propositions=[a, b], labeling_func=label)
    K.add_vertices(num=4)

    assert K.label_state(0) == {a}
    assert K.label_state(1) == set()
    assert K.label_state(2) == {b}
    assert K.label_graph() == {0: {a}, 1: set(), 2: {b}, 3: {b}}


