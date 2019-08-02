# Getting Started with IGLSynth



`iglsynth` primarily deals with games or hypergames defined on graphs. It is divided in 4 modules, namely

* `util`: defines the common data structures and utility functions required by various modules in `iglsynth`
* `game`: defines the classes used to define games or hypergames on graph. 
* `logic`: defines different logic families, acceptance conditions and automata.
* `solver`: define solvers for different games or hypergames. 



## Graphs

A graph is defined as $G = \langle V, E, vprops, eprops, gprops \rangle$, where $<v/ e/g>props$  represent the vertex, edge and graph properties. For various games, hypergames throughout `iglsynth` the graphs are implemented as `util.graph.Graph` objects. 





