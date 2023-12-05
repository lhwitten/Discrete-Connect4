"""
Implementation of Connect 4 game.
"""
from copy import deepcopy
import numpy as np
from game_setup import GameSetup

class ConnectState:
    """
    Create a Connect 4 board and set rules.
    
    Attributes:
        board: a matrix with the dimesions of the Connect 4 board.
        to_play: the player whoever's turn it is to play.
        height: the height of each column of the board.
        last_played: the last move played in the game.
    
    """
    def __init__(self):
        """
        Initialize attributes of the ConnectState class.
        """
        self.board = [[0] * GameSetup.COLS for _ in range(GameSetup.ROWS)]
        self.to_play = GameSetup.PLAYERS['one']
        self.height = [GameSetup.ROWS - 1] * GameSetup.COLS
        self.last_played = []
    
    def get_board(self):
        """
        Get the Connect 4 board.

        Returns:
            A matrix representing the copy of the board.
        """
        return deepcopy(self.board)
    
    def move(self, col):
        """
        Make a move in the specified column. The column will be updated with
        the player's mark, and then the height of the column will be updated
        accordingly.

        Args:
            col: an integer representing a column on the board.
        """
        self.board[self.height[col]][col] = self.to_play
        self.last_played = [self.height[col], col]
        self.height[col] -= 1
        self.to_play = GameSetup.PLAYERS['two'] if self.to_play == GameSetup.PLAYERS['one'] else GameSetup.PLAYERS['one']
        
    def get_legal_moves(self):
        """
        Get the legal moves that could be made. A legal move is defined as a 
        column where a new piece could be placed. 

        Returns:
            A list of legal moves.
        """
        return [col for col in range(GameSetup.COLS) if self.board[0][col] == 0]
    
    def check_win(self):
        """
        Check for a win. 

        Returns:
            The player who won. 
        """
        if len(self.last_played) > 0 and self.check_win_from(self.last_played[0], self.last_played[1]):
            return self.board[self.last_played[0]][self.last_played[1]]
        
        return 0

    
    def check_win_from(self, row, col):
        """
        Check for a win from a given row and column.

        Args:
            row: an integer representing a row on the board.
            col: an integer representing a column on the board.
        """
        player = self.board[row][col]
        
        # Check horizontal locations for win
        for c in range(GameSetup.COLS-3):
            for r in range(GameSetup.ROWS):
                if self.board[r][c] == player and self.board[r][c+1] == player and self.board[r][c+2] == player and self.board[r][c+3] == player:
                    return True
    
        # Check vertical locations for win
        for c in range(GameSetup.COLS):
            for r in range(GameSetup.ROWS-3):
                if self.board[r][c] == player and self.board[r+1][c] == player and self.board[r+2][c] == player and self.board[r+3][c] == player:
                    return True
    
        # Check positively sloped diaganols
        for c in range(GameSetup.COLS-3):
            for r in range(GameSetup.ROWS-3):
                if self.board[r][c] == player and self.board[r+1][c+1] == player and self.board[r+2][c+2] == player and self.board[r+3][c+3] == player:
                    return True
    
        # Check negatively sloped diaganols
        for c in range(GameSetup.COLS-3):
            for r in range(3, GameSetup.ROWS):
                if self.board[r][c] == player and self.board[r-1][c+1] == player and self.board[r-2][c+2] == player and self.board[r-3][c+3] == player:
                    return True
    
    def game_over(self):
        """
        Check if the game is over. The game is over if there are no legal moves
        remaining or if there is a win.

        Returns:
            A boolean representing if the game is over or not.
        """
        return self.check_win() or len(self.get_legal_moves()) == 0
    
    def get_outcome(self):
        """
        Get the outcome of the game. 

        Returns:
            The outcome of the game (win, loss, or draw).
        """
        if len(self.get_legal_moves()) == 0 and self.check_win() == 0:
            return GameSetup.OUTCOMES['draw']
        
        return GameSetup.OUTCOMES['one'] if self.check_win() == GameSetup.PLAYERS['one'] else GameSetup.PLAYERS['two']
    
    def print(self):
        print('================================')
        print("  0   1   2   3   4   5   6")
        for row in range(GameSetup.ROWS):
            for col in range(GameSetup.COLS):
                print("| {} ".format("X" if self.board[row][col] == 1 else "0" if self.board[row][col] == 2 else " "), end = "")
            print("|")
        
print('================================')