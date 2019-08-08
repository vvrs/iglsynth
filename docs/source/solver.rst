Solver Module
=============

.. currentmodule:: iglsynth.solver


----


ZielonkaSolver
--------------

Zielonka solver implements Zielonka's attractor computation algorithm to solve a deterministic two player turn-based
zero-sum game. It inputs a :class:`Game <iglsynth.game.game.Game>` object. It can generate the following outputs,

1. Winning region for player 1
2. Winning region for player 2
3. Winning strategy for player 1: Deterministic/Stochastic
4. Winning strategy for player 2: Deterministic/Stochastic


.. autoclass:: ZielonkaSolver
    :members: configure, win1, win2, run


