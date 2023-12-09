#connect 4 initial copy pasted

import numpy as np
import pygame
import sys
import math
import random

################################ ALL MINIMAX HERE

DEPTH = 3

def evaluate_window(window, player):
    score = 0
    opponent_piece = 2
    if player == 2:
        opponent_piece = 1
    
    if window.count(player) == 4:
        score += 100
    if window.count(player) == 3 and window.count(0) == 1:
        score += 5
    if window.count(player) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4
    """if window.count(opponent_piece) == 2 and window.count(0) == 2:
        score -= 2

    if window.count(player) == 3 and window.count(0) == 1:
        score += 50  # Give a higher score for a winning move"""
    
    return score

def score_position(board, player):
    score = 0

    # Score center column
    #center_array = [int(i) for i in list(board[:, 3])]
    center_array = [int(i) for i in list(board[:, 3])]
    center_count = center_array.count(player)
    score += center_count * 3

    win_number = 10000

    opponent_piece = 2
    if player == 2:
        opponent_piece = 1
    #check for wins
    if winning_move(board,player):
        score += win_number
        return score
    if winning_move(board,opponent_piece):
        score -= win_number
        return score


    # Score horizontal
    for col_num in range(COLUMN_COUNT):
        for row_num in range(ROW_COUNT -4 + 1):
            window = [board[row_num +i][col_num] for i in range(4)]
            score += evaluate_window(window,player)

    # Score vertical
    for row_num in range(ROW_COUNT):
        for col_num in range(COLUMN_COUNT -4 +1):
            window = [board[row_num][col_num + i] for i in range(4)]
            score += evaluate_window(window,player)

    # Score positive diagonal
    for row_num in range(ROW_COUNT -4 +1):
        for col_num in range(COLUMN_COUNT -4 +1):
            window = [board[row_num +i][col_num + i] for i in range(4)]
            score += evaluate_window(window,player)

    # Score negative diagonal
    for row_num in range(ROW_COUNT -4 +1):
        for col_num in range(COLUMN_COUNT -4 +1):
            window = [board[ROW_COUNT - row_num -i -1][col_num + i] for i in range(4)]
            score += evaluate_window(window,player)

    return score

def is_valid_move(board, col):
    return board[5][col] == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_move(board, col):
            valid_locations.append(col)
    return valid_locations

def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, 1):
				return (None, 100000000000000)
			elif winning_move(board, 2):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, 1))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, 1)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, 2)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value




############################################3



BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
 
ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board
 
def drop_piece(board, row, col, piece):
    board[row][col] = piece
 
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0
 
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
 
def print_board(board):
    print(np.flip(board, 0))
 
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
 
    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
 
    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
 
    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
 
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
     
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


board = create_board()
print_board(board)
game_over = False
turn = 0
 
#initalize pygame
pygame.init()
 
#define our screen size
SQUARESIZE = 100
 
#define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
 
size = (width, height)
 
RADIUS = int(SQUARESIZE/2 - 5)
 
screen = pygame.display.set_mode(size)
#Calling function draw_board again
draw_board(board)
pygame.display.update()
 
myfont = pygame.font.SysFont("monospace", 75)
 
while not game_over:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
 
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else: 
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()
 
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            #print(event.pos)
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                #col = int(math.floor(posx/SQUARESIZE))

                col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
 
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
 
                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True


            # # Ask for Player 2 Input
            else:               
                #posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                #print(board)


                #col, value = minimax(board,DEPTH,False,2)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)
 
                    if winning_move(board, 2):
                        label = myfont.render("Player 2 wins!!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True
 
            print_board(board)
            draw_board(board)
 
            turn += 1
            turn = turn % 2
 
            if game_over:
                pygame.time.wait(3000)
