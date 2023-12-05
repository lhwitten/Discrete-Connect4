"""
Pygame implementation of Connect 4 game.
"""
import pygame
import math
import sys
import numpy as np
from game_setup import *

class ConnectPygame:
    """
    Sets up the visualization for a multiplayer Connect 4 game.
    
    Attributes:
        board: a matrix representing the Connect 4 board.
    """

    # Colors for the visualization
    GREEN = (204, 255, 229)         #  Player 1
    BLUE = (204, 255, 255)          #  Board
    PERIWINKLE = (204, 229, 255)    #  Player 2
    CREAM = (255, 255, 239)         #  Background

    SQUARE_SIZE = 100
    RADIUS = int(SQUARE_SIZE/2 - 5)

    # Screen size setup
    WIDTH = GameSetup.COLS * SQUARE_SIZE
    HEIGHT = (GameSetup.ROWS + 1) * SQUARE_SIZE
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)    

    def __init__(self):
        """
        Initialize the attributes for the ConnectPygame class.
        """
        self.board = np.zeros((GameSetup.ROWS, GameSetup.COLS))

    def get_board(self):
        """
        Get the Connect 4 board.

        Returns:
            A matrix representing the game board.
        """
        return self.board

    def drop_piece(self, row, col, piece):
        """
        Drop a game piece into a specified place. Given the row and column, the
        specified player piece will be dropped at that index.

        Args:
            row: an integer representing the row.
            col: an integer representing the column.
            piece: an integer representing which player.
        """
        self.board[row][col] = piece
        
    def is_legal_move(self, col):
        """
        Check if a given column is a legal move.

        Args:
            col: an integer representing the column.

        Returns:
            True if the column is legal.
        """
        return self.board[5][col]== 0
    
    def next_valid_row(self, col):
        """
        Get the next valid row given a column.

        Args:
            col: an integer representing the column.

        Returns:
            r: an integer representing the next valid row.
        """
        for r in range(GameSetup.ROWS):
            if self.board[r][col]==0:
                return r

    def print_board(self):
        """
        Print the board as a matrix.
        """
        print(np.flip(self.board, 0))

    def draw_board(self):
        """
        Draw the Connect 4 game board.
        """
        for col in range(GameSetup.COLS):
            for row in range(GameSetup.ROWS):
                pygame.draw.rect(self.screen, self.BLUE, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE + self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))
                pygame.draw.circle(self.screen, self.CREAM, (int(col * self.SQUARE_SIZE + self.SQUARE_SIZE / 2), int(row * self.SQUARE_SIZE + self.SQUARE_SIZE + self.SQUARE_SIZE / 2)), self.RADIUS)

        for c in range(GameSetup.COLS):
            for r in range(GameSetup.ROWS):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.GREEN, (int(c*self.SQUARE_SIZE+self.SQUARE_SIZE/2),self.HEIGHT-int(r*self.SQUARE_SIZE+self.SQUARE_SIZE/2)),self.RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.PERIWINKLE , (int(c*self.SQUARE_SIZE+self.SQUARE_SIZE/2),self.HEIGHT-int(r*self.SQUARE_SIZE+self.SQUARE_SIZE/2)),self.RADIUS)
            pygame.display.update()


    def check_win(self, piece):
        """
        Given a player, check for a win.

        Args:
            piece: an integer representing the player

        Returns:
            True if there is a win for that player and false otherwise.
        """
        # Check horizontal locations for win
        for c in range(int(GameSetup.COLS) - 3):
            for r in range(int(GameSetup.ROWS)):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True
    
        # Check vertical locations for win
        for c in range(int(GameSetup.COLS)):
            for r in range(int(GameSetup.ROWS) -3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True
    
        # Check positively sloped diaganols
        for c in range(int(GameSetup.COLS)-3):
            for r in range(int(GameSetup.ROWS)-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True
    
        # Check negatively sloped diaganols
        for c in range(int(GameSetup.COLS)-3):
            for r in range(3, int(GameSetup.ROWS)):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

                            