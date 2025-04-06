import sys
sys.path.append("src")
from src.game import ClobberAgent
from src.game_state import ClobberGameState
from src.heuristics import evaluate, mobility_score, piece_count_score, isolation_score

def simulate_game(heuristic_W, heuristic_B, strategy_A, strategy_B, max_depth_A, max_depth_B, rows, cols):
    """
    Simulate a game of Clobber between two agents.
    """
    initial_game_state = ClobberGameState(rows,cols)
    agent = ClobberAgent(name="W", initial_game_state=initial_game_state, heuristic=heuristic_W, strategy=strategy_A, max_depth=max_depth_A)
    agent2 = ClobberAgent(name="B", initial_game_state=initial_game_state, heuristic=heuristic_B, strategy=strategy_B, max_depth=max_depth_B)
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


if __name__ == "__main__":
    rows = 8
    cols = 8
    heuristic_W = isolation_score
    heuristic_B = mobility_score
    # alpha-beta or minmax
    strategy_A = 'alpha-beta'
    strategy_B = 'alpha-beta'
    max_depth_A = 10
    max_depth_B = 10

    simulate_game(heuristic_W, heuristic_B, strategy_A, strategy_B, max_depth_A, max_depth_B, rows, cols)