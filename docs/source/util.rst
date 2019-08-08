Utilities
=========

.. currentmodule:: iglsynth.util


------------


Graph
-----

A graph is defined as

    :math:`G = \langle V, E, vprops, eprops, gprops \rangle`

where

* :math:`V` is a set of vertices.
* :math:`E` is a set of edges.
* :math:`vprops` are vertex properties. Each vertex property maps the set of vertices to its property value.
* :math:`eprops` are edge properties. Each edge property maps the set of edges to its property value.
* :math:`gprops` are graph properties. A graph property is like a global variable for entire graph.


The properties :math:`vprops`, :math:`eprops` and :math:`gprops` can be one of the following types.

.. data:: VALID_PROPERTY_TYPES
    :annotation: (str) = {"bool", "int", "float", "string", "object"}


The API for :class:`Graph` is as follows.

.. autoclass:: Graph
    :members:

----------

Sub-Graph
----------

Given a graph (or sub-graph) :math:`G`, a sub-graph is a graph defined using boolean properties
``vfilt`` and/or ``efilt`` over :math:`G`. The vertices :math:`v \in V` for which ``vfilt[v] = True``
are included in the sub-graph. Similarly, the edges :math:`e \in E` for which ``efilt[e] = True``
are included in the sub-graph.


.. autoclass:: SubGraph
    :members:

.. note:: :class:`SubGraph` is a derived class from :class:`Graph`. All member functions and properties of
    :class:`Graph` class apply to :class:`SubGraph`.