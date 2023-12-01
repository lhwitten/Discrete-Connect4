import numpy as np

ROWS = 6
COLUMNS = 7

# Matrix of 7x7 zeros. Zero represents empty (not yet played).

def create_board():
    board = np.zeros((ROWS,COLUMNS))
    return board
 
def update_board(board, row, col, piece):
    board[row][col] = piece
 
def is_legal_move(board, col):
    # returns true if space is empty
    for row, col in board:
        if row == 0 and board[row][col] == 0:
            return board[row][col] == 0
 
def next_valid_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r
        
def check_win():
    pass