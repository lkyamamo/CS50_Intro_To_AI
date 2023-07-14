"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    xCount = 0
    oCount = 0

    for row in board:
        for element in row:
            if element == "O":
                oCount += 1
            elif element == "X":
                xCount += 1

    if(oCount < xCount):
        return "O"
    else:
        return "X"
    
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    output = set()

    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                output.add((row,column))

    return output

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if board[action[0]][action[1]] != EMPTY:
        raise NameError("Invalid Action")
    
    newBoard = copy.deepcopy(board)

    newBoard[action[0]][action[1]] = player(board)

    return newBoard

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    #horizontal
    for row in board:
        if row[0] == row[1] == row[2] == "X":
            return "X"
        if row[0] == row[1] == row[2] == "O":
            return "O"

    #vertical
    for col in range(3):
        if(board[0][col] == board[1][col] == board[2][col]):
            if board[0][col] == "X":
                return "X"
            elif board[0][col] == "O":
                return "O"

    #diagonal
    if (board[0][0] == board[1][1] == board[2][2]) or (board[0][2] == board[1][1] == board[2][0]):
        if board[1][1] == "X":
            return "X"
        elif board[1][1] == "O":
            return "O"

    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) != None:
        return True

    for row in board:
        if EMPTY in set(row):
            return False
        
    return True

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    result = winner(board)

    if result == "X":
        return 1
    elif result == "O":
        return -1
    else:
        return 0
    
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None
    
    turn = player(board)

    possibleActions = actions(board)
    if(turn == "X"):
        choice = (-2, None)
        for action in possibleActions:
            current = (assignUtility(result(board, action)), action)
            if current[0] > choice[0]:
                choice = current
        return choice[1]
    else:
        choice = (2, None)
        for action in possibleActions:
            current = (assignUtility(result(board, action)), action)
            if current[0] < choice[0]:
                choice = current
        return choice[1]

def assignUtility(board):
    
    if terminal(board):
        return utility(board)
    
    if(player(board) == "X"):
        choice = -2
        for action in actions(board):
            choice = max(choice, assignUtility(result(board, action)))

    else:
        choice = 2
        for action in actions(board):
            choice = min(choice, assignUtility(result(board, action)))

    return choice

    raise NotImplementedError