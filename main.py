import sys
sys.path.append("src")
from src.game import ClobberAgent
from src.game_state import ClobberGameState
from src.heuristics import evaluate, mobility_score, piece_count_score, isolation_score

if __name__ == "__main__":
    initial_game_state = ClobberGameState(10, 10)
    agent = ClobberAgent(name="W", initial_game_state=initial_game_state, heuristic=evaluate, strategy='minmax', max_depth=3)
    agent2 = ClobberAgent(name="B", initial_game_state=initial_game_state, heuristic=evaluate, strategy='minmax', max_depth=3)
    num_of_moves = 1
    print("Starting game...")
    move=agent.play(initial_game_state)
    while move:
        num_of_moves += 1
        move=agent2.play(move)
        if move:
            move=agent.play(move)
        else:
            break
    print("Game Over")
    print(f"Total moves played: {num_of_moves}")