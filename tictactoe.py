"""
Tic Tac Toe Player
"""

import math

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
    count_x = sum(row.count(X) for row in board)
    count_o = sum(row.count(O) for row in board)

    if count_x > count_o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] is not EMPTY:
        raise Exception("Invalid action")

    new_board = [row[:] for row in board]
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for mark in [X, O]:
        # Check rows
        if any(row == [mark] * 3 for row in board):
            return mark

        # Check columns
        if any(all(board[i][j] == mark for i in range(3)) for j in range(3)):
            return mark

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] == mark:
            return mark
        if board[0][2] == board[1][1] == board[2][0] == mark:
            return mark

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(all(cell is not EMPTY for cell in row) for row in board)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)
    opponent = O if current_player == X else X

    if terminal(board):
        return None

    best_action = None
    best_score = float('-inf') if current_player == X else float('inf')
    next_actions = actions(board)

    for action in next_actions:
        new_board = result(board, action)

        # Check if the new move results in a win for the current player
        if winner(new_board) == current_player:
            return action

        # Check if the new move results in a win for the opponent
        if winner(new_board) == opponent:
            continue

        # Check if the next move for the opponent leads to a win
        opponent_winning_move = False
        for opponent_action in actions(new_board):
            opponent_next_board = result(new_board, opponent_action)
            if winner(opponent_next_board) == opponent:
                opponent_winning_move = True
                break

        score = minimax_helper(new_board, current_player)

        if current_player == X and score > best_score:
            if not opponent_winning_move:
                best_score = score
                best_action = action
        elif current_player == O and score < best_score:
            if not opponent_winning_move:
                best_score = score
                best_action = action

    return best_action


def minimax_helper(board, player):
    """
    Returns the optimal score for the current player on the board.
    """
    if terminal(board):
        return utility(board)

    best_score = float('-inf') if player == X else float('inf')

    for action in actions(board):
        new_board = result(board, action)
        score = minimax_helper(new_board, player)

        if player == X:
            best_score = max(best_score, score)
        else:
            best_score = min(best_score, score)

    return best_score
