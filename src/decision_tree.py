import numpy as np
from game_state import ClobberGameState
from heuristics import evaluate, mobility_score, piece_count_score, isolation_score
class DecisionTree:
    def __init__(self, max_depth, game_state: ClobberGameState, heuristic, strategy='minmax'):
        """
        Initialize the decision tree with the game state and strategy.
        """
        self.max_depth = max_depth
        self.tree = self.crate_tree(game_state)
        self.strategy = strategy
        self.heuristic = heuristic


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
            return game_state.check_winner()

        possible_moves = game_state.get_possible_moves()

        tree = {}
        for move in possible_moves:
            new_game_state = game_state.make_move(move)
            tree[move] = self._build_tree(new_game_state, depth + 1)

        return tree
    
    def get_best_move(self, game_state: ClobberGameState):
        """
        Get the best move for the current player using the heuristic.
        """
        best_move = None
        best_value = float('-inf')

        possible_moves = game_state.get_possible_moves()

        for move in possible_moves:
            new_game_state = game_state.make_move(move)
            value = self.heuristic(new_game_state)

            if value > best_value:
                best_value = value
                best_move = move

        return best_move
    
    def minimax_search(self, game_state: ClobberGameState, depth, maximizing_player):
        """
        Perform a minimax search on the game state.
        """
        if depth == 0 or game_state.is_game_over():
            return self.heuristic(game_state)

        possible_moves = game_state.get_possible_moves()

        if maximizing_player:
            max_eval = float('-inf')
            for move in possible_moves:
                new_game_state = game_state.make_move(move)
                eval = self.minimax_search(new_game_state, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                new_game_state = game_state.make_move(move)
                eval = self.minimax_search(new_game_state, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval
    

    
    def alfa_beta_search(self, game_state: ClobberGameState, depth, alpha, beta, maximizing_player):
        """
        Perform an alpha-beta search on the game state.
        """
        if depth == 0 or game_state.is_game_over():
            return self.evaluate(game_state)

        possible_moves = game_state.get_possible_moves()

        if maximizing_player:
            max_eval = float('-inf')
            for move in possible_moves:
                new_game_state = game_state.make_move(move)
                eval = self.alfa_beta_search(new_game_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                new_game_state = game_state.make_move(move)
                eval = self.alfa_beta_search(new_game_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval    