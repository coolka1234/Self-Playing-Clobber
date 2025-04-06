import numpy as np

class ClobberGameState:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = self.create_clobber_board(rows, cols)
        self.current_player = 'W'

    def create_clobber_board(self, rows, cols):
        board = np.empty((rows, cols), dtype=str)
        for r in range(rows):
            for c in range(cols):
                board[r, c] = 'W' if (r + c) % 2 == 0 else 'B'
        return board
    
    def get_possible_moves(self):
        """
        Get all possible moves for the current player.
        """
        moves = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r, c] == self.current_player:
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        new_r, new_c = r + dr, c + dc
                        if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                            if self.board[new_r, new_c] != self.current_player and self.board[new_r, new_c] != '_':
                                moves.append(((r, c), (new_r, new_c)))
        return moves
    
    def make_move(self, move):
        """
        Make a move on the board.
        """
        (start_r, start_c), (end_r, end_c) = move
        self.board[end_r, end_c] = self.current_player
        self.board[start_r, start_c] = '_'
        self.current_player = 'B' if self.current_player == 'W' else 'W'
        return self
    
    def is_game_over(self):
        """
        Check if the game is over.
        """
        return self.get_possible_moves() == []
    
    def check_winner(self):
        if self.is_game_over():
            # def has_moves(player):
            #     opponent = 'B' if player == 'W' else 'W'
            #     for x in range(len(self.board)):
            #         for y in range(len(self.board[0])):
            #             if self.board[x][y] == player:
            #                 for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            #                     nx, ny = x + dx, y + dy
            #                     if 0 <= nx < len(self.board) and 0 <= ny < len(self.board[0]):
            #                         if self.board[nx][ny] == opponent:
            #                             return True
            #     return False

            # white_can_move = has_moves('W')
            # black_can_move = has_moves('B')

            # if white_can_move and not black_can_move:
            #     return 'W'
            # elif black_can_move and not white_can_move:
            #     return 'B'
            # # should not happen in a well-formed game
            # elif not white_can_move and not black_can_move:
            #     return 'Draw'
            # else:
            #     return None 
            if self.current_player == 'W':
                return 'B'
            else:
                return 'W'
        return None
