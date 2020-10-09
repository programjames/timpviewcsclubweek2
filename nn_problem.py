"""
TicTacToe Analyst

Problem Statement:
Given a Tic Tac Toe board, use a neural net to determine which person wins.
Output 1 if "X" wins, -1 if "O" wins, and 0 if no one wins.

Note: you will probably need a wrapper function to convert the output from
your neural net into -1, 0, or 1, as an answer of 0.9997 will be considered
wrong if it is supposed to be 1.
"""

import random

def generate_random_board():
    """Returns the inputs and the winner. The inputs are defined below."""

    # List of winning indices; if one player has all of a group of three, they win.
    winning_positions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
                         (2, 5, 8), (0, 4, 8), (2, 4, 6)]

    # Blank board
    inputs = [0 for i in range(9)]

    # List of which spots are open to place in.
    open = list(range(9))

    # X starts the game
    turn = "X"

    # Letter to input value.
    key = {"X": 1, "O": -1}
    while len(open) > 0:
        # Choose a random spot and place in it.
        i = random.choice(open)
        inputs[i] = key[turn]
        
        # This spot is no longer open
        open.remove(i)

        # Check if they win
        for pos in winning_positions:
            if all(inputs[p] == key[turn] for p in pos):
                return inputs, key[turn]
        
        # Switch whose turn it is.
        if turn == "X":
            turn = "O"
        else:
            turn = "X"
    
    # No one won, it must have been a draw.
    return inputs, 0
            

def test_function(f):
    """
    f(inputs) should give the correct output (-1, 0, or 1) depending on the
    inputs. The inputs will look similar to:

        [1, -1, -1, -1, 1, 1, 0, 0, 1]

    The first 3 values correspond to the first row of the tictactoe board,
    the next 3 values correspond to the middle row, and the last 3 values
    correspond to the last row. A 0 means no one placed in that square, a
    1 means X placed in the square, and a -1 means O placed in the square.

    So, the example above would correspond to this tictactoe board:
    
        X|O|O
        ------
        O|X|X
        ------
         | |X

    In this example X wins, so your function should output 1.

    """
    inputs, output = generate_random_board()
    return f(inputs) == output
    
