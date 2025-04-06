import copy
from game_state import ClobberGameState
from heuristics import evaluate
from decision_tree import DecisionTree
class ClobberAgent:
    def __init__(self, name, initial_game_state, heuristic, strategy='minmax',max_depth=None, adaptive=False):
        self.name = name
        self.game_state = initial_game_state
        self.heuristic = heuristic
        self.strategy = strategy
        self.max_depth = max_depth
        self.adaptive = adaptive

    def play(self, game: ClobberGameState):
        """
        Play a move using the decision tree strategy.
        """
        print(f"{self.name} is playing...")
        print(f"Current board:\n{game.board}")
        print(f"Current player: {game.current_player}")
        print(f"Possible moves: {game.get_possible_moves()}")
        print(f"Evaluating moves using {self.strategy} strategy...")
        dt=DecisionTree(self.max_depth, copy.deepcopy(game), self.heuristic, self.strategy, self.name)
        if self.adaptive:
            potential_new_heuristic = dt.analyze_and_change_heuristic(copy.deepcopy(game))
            self.heuristic= potential_new_heuristic if potential_new_heuristic else self.heuristic
        best_move = dt.get_best_move(copy.deepcopy(game))
        if best_move:
            game.make_move(best_move)
            print(f"{self.name} played move {best_move}")
        else:
            print(f"{self.name} has no valid moves. Game over.")
        winner = game.check_winner()
        if winner:
            print(f"Winner: {winner}")
            print(f"Final board:\n{game.board}")
            return None
        else:
            print("No winner yet.")
        return game



