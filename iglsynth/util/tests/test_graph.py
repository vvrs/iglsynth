import pytest
from iglsynth.util.graph import *


def test_graph_instantiation():
    # 1. Default constructor
    graph = Graph()
    assert str(graph) == "Graph(|V|=0, |E|=0, vprops=[], eprops=[], gprops=[])"

    # 2. Construct with specified vertex, edge and graph properties, defaults are empty tuple.
    graph = Graph(vprops=[("turn", "bool")], eprops=(("act", "int"), ("prob", "float")), gprops=[("name", "string")])
    assert str(graph) == "Graph(|V|=0, |E|=0, vprops=['turn'], eprops=['act', 'prob'], gprops=['name'])"


def test_graph_properties():
    # Create a graph instance
    graph = Graph(vprops=[("turn", "bool")], eprops=(("act", "int"), ("prob", "float")), gprops=[("name", "string")])

    # Add vertices and edges
    v1 = graph.add_vertex()
    v2 = graph.add_vertex()
    e1 = graph.add_edge(v1, v2)

    # Check properties
    assert graph.num_vertices == 2
    assert graph.num_edges == 1
    assert str([v for v in graph.vertices]) == "[0, 1]"
    assert str([e for e in graph.edges]) == "[Edge(source=0, target=1)]"
    assert {"act", "turn", "prob", "name"} == set(graph.properties)
    assert {"turn"} == set(graph.vertex_properties)
    assert {"act", "prob"} == set(graph.edge_properties)
    assert {"name"} == set(graph.graph_properties)


def test_add_vertex():
    graph = Graph()
    vid = graph.add_vertex()
    assert graph.num_vertices == 1
    assert vid == 0


def test_add_vertices():
    graph = Graph()

    # Add 1 vertex
    v0 = graph.add_vertices(num=1)
    assert graph.num_vertices == 1
    assert v0 == [0]

    # Add multiple vertices
    v1, v2 = graph.add_vertices(num=2)
    assert graph.num_vertices == 3
    assert v1 == 1
    assert v2 == 2

    # Check if error raised when num <= 0
    with pytest.raises(AssertionError):
        graph.add_vertices(num=0)

    with pytest.raises(AssertionError):
        graph.add_vertices(num=-2)


def test_add_edge():
    graph = Graph()
    v0, v1 = graph.add_vertices(num=2)
    graph.add_edge(v0, v1)

    assert graph.num_edges == 1


def test_add_edges():
    edges = [(0, 0), (0, 1), (1, 1)]
    graph = Graph()
    graph.add_vertices(num=2)
    graph.add_edges(edges=edges)

    assert graph.num_edges == 3


def test_remove_vertex():
    graph = Graph()
    graph.add_vertex()
    graph.remove_vertex(0)
    assert graph.num_vertices == 0


def test_remove_vertices():
    graph = Graph()

    # Single vertex
    graph.add_vertices(1)
    graph.remove_vertices([0])
    assert graph.num_vertices == 0

    # Multiple vertices
    graph.add_vertices(num=3)
    graph.remove_vertices([0, 1, 2])
    print(list(graph.vertices))
    assert graph.num_vertices == 0

    # Remove non-existing vertex
    graph.remove_vertices([0, 1])


def test_add_v_e_g_property():
    # Construct with specified vertex, edge and graph properties. Internally, it calls add_<v/e/g/>_property.
    graph = Graph(vprops=[("turn", "bool")], eprops=(("act", "int"), ("prob", "float")), gprops=[("name", "string")])
    assert str(graph) == "Graph(|V|=0, |E|=0, vprops=['turn'], eprops=['act', 'prob'], gprops=['name'])"


def test_has_v_e_g_property():
    # Construct with specified vertex, edge and graph properties. Internally, it calls add_<v/e/g/>_property.
    graph = Graph(vprops=[("turn", "bool")], eprops=(("act", "int"), ("prob", "float")), gprops=[("name", "string")])

    assert graph.has_vertex_property("turn") is True
    assert graph.has_edge_property("act") is True
    assert graph.has_graph_property("name") is True

    assert graph.has_vertex_property("act") is False
    assert graph.has_edge_property("turn") is False
    assert graph.has_graph_property("turn") is False


def test_typeof_v_e_g_property():
    # Construct with specified vertex, edge and graph properties. Internally, it calls add_<v/e/g/>_property.
    graph = Graph(vprops=[("turn", "bool")], eprops=(("act", "int"), ("prob", "float")), gprops=[("name", "string")])

    assert graph.typeof_vertex_property("turn") == "bool"
    assert graph.typeof_edge_property("act") == "int"
    assert graph.typeof_graph_property("name") == "string"


def test_get_set_v_e_g_property():
    # Construct with specified vertex, edge and graph properties. Internally, it calls add_<v/e/g/>_property.
    graph = Graph(vprops=[("turn", "bool")], eprops=(("act", "int"), ("prob", "float")), gprops=[("name", "string")])

    # Add vertices and an edge
    graph.add_vertices(num=2)
    edge = graph.add_edge(0, 1)

    # Check the default values
    assert graph.get_vertex_property(name="turn", vid=0) is False
    assert graph.get_vertex_property(name="turn", vid=1) is False
    assert graph.get_edge_property(name="act", edge=edge) == 0
    assert graph.get_graph_property(name="name") == ""

    # Set property
    graph.set_vertex_property(name="turn", vid=0, value=True)
    graph.set_vertex_property(name="turn", vid=1, value=True)
    graph.set_edge_property(name="act", edge=edge, value=10)
    graph.set_graph_property(name="name", value="hello")

    # Check the updated properties
    assert graph.get_vertex_property(name="turn", vid=0) is True
    assert graph.get_vertex_property(name="turn", vid=1) is True

    # Access complete maps.
    print(graph.get_vertex_property(name="turn"))
    print(graph.get_edge_property(name="act"))
    print(graph.get_graph_property(name="name"))


if __name__ == '__main__':
    # test_graph_instantiation()
    # test_graph_properties()
    # test_add_edges()
    # test_remove_vertices()
    test_get_set_v_e_g_property()
