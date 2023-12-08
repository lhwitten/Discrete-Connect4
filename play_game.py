"""
Single player Connect 4 game vs. MCTS player.
"""
import pygame
from connect_game import *
from monte_carlo import *
from pygame_setup import ConnectPygame
import sys
import random


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
user_turn = random.choice([0, 1])

pygame.init()
board.draw_board()
pygame.display.set_caption('Connect 4')
font = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
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
                user_move = int(math.floor(pos_x / ConnectPygame.SQUARE_SIZE))
                
                if user_move in board.get_legal_moves():
                    board.move(user_move)
                    monte_carlo.move(user_move)
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


        if turn != user_turn:
            board.print()
            monte_carlo.search(3)
            num_rollouts, run_time = monte_carlo.statistics()
            move = monte_carlo.best_move()
            board.move(move)
            monte_carlo.move(move)

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