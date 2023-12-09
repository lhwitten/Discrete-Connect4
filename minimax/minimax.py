import numpy as np

def print_board(board):
    for row in board:
        print("|".join(row))
    print("")

def is_valid_move(board, col):
    return board[0][col] == ' '

def drop_piece(board, col, player):
    for row in range(5, -1, -1):
        if board[row][col] == ' ':
            board[row][col] = player
            return

def evaluate_window(window, player):
    score = 0
    opponent = 'X' if player == 'O' else 'O'
    
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(' ') == 1:
        score += 5
    elif window.count(player) == 2 and window.count(' ') == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(' ') == 1:
        score -= 100

    if window.count(player) == 3 and window.count(' ') == 1:
        score += 50  # Give a higher score for a winning move

    if window.count(player) == 3 and window.count(' ') == 1 and ' ' in window:
        score += 1000  # Encourage taking the winning move

    return score

def score_position(board, player):
    score = 0

    # Score center column
    #center_array = [int(i) for i in list(board[:, 3])]
    center_array = [i for i in list(board[:, 3])]
    center_count = center_array.count(player)
    score += center_count * 3

    # Score horizontal
    for row in range(6):
        #row_array = [int(i) for i in list(board[row, :])]
        row_array = [i for i in list(board[row, :])]
        for col in range(4):
            window = row_array[col:col+4]
            score += evaluate_window(window, player)

    # Score vertical
    for col in range(7):
        #col_array = [int(i) for i in list(board[:, col])]
        col_array = [i for i in list(board[:, col])]
        for row in range(3):
            window = col_array[row:row+4]
            score += evaluate_window(window, player)

    # Score positive diagonal
    for row in range(3):
        for col in range(4):
            window = [board[row+i][col+i] for i in range(4)]
            score += evaluate_window(window, player)

    # Score negative diagonal
    for row in range(3):
        for col in range(4):
            window = [board[row+3-i][col+i] for i in range(4)]
            score += evaluate_window(window, player)

    return score

def is_terminal_node(board):
    return check_winner(board, 'X') or check_winner(board, 'O') or len(get_valid_locations(board)) == 0

def minimax(board, depth, maximizing_player, alpha, beta):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if check_winner(board, 'O'):
                return (None, -100000000000000)
            elif check_winner(board, 'X'):
                return (None, 100000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, 'O'))

    if maximizing_player:
        value = -np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, col, 'O')
            new_score = minimax(temp_board, depth-1, False, alpha, beta)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = np.Inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, col, 'X')
            new_score = minimax(temp_board, depth-1, True, alpha, beta)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_next_open_row(board, col):
    for r in range(6):
        if board[r][col] == ' ':
            return r

def get_valid_locations(board):
    valid_locations = []
    for col in range(7):
        if is_valid_move(board, col):
            valid_locations.append(col)
    return valid_locations

def check_winner(board, player):
    # Check horizontal
    for row in range(6):
        for col in range(4):
            if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player:
                return True

    # Check vertical
    for col in range(7):
        for row in range(3):
            if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
                return True

    # Check positive diagonal
    for row in range(3):
        for col in range(4):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True

    # Check negative diagonal
    for row in range(3):
        for col in range(4):
            if board[row+3][col] == player and board[row+2][col+1] == player and board[row+1][col+2] == player and board[row][col+3] == player:
                return True

    return False

def play_connect4():
    board = np.full((6, 7), ' ')
    game_over = False
    turn = 0

    while not game_over:
        if turn % 2 == 0:
            col, minimax_score = minimax(board, 4, True, -np.Inf, np.Inf)
            if is_valid_move(board, col):
                drop_piece(board, col, 'O')
                if check_winner(board, 'O'):
                    print("AI wins!")
                    game_over = True
            else:
                print("Invalid move by AI, the game is a draw.")
                game_over = True
        else:
            print_board(board)
            try:
                col = int(input("Player 1, enter your move (0-6): "))
                if is_valid_move(board, col):
                    drop_piece(board, col, 'X')
                    if check_winner(board, 'X'):
                        print_board(board)
                        print("Player 1 wins!")
                        game_over = True
                else:
                    print("Invalid move, please try again.")
                    continue
            except ValueError:
                print("Invalid input, please enter a number between 0")
                continue
        turn += 1

        if turn == 42:  # All positions filled, game is a draw
            print_board(board)
            print("The game is a draw!")
            game_over = True

if __name__ == "__main__":
    play_connect4()
