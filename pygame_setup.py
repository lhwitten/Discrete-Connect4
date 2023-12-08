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