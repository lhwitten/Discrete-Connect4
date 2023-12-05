import pygame
from connect_game import *
from monte_carlo import *
from pygame_setup import ConnectPygame
import sys


board = ConnectPygame()

board.print_board()

game_over = False
turn = 0

pygame.init()

board.draw_board()
pygame.display.set_caption('Connect 4')

font = pygame.font.SysFont("monospace", 75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(board.screen, board.CREAM, (0, 0, board.WIDTH, board.SQUARE_SIZE))
            pos_x = event.pos[0]

            if turn == 0:
                pygame.draw.circle(board.screen, board.GREEN, (pos_x, int(board.SQUARE_SIZE / 2)), board.RADIUS)
            
            else:
                pygame.draw.circle(board.screen, board.PERIWINKLE, (pos_x, int(board.SQUARE_SIZE / 2)), board.RADIUS)
        pygame.display.update()
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(board.screen, board.CREAM, (0, 0, board.WIDTH, board.SQUARE_SIZE))

            if turn == 0:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x / board.SQUARE_SIZE))

                if board.is_legal_move(col):
                    row = board.next_valid_row(col)
                    board.drop_piece(row, col, 1)

                if board.check_win(1):
                    label = font.render("Player 1 wins!!", 1, board.GREEN)
                    board.screen.blit(label, (40, 10))
                    game_over = True

            else:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x / board.SQUARE_SIZE))

                if board.is_legal_move(col):
                    row = board.next_valid_row(col)
                    board.drop_piece(row, col, 2)

                if board.check_win(2):
                    label = font.render("Player 2 wins!!", 1, board.PERIWINKLE)
                    board.screen.blit(label, (40, 10))
                    game_over = True
            
            board.print_board()
            board.draw_board()

            turn += 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(5000)