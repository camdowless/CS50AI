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
            if cell == X:
                x_count += 1
            if cell == O:
                o_count += 1
    if (x_count - o_count == 0) | (x_count == 0 & o_count == 0):
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                possible.add((i, j))
    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new = copy.deepcopy(board)
    new[action[0]][action[1]] = player(board)
    return new


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] == board[0][2]:
        return board[0][0]
    if board[1][0] == board[1][1] == board[1][2]:
        return board[1][0]
    if board[2][0] == board[2][1] == board[2][2]:
        return board[2][0]

    if board[0][0] == board[1][0] == board[2][0]:
        return board[0][0]
    if board[0][1] == board[1][1] == board[2][1]:
        return board[0][1]
    if board[0][2] == board[1][2] == board[2][2]:
        return board[0][2]

    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[2][0] == board[1][1] == board[0][2]:
        return board[2][0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    possible_actions = actions(board)
    # X wants to maximize score
    if player(board) == X:
        optimal_action = (None, -2)  # action, score
        for action in possible_actions:
            if max_value(result(board, action)) > optimal_action[1]:
                optimal_action = (action, max_value(result(board, action)))
        return optimal_action[0]
    # O wants to minimize score
    if player(board) == O:
        optimal_action = (None, 2)  # action, score
        for action in possible_actions:
            if min_value(result(board, action)) < optimal_action[1]:
                optimal_action = (action, min_value(result(board, action)))
        print(optimal_action)
        return optimal_action[0]


def max_value(board):
    if terminal(board):
        return utility(board)
    v = -2
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = 2
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v
