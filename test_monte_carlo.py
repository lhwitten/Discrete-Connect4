"""
Test cases for our MCTS Algorithm.
"""

from connect_game import ConnectState

def test_get_board():
    game = ConnectState()
    original_board = game.get_board()
    original_board[0][0] = 1
    
    assert original_board != game.get_board
    


if __name__ == "__main__":
    test_get_board()