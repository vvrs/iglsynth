import graph_tool as gt
from typing import Iterable, Iterator, List, Tuple

class Graph(object):
    """
    Represents a discrete graph :math:`G = (V, E, vprops, eprops, gprops)`.

    :param vprops: An iterable of 2-tuple of (vertex-property-name, vertex-property-type). The type must be a string
        from values of dictionary :data:`Graph.VALID_PROPERTY_TYPES`
    :type vprops: Iterable[Tuple[str, str]]

    :param eprops: An iterable of 2-tuple of (vertex-property-name, vertex-property-type). The type must be a string
        from values of dictionary :data:`Graph.VALID_PROPERTY_TYPES`
    :type eprops: Iterable[Tuple[str, str]]

    :param gprops: An iterable of 2-tuple of (vertex-property-name, vertex-property-type). The type must be a string
        from values of dictionary :data:`Graph.VALID_PROPERTY_TYPES`
    :type gprops: Iterable[Tuple[str, str]]
    """

    # ------------------------------------------------------------------------------------------------------------------
    # CLASS VARIABLES
    # ------------------------------------------------------------------------------------------------------------------
    VALID_PROPERTY_TYPES = {bool: "bool", int: "int", float: "float", str: "string", object: "object"}

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL PRIVATE CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    class Edge(object):
        """
        [INTERNAL CLASS] Users should not instantiate this class.

        :param graph: A :class:`Graph` object.
        :param gt_edge: A :class:`gt.Edge`object.

        .. note: This class is expected to maintain the API for properties and definition of equivalence. The
        initialization parameters may change according to the internal graph library that is used
        (presently graph_tool).
        """

        __hash__ = object.__hash__

        def __init__(self, graph, gt_edge):
            self._graph = graph
            self._edge = gt_edge

        def __repr__(self):
            return f"Edge(source={self.source}, target={self.target})"

        def __eq__(self, other: 'Edge'):
            """ Two edges are equivalent, if their source, target and all properties are equivalent. """
            return self.edge == other.edge

        @property
        def source(self):
            return int(self._edge.source())

        @property
        def target(self):
            return int(self._edge.target())

        @property
        def edge(self):
            return self._edge

    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, vprops: Iterable[Tuple[str, str]] = tuple(), eprops: Iterable[Tuple[str, str]] = tuple(),
                 gprops: Iterable[Tuple[str, str]] = tuple()):

        # Define a graph object
        self._graph = gt.Graph()

        # Create an edge dictionary to maintain a map of edge id's and edge objects {eid: gt.edge_obj}
        self._edge_map = dict()

        # Add vertex properties
        for name, of_type in vprops:
            self.add_vertex_property(name=name, of_type=of_type)

        # Add edge properties
        for name, of_type in eprops:
            self.add_edge_property(name=name, of_type=of_type)

        # Add graph properties
        for name, of_type in gprops:
            self.add_graph_property(name=name, of_type=of_type)

    def __repr__(self):
        return f"Graph(|V|={self.num_vertices}, |E|={self.num_edges}, vprops={self.vertex_properties}, " \
               f"eprops={self.edge_properties}, gprops={self.graph_properties})"

    def __getattr__(self, item):
        if item in self.vertex_properties:
            return self.get_vertex_property(name=item)

        elif item in self.edge_properties:
            return self.get_edge_property(name=item)

        elif item in self.graph_properties:
            return self.get_graph_property(name=item)

        else:
            raise AttributeError(f"{item} is not an attribute in class Graph.")

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vertices(self) -> Iterator:
        """
        Returns an iterator over vertices in graph.
        """
        return iter(int(v) for v in self._graph.vertices())

    @property
    def edges(self) -> Iterator:
        """
        Returns an iterator over edges in graph.
        """
        return iter(Graph.Edge(graph=self, gt_edge=edge) for edge in self._graph.edges())

    @property
    def num_vertices(self) -> int:
        """
        Returns the number of vertices in graph.
        """
        return self._graph.num_vertices()

    @property
    def num_edges(self) -> int:
        """
        Returns the number of edges in graph.
        """
        return self._graph.num_edges()

    @property
    def vertex_properties(self) -> List[str]:
        """
        Returns the a list of vertex property names in graph.
        """
        return self._graph.vertex_properties.keys()

    @property
    def edge_properties(self):
        """
        Returns a list of edge property names in graph.
        """
        return self._graph.edge_properties.keys()

    @property
    def graph_properties(self):
        """
        Returns a list of graph property names in graph.
        """
        return self._graph.graph_properties.keys()

    @property
    def properties(self):
        """
        Returns a list of all properties of graph, including vertex, edge and graph properties.
        """
        return tuple(prop[1] for prop in self._graph.properties.keys())

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC METHODS
    # ------------------------------------------------------------------------------------------------------------------
    def add_vertex(self) -> int:
        """ Creates a new vertex in graph. """
        return int(self._graph.add_vertex())

    def add_vertices(self, num: int) -> Iterable[int]:
        """
        Creates a given number of vertices in graph.

        :param num: Number of vertices to be added.
        :type num: int (> 0)

        :raises AssertionError: When num <= 0.
        """
        assert num > 0, f"Required, num > 0. Received, num = {num}."
        if num == 1:
            return [self.add_vertex()]
        else:
            return [int(v) for v in self._graph.add_vertex(n=num)]

    def add_edge(self, uid: int, vid: int) -> 'Graph.Edge':
        """
        Adds an edge in the graph. Both the vertices must be present in the graph.

        :param uid: Vertex ID of source vertex.
        :type uid: int

        :param vid: Vertex ID of target vertex.
        :type uid: int

        :return: :class:`Graph.Edge` object representing the edge.

        :raises AssertionError: When at least one of the vertex is not in the graph.
        """
        try:
            edge = self._graph.add_edge(uid, vid, add_missing=False)
            return Graph.Edge(graph=self, gt_edge=edge)

        except ValueError:
            uid_in_graph = "IN-GRAPH" if uid in self.vertices else "NOT-IN-GRAPH"
            vid_in_graph = "IN-GRAPH" if vid in self.vertices else "NOT-IN-GRAPH"
            raise AssertionError(f"At least one vertex is not in graph. "
                             f"Vertex {uid}: {uid_in_graph}, Vertex {vid}: {vid_in_graph}.")

    def add_edges(self, edges: Iterable[Tuple[int, int]]) -> Iterator['Graph.Edge']:
        """
        Adds multiple edges to the graph. All the vertices must be present in the graph.

        :param edges: An iterable of 2-tuple of (uid, vid) representing the edge, where uid is source and vid is target.
        :type edges: Iterable[Tuple[int, int]]

        :raises ValueError: When at least one of the vertex is not in the graph.
        """

        return iter([self.add_edge(u, v) for u, v in edges])

    def remove_vertex(self, vid):
        """
        Removes a single vertex from the graph, if exists.

        :param vid: Vertex id.
        :type vid: int
        """
        if vid in self.vertices:
            self._graph.remove_vertex(vid)

    def remove_vertices(self, vid: Iterable[int]):
        """
        Removes a multiple vertices from the graph, if existing.

        :param vid: A list of vertex id's.
        :type vid: Iterable[int]
        """
        for v in reversed(sorted(vid)):
            self.remove_vertex(v)

    def remove_edge(self, edge: 'Graph.Edge'):
        """
        Removes a single edge from graph.

        :param edge: :class:`Graph.Edge` object to be removed.
        """
        if edge.edge in self._graph.edges():
            self._graph.remove_edge(edge.edge)

    def remove_edges(self, edges: Iterable['Graph.Edge']):
        """
        Removes multiple edges from graph.

        :param edges: A list of :class:`Graph.Edge` object to be removed.
        """
        for edge in edges:
            self.remove_edge(edge)

    def add_vertex_property(self, name: str, of_type: str = "object"):
        """
        Creates a new vertex property for the graph.

        :param name: Name of the property. The given name must be unique among all vertex/edge/graph properties.
        :type name: str
        :param of_type: One of the supported types of properties. See :data:`Graph.VALID_PROPERTY_TYPES`

        :raises NameError: If given name is already a property.
        :raises TypeError: If the given type is invalid.
        """
        # Validate that name is not already a property
        if name in self.properties:
            raise NameError(f"Given vertex property name: {name} is already a property. ")

        # Validate whether the type of property is acceptable
        if of_type not in self.VALID_PROPERTY_TYPES.values():
            raise TypeError(f"Given vertex property type: {of_type} is invalid. "
                            f"Types must be in {self.VALID_PROPERTY_TYPES.values()}")

        self._graph.vertex_properties[name] = self._graph.new_vertex_property(value_type=of_type)

    def add_edge_property(self, name: str, of_type: str = "object"):
        """
        Creates a new edge property for the graph.

        :param name: Name of the property. The given name must be unique among all vertex/edge/graph properties.
        :type name: str
        :param of_type: One of the supported types of properties. See :data:`Graph.VALID_PROPERTY_TYPES`

        :raises NameError: If given name is already a property.
        :raises TypeError: If the given type is invalid.
        """
        # Validate that name is not already a property
        if name in self.properties:
            raise NameError(f"Given edge property name: {name} is already a property. ")

        # Validate whether the type of property is acceptable
        if of_type not in self.VALID_PROPERTY_TYPES.values():
            raise TypeError(f"Given edge property type: {of_type} is invalid. "
                            f"Types must be in {self.VALID_PROPERTY_TYPES.values()}")

        self._graph.edge_properties[name] = self._graph.new_edge_property(value_type=of_type)

    def add_graph_property(self, name: str, of_type: str = "object"):
        """
        Creates a new graph property for the graph.

        :param name: Name of the property. The given name must be unique among all vertex/edge/graph properties.
        :type name: str
        :param of_type: One of the supported types of properties. See :data:`Graph.VALID_PROPERTY_TYPES`

        :raises NameError: If given name is already a property.
        :raises TypeError: If the given type is invalid.
        """
        # Validate that name is not already a property
        if name in self.properties:
            raise NameError(f"Given graph property name: {name} is already a property. ")

        # Validate whether the type of property is acceptable
        if of_type not in self.VALID_PROPERTY_TYPES.values():
            raise TypeError(f"Given graph property type: {of_type} is invalid. "
                            f"Types must be in {self.VALID_PROPERTY_TYPES.values()}")

        self._graph.graph_properties[name] = self._graph.new_graph_property(value_type=of_type)

    def has_vertex_property(self, name: str, of_type: str = None) -> bool:
        """
        Checks if graph has a vertex property with give name. If type is provided, it checks whether the vertex property
        with given name and type exists.

        :param name: Name of vertex property.
        :type name: str

        :param of_type: Expected type of the property.
        :type of_type: str (a value from :data:`Graph.VALID_PROPERTY_TYPES`
        """
        if of_type is not None:
            if name in self.vertex_properties:
                return of_type == self.typeof_vertex_property(name=name)

            return False

        return name in self.vertex_properties

    def has_edge_property(self, name: str, of_type: str = None) -> bool:
        """
        Checks if graph has a edge property with give name. If type is provided, it checks whether the edge property
        with given name and type exists.

        :param name: Name of edge property.
        :type name: str

        :param of_type: Expected type of the property.
        :type of_type: str (a value from :data:`Graph.VALID_PROPERTY_TYPES`
        """
        if of_type is not None:
            if name in self.edge_properties:
                return of_type == self.typeof_edge_property(name=name)

            return False

        return name in self.edge_properties

    def has_graph_property(self, name: str, of_type: str = None) -> bool:
        """
        Checks if graph has a graph property with give name. If type is provided, it checks whether the graph property
        with given name and type exists.

        :param name: Name of graph property.
        :type name: str

        :param of_type: Expected type of the property.
        :type of_type: str (a value from :data:`Graph.VALID_PROPERTY_TYPES`
        """

        if of_type is not None:
            if name in self.graph_properties:
                return of_type == self.typeof_graph_property(name=name)

            return False

        return name in self.graph_properties

    def get_vertex_property(self, name: str, vid: int = None):
        """
        Get the value of vertex property for a given vertex.

        :param name: Name of vertex property.
        :type name: str

        :param vid: Vertex ID of the vertex for which the property value is to be extracted.
            If vertex ID is not given then complete dictionary of property {vid: prop_value} is returned.
        :type vid: int

        :return: Value of the property.
        """
        if vid is None:
            if name in self.vertex_properties:
                return dict(zip(range(self.num_vertices), self._graph.vertex_properties[name].ma))

        else:
            if name in self.vertex_properties and vid in self.vertices:
                return self._graph.vertex_properties[name].python_value_type()(self._graph.vertex_properties[name][vid])

    def get_edge_property(self, name: str, edge: 'Graph.Edge' = None):
        """
        Get the value of edge property for a given edge.

        :param name: Name of edge property.
        :type name: str

        :param edge: Edge for which the property value is to be extracted.
        :type edge: :class:`Graph.Edge`

        :return: Value of the property.

        .. todo: Make ``edge`` to be an optional parameter. When ``edge = None`` return the properties for all edges
            as a dictionary.
        """
        if edge is None:
            if name in self.edge_properties:
                return dict(zip((Graph.Edge(graph=self, gt_edge=edge) for edge in self._graph.edges()),
                                self._graph.edge_properties[name].ma))

        else:
            if name in self.edge_properties and edge.edge in self._graph.edges():
                return self._graph.edge_properties[name].python_value_type()(self._graph.
                                                                             edge_properties[name][edge.edge])

    def get_graph_property(self, name: str):
        """
         Get the value of graph property.

         :param name: Name of graph property.
         :type name: str

         :return: Value of the property.
         """
        if name in self.graph_properties:
            return self._graph.graph_properties[name]

    def set_vertex_property(self, name: str, vid: int, value):
        if name in self.vertex_properties:
            self._graph.vertex_properties[name][vid] = value
        else:
            raise NameError(f"{name} is not a valid vertex property.")

    def set_edge_property(self, name: str, edge: 'Graph.Edge', value):
        if name in self.edge_properties and edge.edge in self._graph.edges():
            self._graph.edge_properties[name][edge.edge] = value

        else:
            raise NameError(f"{name} is not a valid edge property.")

    def set_graph_property(self, name: str, value):
        if name in self.graph_properties:
            self._graph.graph_properties[name] = value

        else:
            raise NameError(f"{name} is not a valid graph property.")

    def typeof_vertex_property(self, name: str):
        """
        Returns the type of vertex property.

        :param name: Name of property.
        :type name: str

        :return: Type of property from :data:`Graph.VALID_PROPERTY_TYPES`.
        """
        if not self.has_vertex_property(name=name):
            raise NameError("'{0}' is not a vertex property of graph '{1}'".format(name, self))

        prop = self._graph.vertex_properties[name]
        return self.VALID_PROPERTY_TYPES[prop.python_value_type()]

    def typeof_edge_property(self, name: str):
        """
        Returns the type of edge property.

        :param name: Name of property.
        :type name: str

        :return: Type of property from :data:`Graph.VALID_PROPERTY_TYPES`.
        """
        if not self.has_edge_property(name=name):
            raise NameError("'{0}' is not a edge property of graph '{1}'".format(name, self))

        prop = self._graph.edge_properties[name]
        return self.VALID_PROPERTY_TYPES[prop.python_value_type()]

    def typeof_graph_property(self, name: str):
        """
        Returns the type of graph property.

        :param name: Name of property.
        :type name: str

        :return: Type of property from :data:`Graph.VALID_PROPERTY_TYPES`.
        """
        if not self.has_graph_property(name=name):
            raise NameError("'{0}' is not a graph property of graph '{1}'".format(name, self))

        # PATCH #2: Support all python object types, by casting them into "object" if they are not from the list of
        #   VALID_PROPERTY_TYPES.
        prop = self._graph.graph_properties[name]
        if type(prop) in self.VALID_PROPERTY_TYPES:
            return self.VALID_PROPERTY_TYPES[type(prop)]
        return "object"

    def in_edges(self, vid: int):
        return iter(Graph.Edge(graph=self, gt_edge=edge) for edge in self._graph.get_in_edges(vid))

    def out_edges(self, vid: int):
        return iter(Graph.Edge(graph=self, gt_edge=edge) for edge in self._graph.get_out_edges(vid))
