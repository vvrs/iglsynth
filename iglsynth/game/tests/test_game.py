from iglsynth.util.graph import *
from iglsynth.game.game import *


def test_game_basic():
    graph = Graph()
    graph.add_vertex_property(name="is_final", of_type="bool")
    graph.add_edge_property(name="act", of_type="int")

    print(graph.vertex_properties)
    print(graph.edge_properties)
    print(graph.graph_properties)

    game = Game()
    game.define(graph=graph)

    print(game.kind)
    print(type(graph.is_final), graph.is_final)
