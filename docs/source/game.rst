Game Module
===========

.. currentmodule:: iglsynth.game.game

------------

Global Variables
----------------

.. data:: CONCURRENT
    :annotation: = "Concurrent"

.. data:: TURN_BASED
    :annotation: = "Turn-based"

-----------------

Deterministic Game
------------------

A deterministic two-player game is defined as the graph

    :math:`{\cal G} = \langle V, E, vprops, eprops, gprops \rangle`

where

* :math:`V` is a set of vertices.
* :math:`E` is a set of edges.
* :math:`vprops` are vertex properties.

    * Vertex properties must include ``is_final`` of type ``bool``.
    * When :math:`\cal G` is turn-based, vertex properties must include ``turn`` of type ``int``.

* :math:`eprops` are edge properties.

    * Edge properties must include ``act`` of type ``int``.

* :math:`gprops` are graph properties.

    * Graph property ``kind`` represents whether the game is Concurrent or Turn-based.

|

.. autoclass:: Game
    :members: define, kind, graph
