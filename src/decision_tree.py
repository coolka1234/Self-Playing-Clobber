import numpy as np
from game_state import ClobberGameState
from heuristics import evaluate, mobility_score, piece_count_score, isolation_score
class DecisionTree:
    def __init__(self, max_depth, game_state: ClobberGameState, heuristic, strategy='minmax', player=None):
        """
        Initialize the decision tree with the game state and strategy.
        """
        self.max_depth = max_depth
        self.tree = self.crate_tree(game_state)
        self.strategy = strategy
        self.heuristic = heuristic
        self.player = player


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
        best_move_so_far = None
        if self.strategy == 'minmax':
            for move in game_state.get_possible_moves():
                new_game_state = game_state.make_move(move)
                move_value = self.minimax_search(new_game_state, self.max_depth, True)
                if best_move_so_far is None or move_value > best_move_so_far[1]:
                    best_move_so_far = (move, move_value)
        elif self.strategy == 'alpha-beta':
            best_move_so_far = (None, float('-inf'))
            for move in game_state.get_possible_moves():
                new_game_state = game_state.make_move(move)
                move_value = self.alfa_beta_search(new_game_state, self.max_depth, float('-inf'), float('inf'), True)
                if move_value > best_move_so_far[1]:
                    best_move_so_far = (move, move_value)
        return best_move_so_far[0] if best_move_so_far else None
    
    def minimax_search(self, game_state: ClobberGameState, depth, maximizing_player):
        """
        Perform a minimax search on the game state.
        game_state: ClobberGameState
        depth: Depth of the search
        maximizing_player: Boolean indicating if it's the maximizing player's turn        
        """
        if depth == 0 or game_state.is_game_over():
            return self.heuristic(game_state, self.player)

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
            return self.heuristic(game_state, self.player)

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
    
    def analyze_and_change_heuristic(self, game_state: ClobberGameState):
        """
        Analyze the game state and change the heuristic based on the analysis.
        Choose the most appropriate heuristic based on the current game state.
        """
        mobility = mobility_score(game_state, self.player)
        piece_count = piece_count_score(game_state, self.player)
        isolation = isolation_score(game_state, self.player)
        
        total_pieces = game_state.get_piece_count(1) + game_state.get_piece_count(2)
        max_pieces = game_state.cols * game_state.rows
        game_progress = 1 - (total_pieces / max_pieces)  # game progress from 0 to 1
        
        epsilon = 1e-10
        scores = {
            "mobility": abs(mobility),
            "piece_count": abs(piece_count),
            "isolation": abs(isolation)
        }
        
        max_score = max(scores.values()) + epsilon
        normalized_scores = {k: v/max_score for k, v in scores.items()}
        
        if game_progress < 0.3:  # Early game
            weights = {"mobility": 0.7, "piece_count": 0.2, "isolation": 0.1}
        elif game_progress < 0.7:  # Mid game
            weights = {"mobility": 0.4, "piece_count": 0.4, "isolation": 0.2}
        else:  # Lategame
            weights = {"mobility": 0.2, "piece_count": 0.3, "isolation": 0.5}
        
        weighted_scores = {
            "mobility": normalized_scores["mobility"] * weights["mobility"],
            "piece_count": normalized_scores["piece_count"] * weights["piece_count"],
            "isolation": normalized_scores["isolation"] * weights["isolation"]
        }
        
        best_heuristic_name = max(weighted_scores, key=weighted_scores.get)
        
        heuristic_map = {
            "mobility": mobility_score,
            "piece_count": piece_count_score,
            "isolation": isolation_score
        }
        
        new_heuristic = heuristic_map[best_heuristic_name]
        
        if self.heuristic.__code__ != new_heuristic.__code__:
            old_heuristic_name = next((name for name, func in heuristic_map.items() 
                                      if func.__code__ == self.heuristic.__code__), "unknown")
            
            print(f"Game progress: {game_progress:.2f} (Phase: {'early' if game_progress < 0.3 else 'mid' if game_progress < 0.7 else 'late'})")
            print(f"Raw scores: Mobility={mobility:.2f}, Piece Count={piece_count:.2f}, Isolation={isolation:.2f}")
            print(f"Normalized scores: {', '.join([f'{k}={v:.2f}' for k, v in normalized_scores.items()])}")
            print(f"Weighted scores: {', '.join([f'{k}={v:.2f}' for k, v in weighted_scores.items()])}")
            print(f"Changing heuristic from {old_heuristic_name} to {best_heuristic_name}")
            
            self.heuristic = new_heuristic
            return True
        
        return False