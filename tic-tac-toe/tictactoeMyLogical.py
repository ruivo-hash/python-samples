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
    aux = 0
    for row in board:
        for cell in row:
            if cell == None:
                aux += 1
    
    if aux  % 2 == 0:
        return O
    else:
        return X


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
    boardCopy = copy.deepcopy(board)
    if boardCopy[action[0]][action[1]] is not None:
        raise Exception("Invalid cell, try another")
    else:
        boardCopy[action[0]][action[1]] = player(boardCopy)
        return boardCopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] == board[0][2] or board[0][0] == board[1][0] == board[2][0] or board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    elif board[0][2] == board[1][2] == board[2][2] or board[2][0] == board[2][1] == board[2][2] and board[0][0] is not None:
        return board[2][2]
    elif board[0][1] == board[1][1] == board[2][1] or board[1][0] == board[1][1] == board[1][2] or board[2][0] == board[1][1] == board[0][2] and board[0][0] is not None:
        return board[1][1]
    else:
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
    
    value = -2**63
    bestMove = None

    for action in actions(board):
        resultValue, _ = minValue(result(board, action))
        if value < resultValue:
            bestMove = action
        value = max(value, resultValue)

    return (value, bestMove)


def minValue(board):
    if terminal(board):
        return utility(board), None
    
    value = 2**63
    bestMove = None

    for action in actions(board):
        resultValue, _ = maxValue(result(board, action))
        if value > resultValue:
            bestMove = action
        value = min(value, resultValue)

    return (value, bestMove)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #while not terminal():
    if terminal(board):
        return None

    current = player(board)
    if current == "X":
        _, bestMove = maxValue(board)
    else:
        _, bestMove = minValue(board)
        
    return bestMove
    
