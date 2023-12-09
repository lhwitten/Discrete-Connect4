"""
Implementation of MCTS for Connect 4 game.
"""
import math
import time
import random
from copy import deepcopy
from connect_game import ConnectState
from game_setup import GameSetup

class Node:
    """
    Creates a node that represents a game state.

    Attributes:
         move: the current game state.
         parent: the parent node of the current node.
         children: a dictionary of the children nodes of the current node.
         total_played: he number of games played during simulation.
         total won: the number of games won during simulation.
         outcome: the outcome of the game during simulation.
    """

    def __init__(self,move,parent):
        """
        Initialize the attributes of the Node class.
        """
        self.move = move      
        self.parent = parent
        self.children = {}
        self.total_played = 0   # N
        self.total_won = 0      # Q
        self.outcome = GameSetup.PLAYERS["none"]
    
    def add_children(self,children:dict):
        """
        Add all children nodes to current node. 

        Args:
            children: a dictionary with the move as the key and the child object as the value.
        """
        for child in children:
            self.children[child.move] = child 
            
    def calculate_UCT(self,explore: float=GameSetup.EXPLORATION):
        """
        Calculate the UCB value for a node. This value determines which node to
        visit next using the exploration value, total games played by current
        node, total games played by the parent node, and total games won.

        Args:
            explore: a float representing the exploration value.
            
        Returns:
            A float representing the UCB value.
        """
        if self.total_played == 0: 
            return 0 if explore == 0 else GameSetup.INF
        else:
            return self.total_won/self.total_played+explore*math.sqrt(math.log(self.parent.total_played)/self.total_played)
        
class MonteCarlo:
    """
    Performs the Monte Carlo Tree Search.
    
    Attributes:
        root_state: the Connect 4 game state of root node.
        root: the root node.
        run_time: number of seconds the algorithm runs for.
        num_rollouts: number of simulations/rollouts.
    
    """
    def __init__(self, state=ConnectState()):
        """
        Initialize the attributes of the MonteCarlo class.

        Args:
            state: the Connect 4 game state.
        """
        self.root_state = deepcopy(state)
        self.root = Node(None,None)
        self.run_time = 0
        self.num_rollouts = 0

    def selection(self) -> tuple:
        """
        Select the best child node to visit. This function finds the node with
        the highest UCB value. If a child node has never been explored, it is
        immediately selected. If all children have been explored, the tree
        is expanded and new children nodes are added. A random child node is
        then selected from the newly expanded nodes. 

        Returns:
            A tuple representing the best child node and the resulting state.
        """
        node = self.root
        state = deepcopy(self.root_state)

        while len(node.children) != 0:
            children = node.children.values()
            max_value = max(children, key=lambda n: n.calculate_UCT()).calculate_UCT()
            max_nodes = [n for n in children if n.calculate_UCT() == max_value]

            node = random.choice(max_nodes)
            state.move(node.move)

            if node.total_played == 0:
                return node, state
        
        if self.expansion(node,state):
            node = random.choice(list(node.children.values()))
            state.move(node.move)
        return node,state

    def expansion(self, parent: Node, state: ConnectState) -> bool: 
        """
        Expands the search tree. Until the game is over, more children nodes
        are added depending on the next legal moves in the current game
        state. 

        Args:
            parent: the parent node.
            state: the Connect 4 game state.

        Returns:
            A boolean representing if the game is over or not.
        """
        if state.game_over():
            return False
        children = [Node(move,parent) for move in state.get_legal_moves()]
        parent.add_children(children)

        return True
    
    def simulation(self, state: ConnectState) -> int:
        """
        Simulates a game until an outcome is reached. 

        Args:
            state: the Connect 4 game state.

        Returns:
            An integer representing the outcome of the game (win, loss, or tie).
        """
        while not state.game_over():
            state.move(random.choice(state.get_legal_moves()))

        return state.get_outcome()
    
    def backpropagation(self, node: Node, turn: int, outcome: int) -> None:
        """
        Update traversed nodes with number of visits and number of wins. 

        Args:
            node: the starting node for backpropagation.
            turn: an integer representing the player's turn.
            outcome: an integer representing the outcome of simulated game.
        """
        reward = 0 if outcome == turn else 1

        while node is not None:
            node.total_played +=1
            node.total_won += reward
            node = node.parent
            if outcome == GameSetup.OUTCOMES['draw']:
                reward = 0
            else:
                reward = 1 - reward

    def search(self, time_limit: int):
        """
        Perform the search. For a specified amount of time, the function will
        select a node, expand the tree, simulate, then backpropagate.

        Args:
            time_limit: an integer representing the time limit for the search.
        """
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
        """
        Get the game state of the best child node. 

        Returns:
            The next move the search has decided on.
        """
        if self.root_state.game_over():
            return -1
        max_value = max(self.root.children.values(), key=lambda n: n.total_played).total_played
        max_nodes = [n for n in self.root.children.values() if n.total_played == max_value]
        best_child = random.choice(max_nodes)

        return best_child.move
    

    def move(self, move):
        """
        Update the game state based on the given move. If the move already exists 
        within the existing children nodes, the new root is assigned to the
        child node corresponding to the given move. If the move doesn't exist
        within the children nodes, then a new root node is created.

        Args:
            move: the move to be performed
        """
        if move in self.root.children:
            self.root_state.move(move)
            self.root = self.root.children[move]
            return
        
        self.root_state.move(move)
        self.root = Node(None, None)


    def statistics(self) -> tuple:
        """
        Get statistics of MCTS algorithm.

        Returns:
            A tuple representing the number of simulations and the run time.
        """
        return self.num_rollouts, self.run_time




    

