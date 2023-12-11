"""
Connect 4 Game Setup.
"""
import math

class GameSetup:
    """
    Sets up important components of the Connect 4 game.
    """
    PLAYERS = {'none': 0, 'one': 1, 'two': 2}
    OUTCOMES = {'none': 0, 'one': 1, 'two': 2, 'draw': 3}
    EXPLORATION = 2
    INF = math.inf
    ROWS = 6
    COLS = 7