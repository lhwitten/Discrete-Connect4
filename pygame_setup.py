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
    """
    #----------------------------------------------------------------------------------
    ## VISUALIZATION SETUP
    #----------------------------------------------------------------------------------
    BLUE = (204, 255, 255)          #  Board
    CREAM = (255, 255, 239)         #  Background
    GREEN = (204, 255, 229)         #  Player 1
    PERIWINKLE = (204, 229, 255)    #  Player 2
    SQUARE_SIZE = 100
    RADIUS = int(SQUARE_SIZE/2 - 5)

    #----------------------------------------------------------------------------------
    ## SCREEN SETUP
    #----------------------------------------------------------------------------------
    WIDTH = GameSetup.COLS * SQUARE_SIZE
    HEIGHT = (GameSetup.ROWS + 1) * SQUARE_SIZE
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size) 