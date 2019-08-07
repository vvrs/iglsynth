from iglsynth.solver.solver import *
from iglsynth.util.graph import *


class ZielonkaSolver(Solver):
    """
    Implements Zielonka's attractor computation algorithm.
    """
    def __init__(self, game: IGame):
        super(ZielonkaSolver, self).__init__(game)

        # Initialize internal variables
        self._attr = None
        self._compute_win1 = True
        self._compute_win2 = True

    @property
    def win1(self):
        return self._attr.get_vertex_property(name="win1")

    def _validate_game(self, game: IGame) -> bool:
        if game.graph.has_vertex_property(name="is_final") and game.graph.has_vertex_property(name="turn"):
            return True

        return False

    def configure(self, win1=True, win2=True):
        """
        Set configuration parameters for solver.

        :param win1: Should winning region for player 1 be computed? Default: True.
        :param win2: Should winning region for player 1 be computed? Default: True.

        .. todo:: Add following params - (compute_strategy_1, compute_strategy_2, loss_strategy_1, loss_strategy_2,
            type_strategy_1, type_strategy_2)
        """
        self._compute_win1 = win1
        self._compute_win2 = win2

    def _pre1(self, win):
        pre1 = set()

        for v in win:
            in_neighbors = set(self.game.graph.in_neighbors(vid=v))
            new_states = in_neighbors - win
            for nv in new_states:
                if self.game.graph.get_vertex_property(name="turn", vid=nv) == 1:
                    self._attr.set_vertex_property(name="win1", vid=nv, value=True)
                    pre1.add(nv)

        return pre1

    def _pre2(self, win):
        pre2 = set()

        for v in win:
            in_neighbors = set(self.game.graph.in_neighbors(vid=v))
            new_states = in_neighbors - win
            for nv in new_states:
                if self.game.graph.get_vertex_property(name="turn", vid=nv) == 2:
                    out_neighbors = set(self.game.graph.out_neighbors(vid=nv))
                    if out_neighbors.issubset(win):
                        self._attr.set_vertex_property(name="win1", vid=nv, value=True)
                        pre2.add(nv)

        return pre2

    def _zielonka(self):
        # Extract final states
        final = set()
        for v in self.game.graph.vertices:
            if self.game.graph.get_vertex_property(name="is_final", vid=v):
                self._attr.set_vertex_property(name="win1", vid=v, value=True)
                final.add(v)

        # Iteratively mark the vertices winning or losing.
        win = final.copy()
        while True:
            pre1 = self._pre1(win)
            pre2 = self._pre2(win)
            new_win = set.union(win, pre1, pre2)

            if new_win == win:
                break

            win = new_win

        print(win)

    def solve(self):
        """
        .. note:: We are not implementing strategy computation, which requires edge filters and
            attractor graph computation.
        """
        # Check if game graph is available.
        if self.game.graph is not None:
            self._attr = SubGraph(graph=self.game.graph, vfilt_name="win1")
            self._zielonka()

        # If not, then we will need to construct based on configuration of game.
        else:
            raise NotImplementedError("Presently only solver for a game defined by graph is implemented.")
