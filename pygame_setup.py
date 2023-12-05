import pygame
import math
import sys
import numpy as np
from game_setup import *

class ConnectPygame:

    GREEN = (204, 255, 229) #Player 1
    BLUE = (204, 255, 255)  #Board
    PERIWINKLE = (204, 229, 255)    #Player 2
    CREAM = (255, 255, 239) #Background

    SQUARE_SIZE = 100

    ROWS = GameSetup.ROWS
    COLS = GameSetup.COLS

    WIDTH = COLS * SQUARE_SIZE
    HEIGHT = (ROWS + 1) * SQUARE_SIZE

    size = (WIDTH, HEIGHT)

    RADIUS = int(SQUARE_SIZE/2 - 5)

    screen = pygame.display.set_mode(size)

    def __init__(self):
        self.board = np.zeros((self.ROWS, self.COLS))

    def get_board(self):
        return self.board

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece
        
    def is_legal_move(self, col):
        return self.board[5][col]== 0
    
    def next_valid_row(self, col):
        for r in range(GameSetup.ROWS):
            if self.board[r][col]==0:
                return r

    def print_board(self):
        print(np.flip(self.board, 0))

    def draw_board(self):
        for col in range(self.COLS):
            for row in range(self.ROWS):
                pygame.draw.rect(self.screen, self.BLUE, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE + self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
                pygame.draw.circle(self.screen, self.CREAM, (int(col * self.SQUARE_SIZE + self.SQUARE_SIZE / 2), int(row * self.SQUARE_SIZE + self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.RADIUS)

        for c in range(self.COLS):
            for r in range(self.ROWS):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.GREEN, (int(c*self.SQUARE_SIZE+self.SQUARE_SIZE/2),self.HEIGHT-int(r*self.SQUARE_SIZE+self.SQUARE_SIZE/2)),self.RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.PERIWINKLE , (int(c*self.SQUARE_SIZE+self.SQUARE_SIZE/2),self.HEIGHT-int(r*self.SQUARE_SIZE+self.SQUARE_SIZE/2)),self.RADIUS)
            pygame.display.update()


    def check_win(self, piece):
        # Check horizontal locations for win
        for c in range(int(self.COLS) - 3):
            for r in range(int(self.ROWS)):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True
    
        # Check vertical locations for win
        for c in range(int(self.COLS)):
            for r in range(int(self.ROWS) -3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True
    
        # Check positively sloped diaganols
        for c in range(int(self.COLS)-3):
            for r in range(int(self.ROWS)-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True
    
        # Check negatively sloped diaganols
        for c in range(int(self.COLS)-3):
            for r in range(3, int(self.ROWS)):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

                            