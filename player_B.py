from multiprocessing.connection import Listener, Client
import sys
sys.path.append("src")
from src.game import ClobberAgent
from src.game_state import ClobberGameState
from src.heuristics import evaluate, mobility_score, piece_count_score, isolation_score
import datetime


def play_and_listen(heuristic, strategy, max_depth, initial_game_state):
    """
    Listen for incoming connections and play a game of Clobber.
    """

    address = ('localhost', 6000)
    listener = Listener(address, authkey=b'secret')
    agent= ClobberAgent(name="B", initial_game_state=initial_game_state, heuristic=heuristic, strategy=strategy, max_depth=max_depth, adaptive=True)

    print("Listening for connections...")
    num_of_moves = 1
    conn = listener.accept()
    times_start= datetime.datetime.now()
    while True:
        try:
            move = conn.recv()
            if move:
                move=agent.play(move)
                num_of_moves += 1
                if not move:
                    print("Game Over")
                    print("Total moves played: ", num_of_moves)
                    print("Winner: B")
                    print("Time taken : ", datetime.datetime.now()-times_start)
                    conn.close()
                    listener.close()
                    break
            else:
                conn.close()
                listener.close()
                print(f"Time taken : {datetime.datetime.now()-times_start}")
                break
            conn.send(move)
        except EOFError:
            print("Connection closed")
            break
        except Exception as e:
            print("An error occurred:", e)
            break

if __name__ == "__main__":
    rows = 8
    cols = 8
    heuristic_W = mobility_score
    # alpha-beta or minmax
    strategy_A = 'minmax'
    max_depth_A = 2
    initial_game_state = ClobberGameState(rows, cols)

    play_and_listen(heuristic_W,strategy_A, max_depth_A,  initial_game_state)
