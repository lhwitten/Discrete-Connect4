from connect_game import *
from monte_carlo import *

def play():
    state = ConnectState()
    monte_carlo = MonteCarlo(state)
    
    while not state.game_over():
        print("Current State:")
        state.print()
        
        user_move = int(input("Enter a move: "))
        while user_move not in state.get_legal_moves():
            print("Illegal move")
            user_move = int(input("Enter a move: "))
            
        state.move(user_move)
        monte_carlo.move(user_move)
        
        state.print()
        
        if state.game_over():
            print("Player one won!")
            break
        
        print("Thinking...")
        
        monte_carlo.search(2)
        num_rollouts, run_time = monte_carlo.statistics()
        
        print(f"Statistics: {num_rollouts} rollouts in {run_time} seconds")
        move = monte_carlo.best_move()
        
        print(f"MCTS chose move: {move}")
        
        state.move(move)
        monte_carlo.move(move)

        
        if state.game_over():
            state.print()
            print("Player two won!")
            break
        

# if __name__ == "__main__":
#     play()