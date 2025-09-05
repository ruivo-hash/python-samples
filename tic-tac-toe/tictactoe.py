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
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == "X":
                x_count += 1
            elif cell == "O":
                o_count += 1

    return "X" if x_count <= o_count else "O"


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possibilities = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == None:
                possibilities.add((i, j))
    
    return possibilities


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] is not None:
        raise Exception("Invalid cell, try another")

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    # Columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    # Diagonal
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    haveWinner = winner(board)
    if haveWinner != None:
        return True
    
    cellLefts = 0
    for row in board:
        for cell in row:
            if cell == None:
                cellLefts += 1
    
    if cellLefts > 0:
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    haveWinner = winner(board)
    if haveWinner == "X":
        return 1
    elif haveWinner == "O":
        return -1
    else:
        return 0


def maxValue(board):
    if terminal(board):
        return utility(board), None

    value = float('-inf')
    bestMove = None

    for action in actions(board):
        resultValue, _ = minValue(result(board, action))
        if resultValue > value:
            value = resultValue
            bestMove = action

    return value, bestMove


def minValue(board):
    if terminal(board):
        return utility(board), None

    value = float('inf')
    bestMove = None

    for action in actions(board):
        resultValue, _ = maxValue(result(board, action))
        if resultValue < value:
            value = resultValue
            bestMove = action

    return value, bestMove


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current = player(board)
    if current == "X":
        _, bestMove = maxValue(board)
    else:
        _, bestMove = minValue(board)

    return bestMove

    
    

    
