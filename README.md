# Connect 4: Minimax vs. Monte Carlo Tree Search 
### Prisha Bhatia, Allyson Hur, Luke Witten, Milo Song-Weiss

## Project Overview
Our project explores two different Connect 4 algorithms: Minimax and Monte Carlo Tree Search (MCTS). The Minimax algorithm primarily focuses on determining the optimal move by recursively evaluating future game states. The MCTS algorithm operates through a process of random simulations and tree exploration to find an optimal decision. We investigate which algorithm would perform more optimally when the two are played against each other.

Please see this [google slides](https://docs.google.com/presentation/d/1lUV6oKq1TK0hJg7rceNy-cgHpFHKEblRK2_G2xImq64/edit?usp=sharing) link for a guided walkthrough on how the two algorithms work.

## Dependencies
These instructions are for Ubuntu 22.04. Download numpy using the following command.
```
$ pip install numpy
```

## Instructions
Please download this repository. These instructions are for Ubuntu 22.04.
**Make sure you are in the Discrete-Connect4 directory.**
To run the single player game for Minimax, run the following command:
```
$ python3 minimax/play_game.py
```
To run the single player game for MCTS, run the following command:
```
$ python3 monte_carlo/play_game.py
```
To run the AI vs. AI to see Minimax vs. MCTS in action, run the following command:
```
$ python3 AIvsAI/play_game.py 
```



