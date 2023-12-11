"""
Connect 4 game minimax vs. MCTS
"""
import pygame
from connect_game import ConnectState
from monte_carlo import MonteCarlo
from pygame_setup import ConnectPygame
from game_setup import GameSetup
import sys
import random
import math
import numpy as np


#----------------------------------------------------------------------------------
## OBJECTS
#----------------------------------------------------------------------------------
board = ConnectState()
monte_carlo = MonteCarlo(board)

#----------------------------------------------------------------------------------
## SETUP
#----------------------------------------------------------------------------------
game_over = False
turn = 0
user_turn = 0
#user_turn = 1

DEPTH = 5
ROW_COUNT = GameSetup.ROWS
COLUMN_COUNT = GameSetup.COLS

pygame.init()
board.draw_board()
pygame.display.set_caption('Connect 4')
font = pygame.font.SysFont("monospace", 75)

#----------------------------------------------------------------------------------
## MINIMAX SETUP
#----------------------------------------------------------------------------------
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

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

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
     
def cheesed_array(arr):
    # Create a copy of the original array
    swapped_array = arr.copy()
    
    # Swap values in the temporary array
    swapped_array[arr == 1] = 2
    swapped_array[arr == 2] = 1
    
    return swapped_array

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        # Minimax player
        if turn == user_turn:
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(ConnectPygame.screen, ConnectPygame.CREAM, (0, 0, ConnectPygame.WIDTH, ConnectPygame.SQUARE_SIZE))
                pos_x = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(ConnectPygame.screen, ConnectPygame.GREEN, (pos_x, int(ConnectPygame.SQUARE_SIZE / 2)), ConnectPygame.RADIUS)
                if turn == 1:
                    pygame.draw.circle(ConnectPygame.screen, ConnectPygame.PERIWINKLE, (pos_x, int(ConnectPygame.SQUARE_SIZE / 2)), ConnectPygame.RADIUS)
                    
            pygame.display.update()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(ConnectPygame.screen, ConnectPygame.CREAM, (0, 0, ConnectPygame.WIDTH, ConnectPygame.SQUARE_SIZE))
                pos_x = event.pos[0]
                #col, minimax_score = minimax(cheesed_array(np.array(board.get_board())), DEPTH, -math.inf, math.inf, True)
                col, minimax_score = minimax(np.flip(np.array(board.get_board()), 0), DEPTH, -math.inf, math.inf, True)
                #col = int(math.floor(pos_x / ConnectPygame.SQUARE_SIZE))

                if col in board.get_legal_moves():
                    board.move(col)
                    monte_carlo.move(col)
                    #board.print()
                    print(np.array(board.get_board()))
                    print("minimax played")
                else:
                    print(col)
                    print("ILLEGAL MOVE BY MINIMAX :(((")
                    
                turn += 1
                turn = turn % 2
                    
                if board.game_over():
                    if user_turn == 0:
                        label = font.render("Player 1 wins!!", 1, ConnectPygame.GREEN)
                        ConnectPygame.screen.blit(label, (40, 10))
                        game_over = True        
                    if user_turn == 1:
                        label = font.render("Player 2 wins!!", 1, ConnectPygame.PERIWINKLE)
                        ConnectPygame.screen.blit(label, (40, 10))
                        game_over = True        
                          
            board.draw_board()


        # Monte Carlo player
        if turn != user_turn:
            monte_carlo.search(3)
            num_rollouts, run_time = monte_carlo.statistics()
            move = monte_carlo.best_move()
            board.move(move)
            monte_carlo.move(move)
            #board.print()
            print(np.array(board.get_board()))
            print("monte carlo played")

            turn += 1
            turn = turn % 2
            
            if board.game_over():
                if user_turn == 0:
                    label = font.render("Player 2 wins!!", 1, ConnectPygame.PERIWINKLE)
                    ConnectPygame.screen.blit(label, (40, 10))
                    board.draw_board()
                if user_turn == 1:
                    label = font.render("Player 1 wins!!", 1, ConnectPygame.GREEN)
                    ConnectPygame.screen.blit(label, (40, 10))
                    board.draw_board()
                game_over = True

            if game_over:
                pygame.time.delay(2500)