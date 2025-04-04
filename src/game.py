from game_state import ClobberGameState
from heuristics import evaluate
from decision_tree import DecisionTree
class ClobberAgent:
    def __init__(self, name, initial_game_state, heuristic, strategy='minmax',max_depth=None):
        self.name = name
        self.game_state = initial_game_state
        self.heuristic = heuristic
        self.strategy = strategy
        self.max_depth = max_depth

    def play(self, game):
        

