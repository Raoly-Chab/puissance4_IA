import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
EMPTY = 0
PLAYER_PIECE = 1
L_PIECE = 2
WINDOW_LENGTH = 4
L_DEPTH = 4

# --- Fonctions de plateau ---
def create_board():
    return [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT-1, -1, -1):
        if board[r][col] == 0:
            return r
    return None

def winning_move(board, piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if all(board[r+3-i][c+i] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    return False

# --- Évaluation heuristique ---
def evaluate_window(window, piece):
    opp_piece = PLAYER_PIECE if piece == L_PIECE else L_PIECE
    if window.count(piece) == 4:
        return 10000
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        return 50
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        return 10
    elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        return -80
    return 0

def score_position(board, piece):
    score = 0
    score += [board[r][COLUMN_COUNT//2] for r in range(ROW_COUNT)].count(piece) * 6
    for r in range(ROW_COUNT):
        row = board[r]
        for c in range(COLUMN_COUNT-3):
            score += evaluate_window(row[c:c+4], piece)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            score += evaluate_window([board[r+i][c] for i in range(4)], piece)
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            score += evaluate_window([board[r+3-i][c+i] for i in range(4)], piece)
            score += evaluate_window([board[r+i][c+i] for i in range(4)], piece)
    return score

# --- Minimax avec alpha-bêta ---
def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, L_PIECE) or not get_valid_locations(board)

def minimax(board, depth, alpha, beta, maximizing):
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)
    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, L_PIECE):
                return None, 1e14
            elif winning_move(board, PLAYER_PIECE):
                return None, -1e13
            else:
                return None, 0
        return None, score_position(board, L_PIECE)

    if maximizing:
        value, best_col = -math.inf, random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = [r[:] for r in board]
            drop_piece(b_copy, row, col, L_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value, best_col = new_score, col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value, best_col = math.inf, random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            if row is None:
                continue
            b_copy = [r[:] for r in board]
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value, best_col = new_score, col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value
