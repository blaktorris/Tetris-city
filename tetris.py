import pygame
import sys
import random # For choosing random tetrominoes
from game_elements import Board, Tetromino # Import Tetromino
from settings import *

def get_random_tetromino_shape():
    return random.choice(list(Tetromino.SHAPES.keys()))

def main():
    pygame.init() # Initialize Pygame modules

    # Initialize Pygame Mixer
    try:
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        print("Pygame mixer initialized successfully.")
    except pygame.error as e:
        print(f"Warning: Could not initialize Pygame mixer. {e}")
        # Optionally, set ENABLE_SOUND to False here if mixer is critical
        # settings.ENABLE_SOUND = False

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Font initialization
    score_font = pygame.font.Font(FONT_NAME, SCORE_FONT_SIZE)
    game_over_font = pygame.font.Font(FONT_NAME, GAME_OVER_FONT_SIZE)
    pause_font = pygame.font.Font(FONT_NAME, PAUSE_FONT_SIZE)
    label_font = pygame.font.Font(FONT_NAME, LABEL_FONT_SIZE)

    # Global Sound Variables (placeholders)
    # These are defined within main() so 'nonlocal' will be used in load_sounds()
    rotate_sound = None
    move_sound = None
    land_sound = None
    line_clear_sound = None
    tetris_clear_sound = None
    game_over_sound = None

    def load_sounds():
        nonlocal rotate_sound, move_sound, land_sound, line_clear_sound, tetris_clear_sound, game_over_sound

        sounds_enabled_by_setting = globals().get('ENABLE_SOUND', False)

        if not sounds_enabled_by_setting:
            # print("Sound loading skipped: ENABLE_SOUND is False or missing from settings.") # Optional print
            return
        if not pygame.mixer.get_init():
            # print("Sound loading skipped: Pygame mixer not initialized.") # Optional print
            return

        def _load_individual_sound(sound_constant_name):
            file_path = globals().get(sound_constant_name)
            if file_path:
                try:
                    return pygame.mixer.Sound(file_path)
                except pygame.error as e:
                    print(f"Warning: Pygame error loading sound '{file_path}' for {sound_constant_name}. {e}")
                except Exception as e:
                    print(f"Warning: Generic error loading sound '{file_path}' for {sound_constant_name}. {e}")
            elif sounds_enabled_by_setting: # Only warn if sounds were expected
                print(f"Warning: Sound file constant '{sound_constant_name}' not found or is None in settings.")
            return None

        rotate_sound = _load_individual_sound('ROTATE_SOUND_FILE')
        move_sound = _load_individual_sound('MOVE_SOUND_FILE')
        land_sound = _load_individual_sound('LAND_SOUND_FILE')
        line_clear_sound = _load_individual_sound('LINE_CLEAR_SOUND_FILE')
        tetris_clear_sound = _load_individual_sound('TETRIS_CLEAR_SOUND_FILE')
        game_over_sound = _load_individual_sound('GAME_OVER_SOUND_FILE')

        # Load background music
        music_constant_name = 'BACKGROUND_MUSIC_FILE'
        music_file_path = globals().get(music_constant_name)
        if music_file_path:
            try:
                pygame.mixer.music.load(music_file_path)
                # print(f"Background music '{music_file_path}' loaded successfully.") # Optional print
                pygame.mixer.music.play(-1) # Loop indefinitely
            except pygame.error as e:
                print(f"Warning: Pygame error with background music '{music_file_path}'. {e}")
            except Exception as e:
                print(f"Warning: Generic error with background music '{music_file_path}'. {e}")
        elif sounds_enabled_by_setting: # Only warn if sounds were expected
            print(f"Warning: Background music constant '{music_constant_name}' not found or is None in settings.")

    load_sounds()

    # Game state variables
    board = None
    current_tetromino = None
    next_tetromino = None
    score = 0
    game_over = False
    paused = False
    music_playing = globals().get('ENABLE_SOUND', False) and pygame.mixer.get_init() and pygame.mixer.music.get_busy()


    # Scoring system
    LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}

    fall_speed = INITIAL_FALL_SPEED
    FALL_EVENT = pygame.USEREVENT + 1

    def play_sound(sound_object):
        sounds_enabled_by_setting = globals().get('ENABLE_SOUND', False)
        if sounds_enabled_by_setting and sound_object and pygame.mixer.get_init():
            sound_object.play()

    def handle_landing():
        """Logic for when a tetromino lands."""
        nonlocal score, game_over
        play_sound(land_sound)
        board.add_tetromino(current_tetromino)
        lines_cleared = board.clear_lines()
        if lines_cleared > 0:
            score += LINE_SCORES.get(lines_cleared, 0)
            if lines_cleared == 4:
                play_sound(tetris_clear_sound)
            else:
                play_sound(line_clear_sound)
        spawn_new_tetromino()


    def spawn_new_tetromino():
        nonlocal current_tetromino, next_tetromino, game_over, music_playing
        if next_tetromino:
            current_tetromino = next_tetromino
        else:
            current_tetromino = Tetromino(get_random_tetromino_shape(), board)

        next_tetromino = Tetromino(get_random_tetromino_shape(), board)

        if not board.is_valid_position(current_tetromino):
            game_over = True
            play_sound(game_over_sound)
            pygame.time.set_timer(FALL_EVENT, 0)
            if music_playing: # Stop music on game over
                pygame.mixer.music.stop()
                # music_playing = False # Not strictly needed to set here as reset_game will handle it


    def reset_game():
        nonlocal board, score, game_over, paused, fall_speed, next_tetromino, current_tetromino, music_playing
        board = Board()
        score = 0
        game_over = False
        paused = False
        fall_speed = INITIAL_FALL_SPEED
        next_tetromino = Tetromino(get_random_tetromino_shape(), board)
        spawn_new_tetromino()
        pygame.time.set_timer(FALL_EVENT, int(fall_speed * 1000))

        if globals().get('ENABLE_SOUND', False) and pygame.mixer.get_init():
            try:
                # Ensure music is loaded before trying to play. load_sounds() should have handled this.
                # If music was stopped, play it again.
                pygame.mixer.music.play(-1) # Loop indefinitely
                music_playing = True
            except pygame.error as e:
                print(f"Warning: Could not play music on reset. {e}")
                music_playing = False
        else:
            music_playing = False


    reset_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_p:
                    if not game_over:
                        paused = not paused
                        if paused:
                            pygame.time.set_timer(FALL_EVENT, 0)
                            if music_playing: pygame.mixer.music.pause() # Pause music with game
                        else:
                            pygame.time.set_timer(FALL_EVENT, int(fall_speed * 1000))
                            if music_playing: pygame.mixer.music.unpause() # Resume music
                elif event.key == pygame.K_m: # Mute/Unmute toggle
                    if globals().get('ENABLE_SOUND', False) and pygame.mixer.get_init():
                        if music_playing:
                            pygame.mixer.music.pause()
                            music_playing = False
                        else:
                            # Before unpausing, ensure music is loaded and was playing or is ready to play
                            # This handles case where music might not have started if game started muted somehow
                            # or if it was stopped explicitly.
                            # A simple unpause might be enough if play(-1) was already called.
                            pygame.mixer.music.unpause()
                            # If music was stopped entirely (not just paused), unpause won't resume.
                            # We might need to call play() again if it was stopped.
                            # For now, assuming pause/unpause is sufficient if music was initially started.
                            if not pygame.mixer.music.get_busy(): # If it wasn't just paused, but stopped
                                pygame.mixer.music.play(-1) # Re-play it
                            music_playing = True

            if not game_over and not paused:
                if event.type == pygame.KEYDOWN: # Game controls
                    if event.key == pygame.K_LEFT:
                        if board.is_valid_position(current_tetromino, offset_x=-1):
                            current_tetromino.x -= 1
                            play_sound(move_sound)
                    elif event.key == pygame.K_RIGHT:
                        if board.is_valid_position(current_tetromino, offset_x=1):
                            current_tetromino.x += 1
                            play_sound(move_sound)
                    elif event.key == pygame.K_DOWN: # Soft drop
                        if board.is_valid_position(current_tetromino, offset_y=1):
                            current_tetromino.y += 1
                            play_sound(move_sound) # Sound for soft drop movement
                        else: # Landed due to soft drop
                            handle_landing()
                    elif event.key == pygame.K_UP: # Rotate
                        # Store original shape and position for rotation check
                        original_shape_for_sound = current_tetromino.shape
                        current_tetromino.rotate()
                        if current_tetromino.shape != original_shape_for_sound: # Play sound if rotation actually happened
                            play_sound(rotate_sound)
                    elif event.key == pygame.K_SPACE: # Hard drop
                        # Play move sound for each step of hard drop for dramatic effect, or just one land sound.
                        # For simplicity here, we'll play land sound once via handle_landing.
                        # If you want sound per step:
                        # while board.is_valid_position(current_tetromino, offset_y=1):
                        #    current_tetromino.y += 1
                        #    # play_sound(move_sound) # This could be too much
                        # Instead, just move it to the bottom:
                        while board.is_valid_position(current_tetromino, offset_y=1):
                            current_tetromino.y += 1
                        handle_landing()

                if event.type == FALL_EVENT:
                    if board.is_valid_position(current_tetromino, offset_y=1):
                        current_tetromino.y += 1
                    else: # Tetromino has landed
                        handle_landing()

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

        # Safely get display settings for preview, with defaults
        _BLOCK_SIZE = globals().get('BLOCK_SIZE', 30)
        _PREVIEW_AREA_X = globals().get('PREVIEW_AREA_X', GAME_BOARD_WIDTH + 10) # Default X if not in settings
        _PREVIEW_AREA_Y = globals().get('PREVIEW_AREA_Y', 50) # Default Y
        _PREVIEW_AREA_WIDTH = globals().get('PREVIEW_AREA_WIDTH', 130)
        _PREVIEW_AREA_HEIGHT = globals().get('PREVIEW_AREA_HEIGHT', 100)
        _PREVIEW_AREA_COLOR = globals().get('PREVIEW_AREA_COLOR', (20,20,20))
        _PREVIEW_BORDER_COLOR = globals().get('PREVIEW_BORDER_COLOR', (50,50,50))
        _NEXT_LABEL_TEXT = globals().get('NEXT_LABEL_TEXT', "Next:")
        _NEXT_LABEL_X = globals().get('NEXT_LABEL_X', _PREVIEW_AREA_X + _PREVIEW_AREA_WIDTH // 2)
        _NEXT_LABEL_Y = globals().get('NEXT_LABEL_Y', _PREVIEW_AREA_Y - 15) # Adjust based on font size if possible

        # Ensure numeric types for calculations
        if not isinstance(_BLOCK_SIZE, (int, float)): _BLOCK_SIZE = 30
        if not isinstance(_PREVIEW_AREA_WIDTH, (int, float)): _PREVIEW_AREA_WIDTH = 100
        if not isinstance(_PREVIEW_AREA_HEIGHT, (int, float)): _PREVIEW_AREA_HEIGHT = 100
        if not isinstance(_PREVIEW_AREA_X, (int, float)): _PREVIEW_AREA_X = GAME_BOARD_WIDTH + 10
        if not isinstance(_PREVIEW_AREA_Y, (int, float)): _PREVIEW_AREA_Y = 50
        if not isinstance(_NEXT_LABEL_X, (int, float)): _NEXT_LABEL_X = _PREVIEW_AREA_X + _PREVIEW_AREA_WIDTH // 2
        if not isinstance(_NEXT_LABEL_Y, (int, float)): _NEXT_LABEL_Y = _PREVIEW_AREA_Y -15


        # Display current score (using safe access for its position constants too)
        _SCORE_TEXT_X = globals().get('SCORE_TEXT_X', SCREEN_WIDTH - SIDE_PANEL_WIDTH // 2) # Example default
        _SCORE_TEXT_Y = globals().get('SCORE_TEXT_Y', 30) # Example default
        if not isinstance(_SCORE_TEXT_X, (int, float)): _SCORE_TEXT_X = SCREEN_WIDTH - SIDE_PANEL_WIDTH // 2
        if not isinstance(_SCORE_TEXT_Y, (int, float)): _SCORE_TEXT_Y = 30

        score_surface = score_font.render(f"Score: {score}", True, SCORE_FONT_COLOR)
        score_display_rect = score_surface.get_rect(center=(_SCORE_TEXT_X, _SCORE_TEXT_Y))
        screen.blit(score_surface, score_display_rect)

        # Draw border/background for preview area
        preview_bg_rect = pygame.Rect(_PREVIEW_AREA_X, _PREVIEW_AREA_Y, _PREVIEW_AREA_WIDTH, _PREVIEW_AREA_HEIGHT)
        pygame.draw.rect(screen, _PREVIEW_AREA_COLOR, preview_bg_rect)
        pygame.draw.rect(screen, _PREVIEW_BORDER_COLOR, preview_bg_rect, 2)

        # Render "Next Block" label
        next_label_surface = label_font.render(_NEXT_LABEL_TEXT, True, LABEL_FONT_COLOR)
        label_rect = next_label_surface.get_rect(center=(_NEXT_LABEL_X, _NEXT_LABEL_Y))
        screen.blit(next_label_surface, label_rect)

        if next_tetromino and not game_over:
            valid_shape = False
            if next_tetromino.shape and isinstance(next_tetromino.shape, list) and len(next_tetromino.shape) > 0:
                if isinstance(next_tetromino.shape[0], list) and len(next_tetromino.shape[0]) > 0:
                    valid_shape = True

            if valid_shape:
                preview_block_scale = 0.75
                preview_block_size = int(_BLOCK_SIZE * preview_block_scale)

                shape_cols = len(next_tetromino.shape[0])
                shape_rows = len(next_tetromino.shape)

                if _PREVIEW_AREA_WIDTH < (shape_cols * preview_block_size) or \
                   _PREVIEW_AREA_HEIGHT < (shape_rows * preview_block_size) or \
                   preview_block_size <= 0:

                    block_size_w = _PREVIEW_AREA_WIDTH // shape_cols if shape_cols > 0 else _PREVIEW_AREA_WIDTH
                    block_size_h = _PREVIEW_AREA_HEIGHT // shape_rows if shape_rows > 0 else _PREVIEW_AREA_HEIGHT
                    preview_block_size = max(1, min(block_size_w, block_size_h))

                shape_width = shape_cols * preview_block_size
                shape_height = shape_rows * preview_block_size

                draw_x = _PREVIEW_AREA_X + (_PREVIEW_AREA_WIDTH - shape_width) // 2
                draw_y = _PREVIEW_AREA_Y + (_PREVIEW_AREA_HEIGHT - shape_height) // 2

                next_tetromino.draw_at(screen, draw_x, draw_y, preview_block_size)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
