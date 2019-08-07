"""
iglsynth: game.py

License goes here...
"""

from iglsynth.util.graph import *
from iglsynth.game.bases import *


class Game(IGame):
    """
    Represents a deterministic two-player game. The game may be concurrent or turn-based.

    :param kind: Whether the game is concurrent or turn-based.
    :type kind: str, either :data:`CONCURRENT <iglsynth.game.game.CONCURRENT>` or
        :data:`TURN_BASED <iglsynth.game.game.TURN_BASED>`
    """

    def _validate_graph(self, graph: Graph) -> bool:
        """
        A deterministic two-player game graph must have an edge property: "act : <Int>", where the integer represents
        action-id. It must also have a vertex property: "is_final : <bool>" that marks
        whether a vertex is a final state or not.

        If game is turn-based, then graph must have vertex property: "turn : <Int>", where the integer
        represents the ID of player who will play at that vertex.

        :param graph: An :class:`Graph` object.
        """

        # Check if graph has necessary properties applicable to both turn-based and concurrent games
        if self.kind == TURN_BASED:
            if not graph.has_vertex_property(name="turn", of_type="int"):
                return False

        # Check if graph has necessary properties applicable to both turn-based and concurrent games
        if not (graph.has_vertex_property(name="is_final", of_type="bool") and
                graph.has_edge_property(name="act", of_type="int")):
            return False

        # If all properties are as expected
        return True

    def _validate_model(self, model: Kripke) -> bool:
        raise NotImplementedError("Feature yet to be implemented.")

    def _validate_player(self, p: Player) -> bool:
        raise NotImplementedError("Feature yet to be implemented.")

    def _validate_acc(self, acc: 'Acceptance') -> bool:
        raise NotImplementedError("Feature yet to be implemented.")

    def _define_by_model(self, model: Kripke, acc1: 'Acceptance', acc2: 'Acceptance' = None):
        raise NotImplementedError("Feature yet to be implemented.")

    def _define_by_player(self, p1: Player, p2: Player, acc1: 'Acceptance',
                          rp: 'Distribution' = None, acc2: 'Acceptance' = None):
        raise NotImplementedError("Feature yet to be implemented.")

    def _define_by_graph(self, graph: 'Graph'):
        """
        Configures the game using a graph provided by user.

        :param graph: An :class:`Graph` object satisfying necessary constraints.

        .. note:: The graph is assumed to satisfy the requirements of a deterministic two-player game.
        """
        self._p1 = None
        self._p2 = None
        self._model = None
        self._acc = None
        self._graph = graph

    def define(self, graph: Graph = None, model: Kripke = None, p1: Player = None, p2: Player = None,
               rp: 'Distribution' = None, acc1: 'Acceptance' = None, acc2: 'Acceptance' = None):
        """
        Define a two-player zero-sum game with given parameters.
        The instantiation checks for the following patterns, in order:

        1. ``game.define(graph=<Graph>)``
        2. ``game.define(model=<TSys>, acc1=<Acceptance>)``
        3. ``game.define(p1=<Player>, p2=<Player>, acc1=<Acceptance>)``

        :param graph: Graph object representing game.
        :type graph: :class:`Graph <iglsynth.util.Graph>`

        :param model: A Kripke structure.
        :type model: :class:`TSys`

        :param p1: Player 1 profile.
        :type p1: :class:`Player`

        :param p2: Player 1 profile.
        :type p2: :class:`Player`

        :param acc1: Winning condition of player 1.
        :type acc1: :class:`Acceptance`

        .. caution:: Currently, only instantiation using ``graph`` is implemented.
        """

        # Case 1: Definition by graph
        if graph is not None:
            if self._validate_graph(graph):
                self._define_by_graph(graph)
            else:
                raise AttributeError("Game could not be defined using provided 'graph'. Validation failed.")

        # Case 2: Definition by model and winning condition
        elif model is not None and acc1 is not None:
            raise NotImplementedError("Feature yet to be implemented.")
            # if self._validate_model(model) and self._validate_acc(acc1):
            #     self._define_by_model(model, acc1)
            # else:
            #     raise AttributeError("Game could not be defined using provided 'model', 'acc1'. Validation failed.")

        # Case 2: Definition by player profiles and winning condition
        elif p1 is not None and p2 is not None and acc1 is not None:
            raise NotImplementedError("Feature yet to be implemented.")

            # if self._validate_player(p1) and self._validate_player(p2) and self._validate_acc(acc1):
            #     self._define_by_player(p1, p2, acc1)
            # else:
            #     raise AttributeError("Game could not be defined using provided 'p1', 'p2', 'acc1'. Validation failed.")

        # Case else:
        else:
            raise AttributeError('Game cannot be defined using given parameters. See docs for acceptable definitions.')

    def construct(self, model_product: Callable = None, game_product: Callable = None):
        """
        Yet to be implemented...

        :param model_product:
        :param game_product:
        :return:
        """
        raise NotImplementedError("Feature yet to be implemented.")

