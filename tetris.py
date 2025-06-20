import pygame
import sys
import random # For choosing random tetrominoes
from game_elements import Board, Tetromino # Import Tetromino
from settings import *

def get_random_tetromino_shape():
    return random.choice(list(Tetromino.SHAPES.keys()))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Font initialization
    score_font = pygame.font.Font(FONT_NAME, SCORE_FONT_SIZE)
    game_over_font = pygame.font.Font(FONT_NAME, GAME_OVER_FONT_SIZE)
    pause_font = pygame.font.Font(FONT_NAME, PAUSE_FONT_SIZE) # Use specific PAUSE_FONT_SIZE
    label_font = pygame.font.Font(FONT_NAME, LABEL_FONT_SIZE)

    # Game state variables
    board = None
    current_tetromino = None
    next_tetromino = None # For the preview block
    score = 0
    game_over = False
    paused = False

    # Scoring system
    LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}

    fall_speed = INITIAL_FALL_SPEED # Seconds per step
    FALL_EVENT = pygame.USEREVENT + 1 # Custom event for automatic falling

    def spawn_new_tetromino():
        nonlocal current_tetromino, next_tetromino, game_over
        if next_tetromino:
            current_tetromino = next_tetromino
        else: # First piece of the game
            current_tetromino = Tetromino(get_random_tetromino_shape(), board)

        next_tetromino = Tetromino(get_random_tetromino_shape(), board)

        if not board.is_valid_position(current_tetromino):
            game_over = True
            pygame.time.set_timer(FALL_EVENT, 0) # Stop falling on game over


    def reset_game():
        nonlocal board, score, game_over, paused, fall_speed, next_tetromino, current_tetromino
        board = Board()
        score = 0
        game_over = False
        paused = False
        fall_speed = INITIAL_FALL_SPEED
        next_tetromino = Tetromino(get_random_tetromino_shape(), board) # Initialize next for the first current
        spawn_new_tetromino() # This will set current_tetromino and the new next_tetromino
        pygame.time.set_timer(FALL_EVENT, int(fall_speed * 1000))

    reset_game() # Initialize game state

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Restart game
                    reset_game()
                elif event.key == pygame.K_p: # Pause/Unpause game
                    if not game_over: # Can only pause if game is not over
                        paused = not paused
                        if paused:
                            pygame.time.set_timer(FALL_EVENT, 0) # Stop falling when paused
                        else:
                            pygame.time.set_timer(FALL_EVENT, int(fall_speed * 1000)) # Resume falling

            if not game_over and not paused:
                if event.type == pygame.KEYDOWN: # Game controls
                    if event.key == pygame.K_LEFT:
                        if board.is_valid_position(current_tetromino, offset_x=-1):
                            current_tetromino.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if board.is_valid_position(current_tetromino, offset_x=1):
                            current_tetromino.x += 1
                    elif event.key == pygame.K_DOWN: # Soft drop
                        if board.is_valid_position(current_tetromino, offset_y=1):
                            current_tetromino.y += 1
                        else: # Landed due to soft drop
                            board.add_tetromino(current_tetromino)
                            lines_cleared = board.clear_lines()
                            if lines_cleared > 0:
                                score += LINE_SCORES.get(lines_cleared, 0)
                            spawn_new_tetromino()
                    elif event.key == pygame.K_UP: # Rotate
                        current_tetromino.rotate()
                    elif event.key == pygame.K_SPACE: # Hard drop
                        while board.is_valid_position(current_tetromino, offset_y=1):
                            current_tetromino.y += 1
                        board.add_tetromino(current_tetromino)
                        lines_cleared = board.clear_lines()
                        if lines_cleared > 0:
                            score += LINE_SCORES.get(lines_cleared, 0)
                        spawn_new_tetromino()

                if event.type == FALL_EVENT:
                    if board.is_valid_position(current_tetromino, offset_y=1):
                        current_tetromino.y += 1
                    else: # Tetromino has landed
                        board.add_tetromino(current_tetromino)
                        lines_cleared = board.clear_lines()
                        if lines_cleared > 0:
                            score += LINE_SCORES.get(lines_cleared, 0)
                        spawn_new_tetromino()

        screen.fill(BLACK)

        # Draw game board (this will be drawn on the left part of the screen)
        board.draw(screen)

        if not game_over:
            current_tetromino.draw(screen, board.block_size)
        else: # Display Game Over message
            # Adjust game over message position due to wider screen
            game_over_text_surface = game_over_font.render("Game Over", True, GAME_OVER_FONT_COLOR)
            final_score_text_surface = score_font.render(f"Final Score: {score}", True, SCORE_FONT_COLOR)
            restart_text_surface = score_font.render("Press 'R' to Restart", True, WHITE)

            center_x_board = GAME_BOARD_WIDTH // 2 # Center of the game board area for these messages

            game_over_rect = game_over_text_surface.get_rect(center=(center_x_board, SCREEN_HEIGHT // 2 - GAME_OVER_FONT_SIZE * 1.5))
            final_score_rect = final_score_text_surface.get_rect(center=(center_x_board, SCREEN_HEIGHT // 2))
            restart_rect = restart_text_surface.get_rect(center=(center_x_board, SCREEN_HEIGHT // 2 + GAME_OVER_FONT_SIZE * 1.5)) # Adjusted y based on GAME_OVER_FONT_SIZE

            screen.blit(game_over_text_surface, game_over_rect)
            screen.blit(final_score_text_surface, final_score_rect)
            screen.blit(restart_text_surface, restart_rect)

        if paused and not game_over:
            pause_text_surface = pause_font.render("Paused", True, WHITE)
            center_x_board = GAME_BOARD_WIDTH // 2 # Center of the game board area
            pause_rect = pause_text_surface.get_rect(center=(center_x_board, SCREEN_HEIGHT // 2))
            screen.blit(pause_text_surface, pause_rect)

        # --- Side Panel Rendering (Score and Preview) ---

        # Display current score
        score_surface = score_font.render(f"Score: {score}", True, SCORE_FONT_COLOR)
        score_display_rect = score_surface.get_rect(center=(SCORE_TEXT_X, SCORE_TEXT_Y))
        screen.blit(score_surface, score_display_rect)

        # Draw border/background for preview area
        preview_bg_rect = pygame.Rect(PREVIEW_AREA_X, PREVIEW_AREA_Y, PREVIEW_AREA_WIDTH, PREVIEW_AREA_HEIGHT)
        pygame.draw.rect(screen, PREVIEW_AREA_COLOR, preview_bg_rect) # Background
        pygame.draw.rect(screen, PREVIEW_BORDER_COLOR, preview_bg_rect, 2) # Border

        # Render "Next Block" label
        next_label_surface = label_font.render(NEXT_LABEL_TEXT, True, LABEL_FONT_COLOR)
        # Use NEXT_LABEL_X and NEXT_LABEL_Y from settings for precise positioning
        label_rect = next_label_surface.get_rect(center=(NEXT_LABEL_X, NEXT_LABEL_Y))
        screen.blit(next_label_surface, label_rect)

        if next_tetromino and not game_over:
            # Calculate position to draw the next_tetromino centered in the preview area
            # Make preview blocks smaller if the area is small, but not too small
            preview_block_scale = 0.75
            preview_block_size = int(BLOCK_SIZE * preview_block_scale)

            # Ensure tetromino shape is not empty before calculating its dimensions
            if next_tetromino.shape and len(next_tetromino.shape) > 0 and len(next_tetromino.shape[0]) > 0 :
                if PREVIEW_AREA_WIDTH < (len(next_tetromino.shape[0]) * preview_block_size) or \
                   PREVIEW_AREA_HEIGHT < (len(next_tetromino.shape) * preview_block_size) or \
                   preview_block_size <=0 : # ensure block size is positive

                    shape_cols = len(next_tetromino.shape[0])
                    shape_rows = len(next_tetromino.shape)

                    # Calculate block size based on fitting the shape into the preview area
                    block_size_w = PREVIEW_AREA_WIDTH // shape_cols if shape_cols > 0 else PREVIEW_AREA_WIDTH
                    block_size_h = PREVIEW_AREA_HEIGHT // shape_rows if shape_rows > 0 else PREVIEW_AREA_HEIGHT
                    preview_block_size = max(1, min(block_size_w, block_size_h)) # Ensure at least 1px

                shape_width = len(next_tetromino.shape[0]) * preview_block_size
                shape_height = len(next_tetromino.shape) * preview_block_size

                draw_x = PREVIEW_AREA_X + (PREVIEW_AREA_WIDTH - shape_width) // 2
                draw_y = PREVIEW_AREA_Y + (PREVIEW_AREA_HEIGHT - shape_height) // 2

                next_tetromino.draw_at(screen, draw_x, draw_y, preview_block_size)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
