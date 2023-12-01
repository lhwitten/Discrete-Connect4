import math
import time
import random
from copy import deepcopy
from connect_game import * 

class Node:

    # Upper Confidence Bound
    # Q/N * exploration value * square root(log(parent node)/current node)

    exploration_value = 2

    def __init__(self,move,parent):
        self.move = move        # matrix
        self.parent = parent
        self.children = {}
        self.total_played = 0     # N
        self.total_won = 0      # Q
        self.outcome = GameSetup.PLAYERS["none"]
        # self.UCB = (self.total_won / self.total_played) + self.exploration_value * math.sqrt(math.ln(self.total_played)/self.total_won)

    
    def add_children(self,children:dict):
        # Include all possible unexplored children connected to current node
        for child in children:
            self.children[child.move] = child 
            
    def calculate_UCB(self,explore: float=GameSetup.EXPLORATION):
        if self.total_played == 0: 
            return 0 if explore == 0 else GameSetup.INF
        else:
            # return self.total_won/self.total_played + explore* math.sqrt(math.ln(self.total_played)/self.total_won) 
            return self.total_won/self.total_played+explore*math.sqrt(math.log(self.parent.total_played)/self.total_played)
    

    #def monte_carlo_search()
class MonteCarlo:
    def __init__(self, state=ConnectState()):
        self.root_state = deepcopy(state)
        self.root = Node(None,None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0

    

    def selection(self) -> tuple:
        # return best child node
        # select node with the highest UCB
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            children = node.children.values()
            max_value = max(children, key=lambda n: n.calculate_UCB()).calculate_UCB()
            max_nodes = [n for n in children if n.calculate_UCB() == max_value]

            node = random.choice(max_nodes)
            state.move(node.move)

            if node.total_played == 0:
                return node, state
        
        if self.expansion(node,state):
            node = random.choice(list(node.children.values()))
            state.move(node.move)
        return node,state


        
        # select a leaf node that has not been explored OR according to UCB
        pass
    def expansion(self, parent: Node, state: ConnectState) -> bool: 
        if state.game_over():
            return False
        children = [Node(move,parent) for move in state.get_legal_moves()]
        parent.add_children(children)

        return True
    
    def simulation(self, state: ConnectState) -> int:
        # Select child node (can be random) and play it out until it reaches final stage of game (keeping in mind legalities of moves)
        while not state.game_over():
            state.move(random.choice(state.get_legal_moves()))

        return state.get_outcome()
    
    def backpropagation(self, node: Node, turn: int, outcome: int) -> None:
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.total_played +=1
            node.total_won += reward
            node = node.parent
            if outcome == GameSetup.OUTCOMES['draw']:
                reward = 0
            else:
                reward = 1 - reward
        # When final state with a winner is reached, all traversed nodes are updated (visit and win-value)
    # The child of the root node with the highest number of total_played is selected as the next move

    def search(self, time_limit: int):
        start_time = time.process_time()

        num_rollouts = 0

        while time.process_time() - start_time < time_limit:
            node, state = self.selection()
            outcome = self.simulation(state)
            self.backpropagation(node, state.to_play, outcome)
            num_rollouts += 1
        
        run_time = time.process_time() - start_time
        self.run_time = run_time
        self.num_rollouts = num_rollouts

    
    def best_move(self):
        if self.root_state.game_over():
            return -1
        max_value = max(self.root.children.values(), key=lambda n: n.total_played).total_played
        max_nodes = [n for n in self.root.children.values() if n.total_played == max_value]
        best_child = random.choice(max_nodes)

        return best_child.move
    

    def move(self, move):
        if move in self.root.children:
            self.root_state.move(move)
            self.root = self.root.children[move]
            return
        
        self.root_state.move(move)
        self.root = Node(None, None)


    def statistics(self) -> tuple:
        return self.num_rollouts, self.run_time
