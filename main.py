import sys
import math
import pygame
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN

# Import depuis game_logic
from game_logic import (
    ROW_COUNT, COLUMN_COUNT,
    PLAYER_PIECE, L_PIECE,
    create_board, drop_piece, is_valid_location,
    get_next_open_row, winning_move, minimax, L_DEPTH
)

# --- Configurations graphiques ---
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

WIDTH = COLUMN_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)       # joueur
YELLOW = (255, 255, 0)  # IA

PLAYER = 0
AI = 1

# --- Fonctions graphiques ---
def draw_board(screen, board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (c*SQUARESIZE+SQUARESIZE//2, r*SQUARESIZE+SQUARESIZE+SQUARESIZE//2), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (c*SQUARESIZE+SQUARESIZE//2, (r+1)*SQUARESIZE+SQUARESIZE//2), RADIUS)
            elif board[r][c] == L_PIECE:
                pygame.draw.circle(screen, YELLOW, (c*SQUARESIZE+SQUARESIZE//2, (r+1)*SQUARESIZE+SQUARESIZE//2), RADIUS)
    pygame.display.update()

def animate_drop(screen, board, col, row, piece):
    x = col * SQUARESIZE + SQUARESIZE // 2
    y_start = SQUARESIZE // 2
    y_end = (row+1) * SQUARESIZE + SQUARESIZE // 2
    for y in range(y_start, y_end+1, 20):
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        draw_board(screen, board)
        color = RED if piece == PLAYER_PIECE else YELLOW
        pygame.draw.circle(screen, color, (x, y), RADIUS)
        pygame.display.update()
        pygame.time.delay(5)
    drop_piece(board, row, col, piece)

# --- Main loop ---
def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Puissance 4 - Humain vs IA')
    font = pygame.font.SysFont('monospace', 48)
    board = create_board()
    game_over, turn = False, PLAYER
    draw_board(screen, board)

    while not game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (event.pos[0], SQUARESIZE//2), RADIUS)
                pygame.display.update()
            if event.type == MOUSEBUTTONDOWN and turn == PLAYER and not game_over:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                col = event.pos[0] // SQUARESIZE
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    animate_drop(screen, board, col, row, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        screen.blit(font.render('Tu as été plus fort.', True, RED), (40, 10))
                        pygame.display.update(); game_over = True
                    turn = AI
        if turn == AI and not game_over:
            col, _ = minimax(board, L_DEPTH, -math.inf, math.inf, True)
            if col is None:
                screen.blit(font.render('Égalité. Rien de plus à dire.', True, (200, 200, 200)), (40, 10))
                pygame.display.update(); game_over = True
            else:
                row = get_next_open_row(board, col)
                animate_drop(screen, board, col, row, L_PIECE)
                if winning_move(board, L_PIECE):
                    screen.blit(font.render("Justice est rendue.", True, YELLOW), (40, 10))
                    pygame.display.update(); game_over = True
                turn = PLAYER
        draw_board(screen, board)
        if game_over:
            pygame.time.wait(3000)
            pygame.quit(); return

if __name__ == '__main__':
    main()
