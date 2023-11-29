import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

# Matrix of 7x7 zeros. Zero represents empty (not yet played).

def initialize_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def is_legal_move(board, col):
    row_number = 0
    for row in board:
        if board[row][col] == 0:
            row_number = row
            break
    return row_number

def update_board(board, row, col):
    if is_legal_move(board, col):
        board[row][col] = 1
    return board

    



# nodes = {(i, j) for i in range(7) for j in range(7)}
# print(board)

# for key in nodes:
#     row, col = key
#     key_str = str(board[row][col])
#     print(key_str)