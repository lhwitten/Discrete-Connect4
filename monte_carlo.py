# Pseudocode for main function for the Monte Carlo Tree Search

# Set root node to the current game state
import math

class Node:

    # Upper Confidence Bound
    # Q/N * exploration value * square root(log(parent node)/current node)

    exploration_value = 2

    def __init__(self,game_state,parent):
        self.game_state = game_state        # matrix
        self.children = {}
        self.visits = 0
        self.wins = 0      # Total games won / total games played OR Q/N
        self.UCB = (self.wins / self.visits) + self.exploration_value * math.sqrt(math.ln(self.visits)/self.wins)

    

    
    def add_children(self,children:dict):
        # Include all possible unexplored children connected to current node
        for child in children:
            self.children[child.state] = child 

    def selection(self, root_node):
        # return best child node
        # select node with the highest UCB
        
        # select a leaf node that has not been explored OR according to UCB
        pass
    def expansion(self, children :dict):
          
        pass
    def simulation(self):
        # Select child node (can be random) and play it out until it reaches final stage of game (keeping in mind legalities of moves)
        pass
    def backpropagation(self):
        # When final state with a winner is reached, all traversed nodes are updated (visit and win-value)
        pass
    # The child of the root node with the highest number of visits is selected as the next move

    #def monte_carlo_search()
        

