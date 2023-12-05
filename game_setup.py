"""
Connect 4 Game Setup.
"""
import math

class GameSetup:
    """
    Sets up important components of the Connect 4 game.
    
    Attributes:
        PLAYERS: dictionary for players.
        OUTCOMES: dictionary for outcomes of game.
        EXPLORATION: a heuristic value used to calculate UCB.
        INF: infinity
        ROWS: number of rows on the board
        COLS: number of columns on the board.
    """
    PLAYERS = {'none': 0, 'one': 1, 'two': 2}
    OUTCOMES = {'none': 0, 'one': 1, 'two': 2, 'draw': 3}
    EXPLORATION = 2
    INF = math.inf
    ROWS = 6
    COLS = 7
