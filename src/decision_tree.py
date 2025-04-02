
from game_state import ClobberGameState

class DecisionTree:
    def __init__(self, max_depth, game_state: ClobberGameState):
        self.max_depth = max_depth
        self.tree = self.crate_tree(game_state)

    def crate_tree(self, game_state):
        """
        Create a decision tree from the given game state.
        """
        self.tree = self._build_tree(game_state, depth=0)
        return self.tree

    def _build_tree(self, game_state: ClobberGameState, depth):
        """
        Recursively build the decision tree.
        """
        if self.max_depth is not None and depth >= self.max_depth:
            return None

        if game_state.is_game_over():
            return game_state.get_winner()

        possible_moves = game_state.get_possible_moves()

        tree = {}
        for move in possible_moves:
            new_game_state = game_state.make_move(move)
            tree[move] = self._build_tree(new_game_state, depth + 1)

        return tree