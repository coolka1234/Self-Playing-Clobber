from game_state import ClobberGameState


def evaluate(game_state : ClobberGameState, player):
    opponent = 'B' if player == 'W' else 'W'
    
    def is_isolated(x, y):
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(game_state.board) and 0 <= ny < len(game_state.board[0]):
                if game_state.board[nx][ny] in ('B', 'W'):
                    return False
        return True

    my_pieces = opp_pieces = my_moves = opp_moves = my_isolated = opp_isolated = 0
    for x in range(len(game_state.board)):
        for y in range(len(game_state.board[0])):
            piece = game_state.board[x][y]
            if piece == player:
                my_pieces += 1
                if is_isolated(x, y): my_isolated += 1
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(game_state.board) and 0 <= ny < len(game_state.board[0]):
                        if game_state.board[nx][ny] == opponent:
                            my_moves += 1
            elif piece == opponent:
                opp_pieces += 1
                if is_isolated(x, y): opp_isolated += 1
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(game_state.board) and 0 <= ny < len(game_state.board[0]):
                        if game_state.board[nx][ny] == player:
                            opp_moves += 1

    score = (
        10 * (my_moves - opp_moves) +
        20 * (my_pieces - opp_pieces) +
        15 * (opp_isolated - my_isolated)
    )
    return score

def mobility_score(board, player):
    opponent = 'B' if player == 'W' else 'W'
    def count_moves(p):
        moves = 0
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] == p:
                    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(board) and 0 <= ny < len(board[0]):
                            if board[nx][ny] == ('B' if p == 'W' else 'W'):
                                moves += 1
        return moves
    return count_moves(player) - count_moves(opponent)

def piece_count_score(board, player):
    opponent = 'B' if player == 'W' else 'W'
    my_count = sum(row.count(player) for row in board)
    opp_count = sum(row.count(opponent) for row in board)
    return my_count - opp_count

def isolation_score(board, player):
    opponent = 'B' if player == 'W' else 'W'
    
    def is_isolated(x, y):
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]):
                if board[nx][ny] in ('B', 'W'):
                    return False
        return True

    def count_isolated(p):
        count = 0
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] == p and is_isolated(x, y):
                    count += 1
        return count

    return count_isolated(opponent) - count_isolated(player)


def heuristic_evaluate(game_state: ClobberGameState):
    """
    Evaluate the game state for the given player.
    """
    board = game_state.board
    player = game_state.current_player
    return evaluate(board, player)
