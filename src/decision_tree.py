import copy
import sys
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
        self.num_of_visits = 0
        self.heuristic_cache = {}  

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

        possible_moves = game_state.get_possible_moves(print_moves=False)

        tree = {}
        for move in possible_moves:
            copied_game_state = copy.deepcopy(game_state)
            new_game_state = copied_game_state.make_move(move)
            tree[move] = self._build_tree(copy.deepcopy(new_game_state), depth + 1)

        return tree
    
    def get_best_move(self, game_state: ClobberGameState):
        """
        Get the best move for the current player using the heuristic.
        """
        best_move_so_far = None
        if self.strategy == 'minmax':
            best_move_so_far = (None, float('-inf'))
            for move in game_state.get_possible_moves():
                temp_game_state = copy.deepcopy(game_state)
                temp_game_state.make_move(move)
                
                move_value = self.minimax_search(temp_game_state, self.max_depth - 1, False)
                
                if move_value > best_move_so_far[1]:
                    best_move_so_far = (move, move_value)
        elif self.strategy == 'alpha-beta':
            best_move_so_far = (None, float('-inf'))
            for move in game_state.get_possible_moves():
                temp_game_state = copy.deepcopy(game_state)
                temp_game_state.make_move(move)
                
                move_value = self.alfa_beta_search(temp_game_state, self.max_depth - 1, float('-inf'), float('inf'), False)
                
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
        state_key = (str(game_state.board), depth, maximizing_player)
        if state_key in self.heuristic_cache:
            return self.heuristic_cache[state_key]
            
        if depth == 0 or game_state.is_game_over():
            result = self.heuristic(game_state, self.player)
            self.heuristic_cache[state_key] = result
            return result

        possible_moves = game_state.get_possible_moves()
        if not possible_moves:  
            result = self.heuristic(game_state, self.player)
            self.heuristic_cache[state_key] = result
            return result

        if maximizing_player:
            max_eval = float('-inf')
            for move in possible_moves:
                self.num_of_visits += 1
                
                temp_game_state = copy.deepcopy(game_state)
                temp_game_state.make_move(move)
                
                eval_value = self.minimax_search(temp_game_state, depth - 1, False)
                max_eval = max(max_eval, eval_value)
            
            self.heuristic_cache[state_key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                self.num_of_visits += 1
                
                temp_game_state = copy.deepcopy(game_state)
                temp_game_state.make_move(move)
                
                eval_value = self.minimax_search(temp_game_state, depth - 1, True)
                min_eval = min(min_eval, eval_value)
            
            self.heuristic_cache[state_key] = min_eval
            return min_eval
    
    def alfa_beta_search(self, game_state: ClobberGameState, depth, alpha, beta, maximizing_player):
        """
        Perform an alpha-beta search on the game state.
        """
        state_key = (str(game_state.board), depth, maximizing_player)
        if state_key in self.heuristic_cache:
            return self.heuristic_cache[state_key]
            
        if depth == 0 or game_state.is_game_over():
            result = self.heuristic(game_state, self.player)
            self.heuristic_cache[state_key] = result
            return result

        possible_moves = game_state.get_possible_moves(print_moves=False)
        if not possible_moves:  
            result = self.heuristic(game_state, self.player)
            self.heuristic_cache[state_key] = result
            return result

        if maximizing_player:
            max_eval = float('-inf')
            for move in possible_moves:
                self.num_of_visits += 1
                
                temp_game_state = copy.deepcopy(game_state)
                temp_game_state.make_move(move)
                
                eval_value = self.alfa_beta_search(temp_game_state, depth - 1, alpha, beta, False)
                
                max_eval = max(max_eval, eval_value)
                alpha = max(alpha, eval_value)
                if beta <= alpha:
                    break
            
            self.heuristic_cache[state_key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                self.num_of_visits += 1
                
                temp_game_state = copy.deepcopy(game_state)
                temp_game_state.make_move(move)
                
                eval_value = self.alfa_beta_search(temp_game_state, depth - 1, alpha, beta, True)
                
                min_eval = min(min_eval, eval_value)
                beta = min(beta, eval_value)
                if beta <= alpha:
                    break
            
            self.heuristic_cache[state_key] = min_eval
            return min_eval
    
    def analyze_and_change_heuristic(self, game_state: ClobberGameState):
        """
        Analyze the game state and change the heuristic based on the analysis.
        Choose the most appropriate heuristic based on the current game state.
        """
        mobility = mobility_score(game_state, self.player)
        piece_count = piece_count_score(game_state, self.player)
        isolation = isolation_score(game_state, self.player)
        
        total_pieces = game_state.get_num_of_pieces('W') + game_state.get_num_of_pieces('B')
        max_pieces = game_state.cols * game_state.rows
        game_progress = 1 - (total_pieces / max_pieces) 
        
        epsilon = 1e-10
        scores = {
            "mobility": abs(mobility),
            "piece_count": abs(piece_count),
            "isolation": abs(isolation)
        }
        
        max_score = max(scores.values()) + epsilon
        normalized_scores = {k: v/max_score for k, v in scores.items()}
        
        if game_progress < 0.3: 
            weights = {"mobility": 0.7, "piece_count": 0.2, "isolation": 0.1}
        elif game_progress < 0.7:
            weights = {"mobility": 0.4, "piece_count": 0.4, "isolation": 0.2}
        else: 
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
            
            return new_heuristic
        return None