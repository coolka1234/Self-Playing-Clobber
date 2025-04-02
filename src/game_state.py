import numpy as np

class ClobberGameState:
    def __inti__(self, rows, cols):
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
                            if self.board[new_r, new_c] == 'B':
                                moves.append(((r, c), (new_r, new_c)))
        return moves
    
    def make_move(self, move):
        """
        Make a move on the board.
        """
        (start_r, start_c), (end_r, end_c) = move
        self.board[end_r, end_c] = self.current_player
        self.board[start_r, start_c] = 'B'
        self.current_player = 'B' if self.current_player == 'W' else 'W'
    
    def is_game_over(self):
        """
        Check if the game is over.
        """
        return self.get_possible_moves() == []