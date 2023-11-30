#connect 4 initial copy pasted

import numpy as np
import pygame
import sys
import math

################################ ALL MINIMAX HERE

def evaluate_window(window, player):
    score = 0
    opponent_piece = 2
    if player == 2:
        opponent_piece = 1
    
    if window.count(player) == 4:
        score += 100
    if window.count(player) == 3 and window.count(' ') == 1:
        score += 5
    if window.count(player) == 2 and window.count(' ') == 2:
        score += 2

    if window.count(opponent_piece) == 3 and window.count(' ') == 1:
        score -= 10
    if window.count(opponent_piece) == 2 and window.count(' ') == 2:
        score -= 2

    if window.count(player) == 3 and window.count(' ') == 1:
        score += 50  # Give a higher score for a winning move
    
    return score

def score_position(board, player):
    score = 0

    # Score center column
    #center_array = [int(i) for i in list(board[:, 3])]
    center_array = [i for i in list(board[:, 3])]
    center_count = center_array.count(player)
    score += center_count * 3

    num_cols = COLUMN_COUNT
    num_rows = ROW_COUNT

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
    for col_num in range(num_cols):
        for row_num in range(num_rows -4 + 1):
            window = [board[row_num +i][col_num] for i in range(4)]
            score += evaluate_window(window,player)

    # Score vertical
    for row_num in range(num_rows):
        for col_num in range(num_cols -4 +1):
            window = [board[row_num][col_num + i] for i in range(4)]
            score += evaluate_window(window,player)

    # Score positive diagonal
    for row_num in range(num_rows -4 +1):
        for col_num in range(num_cols -4 +1):
            window = [board[row_num +i][col_num + i] for i in range(4)]
            score += evaluate_window(window,player)

    # Score negative diagonal
    for row_num in range(num_rows -4 +1):
        for col_num in range(num_cols -4 +1):
            window = [board[num_rows - row_num -i -1][col_num + i] for i in range(4)]
            score += evaluate_window(window,player)

    return score

def is_valid_move(board, col):
    return board[0][col] == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_move(board, col):
            valid_locations.append(col)
    return valid_locations

def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or len(get_valid_locations(board)) == 0

def minimax(board, depth, is_maximizing,ai_player):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    opponent = 2
    if ai_player ==2:
        opponent = 1

    if depth ==0 or is_terminal:
        if is_terminal:
            if winning_move(board, ai_player):
                return (None,-1000000000000000)
            elif winning_move(board, opponent):
                return (None,10000000000000)
            else:
                return(None,0)
        else:
            return (None, score_position(board,ai_player))

    #what the maximizing player does, what the AI wants  
    if is_maximizing:
        value = -1000000000000000
        column = np.random.choice(valid_locations)

        for col in valid_locations:
            row = get_next_open_row(board,col)
            temp_board = board.copy()
            drop_piece(temp_board,row,col,ai_player)
            new_score = minimax(temp_board,depth-1,False)[1]
            #set the score to the best score out of the seen columns
            if new_score > value:
                value = new_score
                column = col
            #alpha beta pruning would go here
        return column, value
    #find best move for the minimizer, the player
    else:
        value = 100000000000000
        column = np.random.choice(valid_locations)
        
        for col in valid_locations:
            row = get_next_open_row(board,col)
            temp_board = board.copy()
            drop_piece(temp_board,row,col,opponent)
            new_score = minimax(temp_board,depth-1,True)[1]
            
            #this player wants to minimize the score of the AI player
            if new_score < value:
                value = new_score
                column = col
            
            #alpha beta prining would go here
        
        return column,value




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
                col = int(math.floor(posx/SQUARESIZE))
 
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
 
                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True


            # # Ask for Player 2 Input
            else:               
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))


                col, value = minimax(board,4,True,2)
 
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
