==================================================================
IGLSynth: Automatic Strategy Synthesis Library
==================================================================

:mod:`iglsynth` is a high-level Python API for solving Infinite Games and Logic-based strategy Synthesis. It provides
an easy interface to

1. Define two-player games-on-graphs.
2. Assign tasks to players using formal logic.
3. Write solvers to compute winning strategies in the game.



------------

Installation
------------

:mod:`iglsynth` can be easily installed on Linux/Mac/Windows using `Docker <https://www.docker.com/>`_ by running
the following command in terminal in Linux (or equivalent for other OS).

.. code-block:: bash

    docker pull abhibp1993/iglsynth


The above docker image has the latest version of :mod:`iglsynth` installed along with its dependencies. There are two
ways of developing projects using :mod:`iglsynth`,

1. Mount the project directory to docker container
(`Docker Docs for Mounting Volumes <https://docs.docker.com/storage/volumes/>`_). An example usage is as follows,

    .. code-block:: bash

        docker run -it -v /location/of/project/project_name:/home/project_name abhibp1993/iglsynth
        cd /home/project_name
        python3 project_name/file_to_run.py


2. Configure docker image as remote interpreter (`PyCharm: Configure Remote Interpreter
<https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html>`_).



------------

Getting Started
---------------

Consider the reachability game from `EPFL Slides <http://richmodels.epfl.ch/_media/w2_wed_3.pdf>`_.
shown in the figure below,

.. image:: EPFL_Problem1.png
    :scale: 50%
    :align: center
    :alt: Game graph from `EPFL Slides <http://richmodels.epfl.ch/_media/w2_wed_3.pdf>`_.


To solve this game, first create a :class:`Graph` object to represent the vertices and edges in above figure.

.. code-block:: python

    from iglsynth.util.graph import Graph

    # Instantiate graph
    graph = Graph()

    # Add vertices to graph
    vertices = graph.add_vertices(num=8)

    # Add edges to graph
    edge_list = [(0, 1), (0, 3), (1, 0), (1, 2), (1, 4), (2, 4), (2, 2), (3, 0), (3, 4), (3, 5), (4, 3),
                 (5, 3), (5, 6), (6, 6), (6, 7), (7, 0), (7, 3)]
    edges = graph.add_edges(edges=edge_list)


Now, mark the vertices ``3, 4`` as final vertices and add action labels to edges.

.. code-block:: python

    # Create vertex property to maintain set of final vertices
    graph.add_vertex_property(name="is_final", of_type="bool", default=False)

    # Set the value of property for final vertices
    graph.set_vertex_property(name="is_final", vid=3, value=True)
    graph.set_vertex_property(name="is_final", vid=4, value=True)

    # Create action as an edge property. Let index of action in edge_list be the action label.
    graph.add_edge_property(name="act", of_type="int")

    # Set the value of property for all edges
    for idx in len(edge_list):
         graph.set_edge_property(name="act", eid=edges[idx], value=idx)


This defines the graph structure as required. Next, create a :class:`Game` object to define
a deterministic two-player game that can be passed to a solver.

.. code-block:: python

    from iglsynth.game.game import Game

    # Instantiate a turn-based game
    game = Game(kind=TURN_BASED)

    # Define the game
    game.define(graph=graph)


Finally, select an appropriate solver to solve the game. We will use :class:`ZielonkaSolver` to solve
the reachability game.

.. code-block:: python

    from iglsynth.solver import ZielonkaSolver

    # Instantiate a solver
    solver = ZielonkaSolver(game=game)

    # Configure the solver to only compute winning regions, and not strategies
    solver.configure(compute_strategy_1=False, compute_strategy_1=False)

    # Run the solver
    solver.run(verbose=False)


The solution of solver can be accessed by accessing the properties.

.. code-block:: python

    win1 = solver.win1      # Winning region for player 1 (Circle)
    win2 = solver.win2      # Winning region for player 2 (Square)


For defining and solving more complex games or hypergames, refer to the ``API documentation`` and ``examples``
(to be added soon).


.. toctree::
    :caption: API Documentation
    :maxdepth: 2
    :hidden:

    Home Page <self>
    Game Module <game>
    Utilities  <util>
