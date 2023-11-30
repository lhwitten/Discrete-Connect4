from copy import deepcopy
import numpy as np
from game_rules import GameSetup

class ConnectState:
    def __init__(self):
        self.board = [[0] * GameSetup.COLS for _ in range(GameSetup.ROWS)]
        self.to_play = GameSetup.PLAYERS['one']
        self.height = [GameSetup.ROWS - 1] * GameSetup.COLS
        self.last_played = []
    
    def get_board(self):
        return deepcopy(self.board)
    
    def move(self, col):
        self.board[self.height[col]][col] = self.to_play
        self.last_played = [self.height[col], col]
        self.height[col] -= 1
        self.to_play = GameSetup.PLAYERS['two'] if self.to_play == GameSetup.PLAYERS['one'] else GameSetup.PLAYERS['one']

    def get_legal_moves(self):
        return [col for col in range(GameSetup.COLS) if self.board[0][col] == 0]
    
    def check_win(self):
        if len(self.last_played) > 0 and self.check_win_from(self.last_played[0], self.last_played[1]):
            return self.board[self.last_played[0]][self.last_played[1]]
        
        return 0

    def check_win_from(self, row, col):
        player = self.board[row][col]


        consecutive = 1

        # Check horizontal

        temp_row = row

        while temp_row + 1 < GameSetup.ROWS and self.board[temp_rows + 1][col] == player:
            consecutive += 1
            temp_row += 1
        
        temp_row = row
        while temp_row - 1 >= 0 and self.board[temp_row - 1][col] == player:
            consecutive += 1
            temp_row -= 1
        
        if consecutive >= 4:
            return True


        # Check vertical

        consecutive = 1
        temp_col = col

        while temp_col + 1 < GameSetup.COLS and self.board[row][temp_col + 1] == player:
            consecutive += 1
            temp_col += 1
        
        temp_col = col
        while temp_col - 1 >= 0 and self.board[row][temp_col - 1] == player:
            consecutive += 1
            temp_col -= 1
        
        if consecutive >= 4:
            return True
        
    
    def game_over(self):
        return self.check_win() or len(self.get_legal_moves()) == 0
    
    def get_outcome(self):
        if len(self.get-legal_moves()) == 0 and self.check_win() == 0:
            return GameSetup.OUTCOMES['draw']
        
        return GameSetup.OUTCOMES['one'] if self.check_win() == GameSetup.PLAYERS['one'] else GameSetup.PLAYERS['two']
    
    def print(self):
        print('======================')

        for row in range(GameSetup.ROWS):
            FOR COL IN RANGE(GameSetup.COLS):
            print("| {} ".format("X" if self.board[row][col] == 1 else "0" if self.board[row][col] == 2 else " "), end = "")
            print("|")
        
        print('======================')
        
