import abc
from typing import Callable

CONCURRENT = "Concurrent"
TURN_BASED = "Turn-based"


class IGame(abc.ABC):
    # ------------------------------------------------------------------------------------------------------------------
    # INTERNAL CLASSES
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, kind=CONCURRENT):
        """
        Create a new instance of game on graph.
        :param kind: Type of game, whether :data:`CONCURRENT` or :data:`TURN_BASED`.
        """
        self._kind = kind
        self._p1 = None
        self._p2 = None
        self._model = None
        self._acc = None
        self._graph = None

    # ------------------------------------------------------------------------------------------------------------------
    # PROPERTIES
    # ------------------------------------------------------------------------------------------------------------------
    @property
    def kind(self):
        """ Returns the whether the game is turn-based or concurrent. """
        return self._kind

    @property
    def p1(self):
        """ Returns the player 1 object. """
        return self._p1

    @property
    def p2(self):
        """ Returns the player 1 object. """
        return self._p2

    @property
    def model(self):
        """ Returns the Kripke model of the interaction. """
        return self._model

    @property
    def acc(self):
        return self._acc

    @property
    def graph(self):
        """ Returns the game graph. """
        return self._graph

    # ------------------------------------------------------------------------------------------------------------------
    # PRIVATE FUNCTIONS (ABSTRACT)
    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _validate_graph(self, graph: 'Graph') -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _validate_model(self, model: 'Kripke'):
        raise NotImplementedError

    @abc.abstractmethod
    def _validate_player(self, p: 'Player'):
        raise NotImplementedError

    @abc.abstractmethod
    def _validate_acc(self, acc: 'Acceptance'):
        raise NotImplementedError

    @abc.abstractmethod
    def _define_by_model(self, model: 'Kripke', acc1: 'Acceptance', acc2: 'Acceptance' = None):
        raise NotImplementedError

    @abc.abstractmethod
    def _define_by_player(self, p1: 'Player', p2: 'Player', acc1: 'Acceptance',
                          rp: 'Distribution' = None, acc2: 'Acceptance' = None):
        raise NotImplementedError

    @abc.abstractmethod
    def _define_by_graph(self, graph: 'Graph'):
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC FUNCTIONS (ABSTRACT)
    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def define(self, graph: 'Graph' = None, model: 'TSys' = None, p1: 'Player' = None, p2: 'Player' = None,
               rp: 'Distribution' = None, acc1: 'Acceptance' = None, acc2: 'Acceptance' = None):
        """
        Define the game parameters. The instantiation checks for the following patterns, in order:
        #. game.define(graph=<Graph>) -- all other params will be ignored.
        #. game.define(model=<TSys>, acc1=<Acceptance>, acc2=<Acceptance>)
        #. game.define(model=<TSys>, acc1=<Acceptance>)
        #. game.define(p1=<Player>, p2=<Player>, rp=<Distribution>, acc1=<Acceptance>, acc2=<Acceptance>)
        #. game.define(p1=<Player>, p2=<Player>, rp=<Distribution>, acc1=<Acceptance>)
        #. game.define(p1=<Player>, p2=<Player>, acc1=<Acceptance>, acc2=<Acceptance>)
        #. game.define(p1=<Player>, p2=<Player>, acc1=<Acceptance>)

        :param graph: Graph object representing game.
        :type graph: :class:`Graph`

        :param model: A Kripke structure.
        :type model: :class:`TSys`

        :param p1: Player 1 profile.
        :type p1: :class:`Player`

        :param p2: Player 1 profile.
        :type p2: :class:`Player`

        :param rp: A distribution representing a random player.
        :type rp: :class:`Distribution`

        :param acc1: Winning condition of player 1.
        :type acc1: :class:`Acceptance`

        :param acc2: Winning condition of player 1.
        :type acc2: :class:`Acceptance`
        """
        raise NotImplementedError

    @abc.abstractmethod
    def construct(self, model_product: Callable = None, game_product: Callable = None):
        """
        Constructs the game graph. If necessary, first constructs the model graph, then the game graph.

        :param model_product: If provided and applicable, this function will be used to compute product of player graphs
            to compute a transition system graph.
        :type: Callable.

        :param game_product: If provided and applicable, this function will be used to compute product of transition
            system graph and automaton defined by acceptance condition to compute product game graph.
        :type: Callable.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    # PUBLIC FUNCTIONS (IMPLEMENTED)
    # ------------------------------------------------------------------------------------------------------------------
    def save(self, filename: str, save_graphs: bool = True):
        pass

    def load(self, filename: str, load_graphs: bool = True):
        pass


class Kripke(abc.ABC):
    pass


class Player(object):
    pass


