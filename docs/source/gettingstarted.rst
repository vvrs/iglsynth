Getting Started
===============


:mod:`iglsynth` primarily deals with games or hypergames defined on graphs.
It is divided in 4 modules, namely

- :mod:`util`: defines the data structures and utility functions required by various modules in :mod:`iglsynth`.
- :mod:`game`: defines the classes used to define games or hypergames on graph.
- :mod:`logic`: defines different logic families, acceptance conditions and automata.
- :mod:`solver`: define solvers for different games or hypergames.



A typical workflow for solving a game-on-graph problem may include following steps:

1. Define a Kripke structure ``model`` that captures the interaction graph between two players.
The :mod:`game` module provides classes to define different deterministic/stochastic
turn-based/concurrent models.

2. Define an ``acceptance_condition`` to represent the objectives of players.
The :mod:`logic` module provides classes implementing several acceptance conditions, such as
:class:`Reachability`, :class:`Buchi` etc.

3. Define a game as an instance of class :class:`game.Game` using a ``model`` and ``acceptance_condition``.

4. Finally, invoke a solver from `solver` sub-package to compute the winning regions and strategies
in the defined game.



Graphs
------

Graph is the most common data structure used in :mod:`iglsynth`. It is defined as

        :math:`G = \langle V, E, vprops, eprops, gprops \rangle`

where

    * :math:`vprops` are vertex properties associated with all vertices :math:`V`,
    * :math:`eprops` are edge properties associated with all edges :math:`E`,
    * :math:`gprops` are graph properties associated with entire graph :math:`G`


Different graph-based objects such as Kripke structures, automata etc.
by requiring the graph to have certain predefined properties. For instance, an automaton
must have a vertex property; ``is_final_state``.


A graph can be instantiated as

.. code-block:: python

    from iglsynth.util.graph import *
    graph = Graph()


Vertices and edges may be added to graph as follows,

.. code-block:: python

    vertex_id = graph.add_vertex()                  # Adds 1 vertex and returns its ID
    vertex_id_list = graph.add_vertices(num=10)     # Adds 10 vertices and returns their IDs

    edges = [(2, 3), (1, 2)]
    edges_id = graph.add_edge(uid=0, vid=3)         # Adds edge from vertex with ID 0 to vertex with ID 3
    edges_id_list = graph.add_edges(edges=edges)    # Adds multiple edges


It is possible to create new properties for graph and get/set them.

.. code-block:: python

    graph.add_vertex_property(name="turn", of_type="int")       # Adds new vertex property
    print(graph.turn)                                           # Gets dictionary {vid: prop_value}
    print(graph.turn[0])                                        # Gets value of property for vertex 0
    graph.turn[0] = 10                                          # Sets value of property for vertex 0


See :mod:`util.graph` module documentation for detailed API documentation for :class:`util.graph.Graph`.


Acceptance Condition
--------------------

An acceptance condition represents an :math:`\omega`-regular specification. An acceptance condition
is defined using a logical specification.

.. code-block:: python

    from iglsynth.logic.acceptance import *
    from iglsynth.logic.ltl import *

    @ap
    def is_origin(state):
        return state == [0, 0]

    phi1 = LTL('F is_origin', alphabet=Alphabet(is_origin))
    acc = Reachability(phi=phi1)


.. warning:: This API is not final and might change.


Game
----

The :mod:`game` module provides several classes that define different deterministic/stochastic
turn-based/concurrent models. The class :class:`game.game.Game` represents a perfect-information
deterministic two-player game given by

* **Concurrent Game:**
    :math:`{\cal G} = \langle V, E, vprop = (\dots), eprops = (act, \ldots), gprops = (p_1, p_2, acc_1, acc_2) \rangle`
* **Turn-based Game:**
    :math:`{\cal G} = \langle V, E, vprop = (turn, \dots), eprops = (act, \ldots), gprops = (p_1, p_2, acc_1, acc_2) \rangle`

where

    - :math:`turn \in \{1, 2\}` represents the turn of player 1 or 2,
    - :math:`act \in \mathbb{Z}^+` represents an action,
    - :math:`p_1, p_2` are :class:`Player` objects representing players,
    - :math:`acc_1, acc_2` are :class:`AcceptanceCondition` objects.


The properties mentioned in parentheses "must" be associated with a game object. Users may add any
other relevant properties as they wish.

.. note::  The users are responsible for mapping action IDs to respective action objects. One possible
    way is to create a graph property ``actions1`` and ``actions2`` as dictionary of action
    id to action object. This will ensure that actions objects are saved when saving the ``game`` object.


A game can be instantiated in one of the following ways,

.. code-block:: python

    from iglsynth.game.game import *

    concurrent_game = game()
    concurrent_game = game(kind=CONCURRENT)
    turn_based_game = game(kind=TURN_BASED)


Once the game is instantiated, it must be defined. There are three ways to define a game.

.. code-block:: python

    from iglsynth.game.game import *

    # 1. Using a Kripke structure and acceptance conditions.
    game.define(model=<Kripke>, acc1=<AcceptanceCondition>, acc2=<AcceptanceCondition>)

    # 2. Using a player profiles and acceptance conditions.
    game.define(p1=<Player>, p2=<Player>, acc1=<AcceptanceCondition>, acc2=<AcceptanceCondition>)

    # 3. Using a game graph
    game.define(graph=<Graph>)


.. note:: When defining a game using ``graph`` parameter, the graph must have the properties
    ``act, p1, p2, acc1, acc2`` associated with it. If game is defined to be turn-based, then graph
    must also have ``turn`` property.


Solvers
-------

The :mod:`solver` module defines several solvers for different types of games and hypergames. All
solvers provide a ``configure`` method to set parameters for the solver. Check the API documentation
page of respective solvers to know about configuration parameters.


A typical call to solver might look as follows. Assume the game defines a reachability game.

.. code-block:: python

    from iglsynth.solvers import ZielonkaSolver
    solver = ZielonkaSolver(game=reach_game)
    solver.configure(win1=True, win2=True,
                     strategy1_type=DETERMINISTIC, strategy2_type=STOCHASTIC,
                     strategy1_lose=distributions.Uniform, strategy1_lose=distributions.Normal,
                     strategy1_compute=True, strategy1_compute=True
                    )
    solver.solve()

    # Access solutions
    print(solver.win1)
    print(solver.win2)
    print(solver.strategy1(state=<State>))
    print(solver.strategy2(state=<State>))


As player 2 is set to have a stochastic strategy, the call ``solver.strategy2(state=<State>)`` will
return an action sampled from the distribution over actions. To print the support of distribution use
``solver.strategy2[state=<State>]``.

