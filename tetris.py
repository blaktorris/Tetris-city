import pygame
import sys
import random # For choosing random tetrominoes
from game_elements import Board, Tetromino # Import Tetromino
from settings import *

def get_random_tetromino_shape():
    return random.choice(list(Tetromino.SHAPES.keys()))

def main():
import math # For particle calculations, if needed for more complex motion

# Particle Class
class Particle:
    def __init__(self, x, y, color, lifespan, size, velocity_x_range, velocity_y_range):
        self.x = x
        self.y = y
        self.color = color
        self.lifespan = lifespan
        self.size = size
        # Random velocity for a spray effect
        self.vx = random.uniform(velocity_x_range[0], velocity_x_range[1])
        self.vy = random.uniform(velocity_y_range[0], velocity_y_range[1])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= 1
        # Optional: Add gravity or fade color/size
        # self.vy += 0.1 # Example gravity

    def draw(self, screen):
        if self.lifespan > 0:
            # Draw as a small circle or square
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            # Or: pygame.draw.rect(screen, self.color, (self.x - self.size//2, self.y - self.size//2, self.size, self.size))


def get_random_tetromino_shape():
    return random.choice(list(Tetromino.SHAPES.keys()))

def main():
def get_ghost_piece_y(tetromino, board):
    """Calculates the Y board coordinate for where the ghost piece should be."""
    if not tetromino: return tetromino.y # Should not happen if called correctly

    # Create a temporary copy or use offsets carefully if Tetromino object state is mutable during checks
    # For this function, we assume direct checks on board.is_valid_position with offsets are fine.
    # The tetromino's own x,y are grid coordinates.

    current_drop_offset = 0
    # Check validity one step below the current position + current_drop_offset
    while board.is_valid_position(tetromino, offset_x=0, offset_y=current_drop_offset + 1):
        current_drop_offset += 1
    return tetromino.y + current_drop_offset


def get_random_tetromino_shape():
    return random.choice(list(Tetromino.SHAPES.keys()))

def main():
def get_ghost_piece_y(tetromino, board):
    """Calculates the Y board coordinate for where the ghost piece should be."""
    if not tetromino: return tetromino.y

    current_drop_offset = 0
    while board.is_valid_position(tetromino, offset_x=0, offset_y=current_drop_offset + 1):
        current_drop_offset += 1
    return tetromino.y + current_drop_offset

# main function needs to be defined after Particle and get_ghost_piece_y
# if they are not methods of a class imported elsewhere.
# For now, assuming they are helper functions accessible by main.

def get_random_tetromino_shape():
    return random.choice(list(Tetromino.SHAPES.keys()))

def main():
# FloatingScore Class
class FloatingScore:
    def __init__(self, x, y, points_text, font, color, lifespan, speed_y):
        self.x = x
        self.y = y
        self.points_text = points_text
        self.font = font
        self.color = color
        self.lifespan = lifespan
        self.initial_lifespan = lifespan
        self.speed_y = speed_y
        self.alpha = 255
        # Initial render can be done here, but if color/alpha changes, it needs re-render or set_alpha
        # self.surface = self.font.render(self.points_text, True, self.color)

    def update(self):
        self.y += self.speed_y
        self.lifespan -= 1
        self.alpha = max(0, int((self.lifespan / self.initial_lifespan) * 255))

    def draw(self, surface_to_draw_on):
        if self.lifespan > 0:
            # Re-render each time to handle alpha correctly for text
            temp_surface = self.font.render(self.points_text, True, self.color)
            temp_surface.set_alpha(self.alpha)
            # Adjust x position to center the text based on its width
            text_width = temp_surface.get_width()
            surface_to_draw_on.blit(temp_surface, (self.x - text_width // 2, self.y))


def get_ghost_piece_y(tetromino, board):
    """Calculates the Y board coordinate for where the ghost piece should be."""
    if not tetromino: return tetromino.y

    current_drop_offset = 0
    while board.is_valid_position(tetromino, offset_x=0, offset_y=current_drop_offset + 1):
        current_drop_offset += 1
    return tetromino.y + current_drop_offset

# main function needs to be defined after Particle and get_ghost_piece_y
# if they are not methods of a class imported elsewhere.
# For now, assuming they are helper functions accessible by main.

def get_random_tetromino_shape():
    return random.choice(list(Tetromino.SHAPES.keys()))

def main():
# Placed at the top level of tetris.py
# from settings import * # This is already at the top of the file

def calculate_cumulative_points_for_level(target_level_number):
    """
    Calculates the total cumulative score needed to reach the specified target_level_number.
    Level 1 is reached at 0 points.
    """
    if target_level_number <= 1:
        return 0

    # Points to reach Level 2 is the base
    # This is the 'delta' needed to get from L(i-1) to L(i)
    # The first delta (L1 to L2) is BASE_POINTS_FOR_NEXT_LEVEL_INCREMENT
    current_delta_needed = BASE_POINTS_FOR_NEXT_LEVEL_INCREMENT
    cumulative_points = current_delta_needed # This is points to reach L2

    if target_level_number == 2:
        return cumulative_points

    # Calculate for levels beyond Level 2 (i.e., for reaching L3, L4, ...)
    for level_to_reach in range(3, target_level_number + 1):
        # The 'delta' to get from L(i-1) to L(i) increases
        current_delta_needed += ADDITIONAL_POINTS_INCREMENT_STEP
        cumulative_points += current_delta_needed

    return cumulative_points


# Particle Class
class Particle:
    def __init__(self, x, y, color, lifespan, size, velocity_x_range, velocity_y_range):
        self.x = x
        self.y = y
        self.color = color
        self.lifespan = lifespan
        self.size = size
        # Random velocity for a spray effect
        self.vx = random.uniform(velocity_x_range[0], velocity_x_range[1])
        self.vy = random.uniform(velocity_y_range[0], velocity_y_range[1])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifespan -= 1
        # Optional: Add gravity or fade color/size
        # self.vy += 0.1 # Example gravity

    def draw(self, screen):
        if self.lifespan > 0:
            # Draw as a small circle or square
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            # Or: pygame.draw.rect(screen, self.color, (self.x - self.size//2, self.y - self.size//2, self.size, self.size))


def get_random_tetromino_shape():
    return random.choice(list(Tetromino.SHAPES.keys()))

def main():
def get_ghost_piece_y(tetromino, board):
    """Calculates the Y board coordinate for where the ghost piece should be."""
    if not tetromino: return tetromino.y

    current_drop_offset = 0
    while board.is_valid_position(tetromino, offset_x=0, offset_y=current_drop_offset + 1):
        current_drop_offset += 1
    return tetromino.y + current_drop_offset

# main function needs to be defined after Particle and get_ghost_piece_y
# if they are not methods of a class imported elsewhere.
# For now, assuming they are helper functions accessible by main.

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
    floating_score_font = pygame.font.Font(FONT_NAME, FLOATING_SCORE_FONT_SIZE)
    level_font = pygame.font.Font(FONT_NAME, LEVEL_FONT_SIZE)


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
    particles = []
    floating_scores = []

    # Leveling System Variables
    current_level = 1
    points_to_reach_next_level_goal = calculate_cumulative_points_for_level(current_level + 1)
    current_fall_speed_seconds = INITIAL_FALL_SPEED_SECONDS

    # Screen Shake State
    screen_shake_timer = 0
    screen_shake_intensity = 0
    game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


    # Scoring system
    LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}

    # Fall event setup
    FALL_EVENT = pygame.USEREVENT + 1

    def trigger_screen_shake(duration, intensity_val):
        nonlocal screen_shake_timer, screen_shake_intensity
        # Don't interrupt a stronger or longer shake with a weaker/shorter one
        if duration > screen_shake_timer or intensity_val > screen_shake_intensity:
           screen_shake_timer = duration
           screen_shake_intensity = intensity_val

    def play_sound(sound_object):
        sounds_enabled_by_setting = globals().get('ENABLE_SOUND', False)
        if sounds_enabled_by_setting and sound_object and pygame.mixer.get_init():
            sound_object.play()

    def handle_landing():
        """Logic for when a tetromino lands."""
        nonlocal score, game_over, floating_scores, current_level, points_to_reach_next_level_goal, current_fall_speed_seconds
        play_sound(land_sound)
        board.add_tetromino(current_tetromino)

        lines_marked_for_clearing = board.clear_lines()

        if lines_marked_for_clearing > 0:
            points_earned_this_turn = LINE_SCORES.get(lines_marked_for_clearing, 0)
            score += points_earned_this_turn

            _score_text_x_safe = globals().get('SCORE_TEXT_X', SCREEN_WIDTH // 2)
            _score_text_y_safe = globals().get('SCORE_TEXT_Y', 30)
            if not isinstance(_score_text_x_safe, (int,float)): _score_text_x_safe = SCREEN_WIDTH // 2
            if not isinstance(_score_text_y_safe, (int,float)): _score_text_y_safe = 30
            spawn_x = _score_text_x_safe
            spawn_y = _score_text_y_safe + floating_score_font.get_height()
            new_floating_score = FloatingScore(
                spawn_x, spawn_y, f"+{points_earned_this_turn}",
                floating_score_font, FLOATING_SCORE_COLOR,
                FLOATING_SCORE_LIFESPAN, FLOATING_SCORE_SPEED_Y
            )
            floating_scores.append(new_floating_score)

            if lines_marked_for_clearing == 4:
                play_sound(tetris_clear_sound)
            else:
                play_sound(line_clear_sound)

            # Check for level up
            while score >= points_to_reach_next_level_goal and current_level < MAX_LEVEL:
                current_level += 1
                points_to_reach_next_level_goal = calculate_cumulative_points_for_level(current_level + 1)

                new_speed = INITIAL_FALL_SPEED_SECONDS * (FALL_SPEED_MULTIPLIER_PER_LEVEL ** (current_level - 1))
                current_fall_speed_seconds = max(MIN_FALL_SPEED_SECONDS, new_speed)

                pygame.time.set_timer(FALL_EVENT, 0)
                pygame.time.set_timer(FALL_EVENT, int(current_fall_speed_seconds * 1000))

                print(f"Level Up! Reached Level {current_level}. Next goal: {points_to_reach_next_level_goal} pts. Speed: {current_fall_speed_seconds:.3f}s")

        if lines_marked_for_clearing == 0:
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
        nonlocal board, score, game_over, paused, next_tetromino, current_tetromino, music_playing
        nonlocal current_level, points_to_reach_next_level_goal, current_fall_speed_seconds
        board = Board()
        score = 0
        game_over = False
        paused = False

        # Reset leveling variables
        current_level = 1
        current_fall_speed_seconds = INITIAL_FALL_SPEED_SECONDS
        points_to_reach_next_level_goal = calculate_cumulative_points_for_level(current_level + 1)

        next_tetromino = Tetromino(get_random_tetromino_shape(), board)
        spawn_new_tetromino()
        pygame.time.set_timer(FALL_EVENT, int(current_fall_speed_seconds * 1000))

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
    # Fall timer might need to be managed if line clear animation pauses game ticks
    is_fall_timer_active = True

    running = True
    while running:
        # Manage fall timer based on board animation state
        if board.line_clear_animation_timer > 0 and is_fall_timer_active:
            pygame.time.set_timer(FALL_EVENT, 0)
            is_fall_timer_active = False
        elif board.line_clear_animation_timer == 0 and not is_fall_timer_active and not game_over and not paused:
            pygame.time.set_timer(FALL_EVENT, int(current_fall_speed_seconds * 1000)) # Use current_fall_speed_seconds
            is_fall_timer_active = True

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
                            is_fall_timer_active = False
                            if music_playing: pygame.mixer.music.pause()
                        else:
                            pygame.time.set_timer(FALL_EVENT, int(current_fall_speed_seconds * 1000)) # Use current_fall_speed_seconds
                            is_fall_timer_active = True
                            if music_playing: pygame.mixer.music.unpause()
                elif event.key == pygame.K_m:
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

            if not game_over and not paused and board.line_clear_animation_timer == 0: # Process game logic only if no animation
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if board.is_valid_position(current_tetromino, offset_x=-1):
                            current_tetromino.x -= 1
                            play_sound(move_sound)
                    elif event.key == pygame.K_RIGHT:
                        if board.is_valid_position(current_tetromino, offset_x=1):
                            current_tetromino.x += 1
                            play_sound(move_sound)
                    elif event.key == pygame.K_DOWN:
                        if board.is_valid_position(current_tetromino, offset_y=1):
                            current_tetromino.y += 1
                            play_sound(move_sound)
                        else:
                            handle_landing()
                    elif event.key == pygame.K_UP:
                        original_shape_for_sound = current_tetromino.shape
                        current_tetromino.rotate()
                        if current_tetromino.shape != original_shape_for_sound:
                            play_sound(rotate_sound)
                    elif event.key == pygame.K_SPACE:
                        original_y = current_tetromino.y
                        while board.is_valid_position(current_tetromino, offset_y=1):
                            current_tetromino.y += 1
                        if current_tetromino.y > original_y: # If it actually moved
                            trigger_screen_shake(SCREEN_SHAKE_DURATION_HARD_DROP, SCREEN_SHAKE_INTENSITY_HARD_DROP)
                        handle_landing()

                if event.type == FALL_EVENT and is_fall_timer_active:
                    if board.is_valid_position(current_tetromino, offset_y=1):
                        current_tetromino.y += 1
                    else:
                        handle_landing()

        clearing_finished, particle_details_for_creation, num_lines_cleared_this_cycle = board.update_animations()
        if clearing_finished:
            is_tetris_clear = (num_lines_cleared_this_cycle == 4)
            if is_tetris_clear:
                 trigger_screen_shake(SCREEN_SHAKE_DURATION_TETRIS, SCREEN_SHAKE_INTENSITY_TETRIS)

            for p_data in particle_details_for_creation:
                world_x, world_y, block_color = p_data

                num_particles_to_create = PARTICLE_COUNT_PER_BLOCK
                current_lifespan = PARTICLE_LIFESPAN
                current_size = PARTICLE_SIZE
                current_color = TETRIS_PARTICLE_COLOR_OVERRIDE if (is_tetris_clear and TETRIS_PARTICLE_COLOR_OVERRIDE) else block_color

                if is_tetris_clear:
                    num_particles_to_create *= TETRIS_PARTICLE_COUNT_MULTIPLIER
                    current_lifespan *= TETRIS_PARTICLE_LIFESPAN_MULTIPLIER
                    current_size *= TETRIS_PARTICLE_SIZE_MULTIPLIER

                current_size = int(current_size)
                current_lifespan = int(current_lifespan)

                for _ in range(num_particles_to_create):
                    particles.append(Particle(
                        x = world_x + (BLOCK_SIZE // 2),
                        y = world_y + (BLOCK_SIZE // 2),
                        color = current_color,
                        lifespan = current_lifespan,
                        size = current_size,
                        velocity_x_range = PARTICLE_VELOCITY_RANGE_X,
                        velocity_y_range = PARTICLE_VELOCITY_RANGE_Y
                    ))

            spawn_new_tetromino()
            if not game_over and not paused:
                 pygame.time.set_timer(FALL_EVENT, int(current_fall_speed_seconds * 1000)) # Use current_fall_speed_seconds
                 is_fall_timer_active = True

        game_surface.fill(BLACK)

        board.draw(game_surface)

        if not game_over and not paused and current_tetromino and board.line_clear_animation_timer == 0:
            ghost_y = get_ghost_piece_y(current_tetromino, board)
            _GHOST_ALPHA = globals().get('GHOST_PIECE_ALPHA', 100)
            if not isinstance(_GHOST_ALPHA, int) or not (0 <= _GHOST_ALPHA <= 255): _GHOST_ALPHA = 100
            _GHOST_OUTLINE = globals().get('GHOST_PIECE_OUTLINE_THICKNESS', 1)
            if not isinstance(_GHOST_OUTLINE, int) or _GHOST_OUTLINE < 0: _GHOST_OUTLINE = 1

            for r_idx, row in enumerate(current_tetromino.shape):
                for c_idx, cell in enumerate(row):
                    if cell:
                        draw_x = (current_tetromino.x + c_idx) * board.block_size
                        draw_y = (ghost_y + r_idx) * board.block_size
                        block_surface = pygame.Surface((board.block_size, board.block_size), pygame.SRCALPHA)
                        ghost_color_r = max(0, current_tetromino.color[0] - 50)
                        ghost_color_g = max(0, current_tetromino.color[1] - 50)
                        ghost_color_b = max(0, current_tetromino.color[2] - 50)
                        final_ghost_color_tuple = (ghost_color_r, ghost_color_g, ghost_color_b, _GHOST_ALPHA)
                        if _GHOST_OUTLINE > 0:
                            pygame.draw.rect(block_surface, final_ghost_color_tuple,
                                             (0,0, board.block_size, board.block_size), _GHOST_OUTLINE)
                        else:
                            block_surface.fill(final_ghost_color_tuple)
                        game_surface.blit(block_surface, (draw_x, draw_y))

        if not game_over and board.line_clear_animation_timer == 0 :
            current_tetromino.draw(game_surface, board.block_size)
        elif not game_over and current_tetromino:
            is_overlapping_flash = False
            if board.lines_to_clear_animation:
                flashing_rows = {anim_data['index'] for anim_data in board.lines_to_clear_animation}
                for r_idx, row_data in enumerate(current_tetromino.shape):
                    for c_idx, cell in enumerate(row_data):
                        if cell:
                            if (current_tetromino.y + r_idx) in flashing_rows:
                                is_overlapping_flash = True
                                break
                    if is_overlapping_flash:
                        break
            if not is_overlapping_flash:
                 current_tetromino.draw(game_surface, board.block_size)

        for particle in particles[:]:
            particle.update()
            particle.draw(game_surface)
            if particle.lifespan <= 0:
                particles.remove(particle)

        # Update and draw floating scores
        for fs in floating_scores[:]: # Iterate over a slice copy for safe removal
            fs.update()
            fs.draw(game_surface)
            if fs.lifespan <= 0:
                floating_scores.remove(fs)

        if game_over:
            game_over_text_surface = game_over_font.render("Game Over", True, GAME_OVER_FONT_COLOR)
            final_score_text_surface = score_font.render(f"Final Score: {score}", True, SCORE_FONT_COLOR)
            restart_text_surface = score_font.render("Press 'R' to Restart", True, WHITE)
            center_x_board = GAME_BOARD_WIDTH // 2
            game_over_rect = game_over_text_surface.get_rect(center=(center_x_board, SCREEN_HEIGHT // 2 - GAME_OVER_FONT_SIZE * 1.5))
            final_score_rect = final_score_text_surface.get_rect(center=(center_x_board, SCREEN_HEIGHT // 2))
            restart_rect = restart_text_surface.get_rect(center=(center_x_board, SCREEN_HEIGHT // 2 + GAME_OVER_FONT_SIZE * 1.5))
            game_surface.blit(game_over_text_surface, game_over_rect)
            game_surface.blit(final_score_text_surface, final_score_rect)
            game_surface.blit(restart_text_surface, restart_rect)

        if paused and not game_over:
            pause_text_surface = pause_font.render("Paused", True, WHITE)
            center_x_board = GAME_BOARD_WIDTH // 2
            pause_rect = pause_text_surface.get_rect(center=(center_x_board, SCREEN_HEIGHT // 2))
            game_surface.blit(pause_text_surface, pause_rect)

        _BLOCK_SIZE = globals().get('BLOCK_SIZE', 30)
        _PREVIEW_AREA_X = globals().get('PREVIEW_AREA_X', GAME_BOARD_WIDTH + 10)
        _PREVIEW_AREA_Y = globals().get('PREVIEW_AREA_Y', 50)
        _PREVIEW_AREA_WIDTH = globals().get('PREVIEW_AREA_WIDTH', 130)
        _PREVIEW_AREA_HEIGHT = globals().get('PREVIEW_AREA_HEIGHT', 100)
        _PREVIEW_AREA_COLOR = globals().get('PREVIEW_AREA_COLOR', (20,20,20))
        _PREVIEW_BORDER_COLOR = globals().get('PREVIEW_BORDER_COLOR', (50,50,50))
        _NEXT_LABEL_TEXT = globals().get('NEXT_LABEL_TEXT', "Next:")
        _NEXT_LABEL_X = globals().get('NEXT_LABEL_X', _PREVIEW_AREA_X + _PREVIEW_AREA_WIDTH // 2)
        _NEXT_LABEL_Y = globals().get('NEXT_LABEL_Y', _PREVIEW_AREA_Y - 15)

        if not isinstance(_BLOCK_SIZE, (int, float)): _BLOCK_SIZE = 30
        if not isinstance(_PREVIEW_AREA_WIDTH, (int, float)): _PREVIEW_AREA_WIDTH = 100
        if not isinstance(_PREVIEW_AREA_HEIGHT, (int, float)): _PREVIEW_AREA_HEIGHT = 100
        if not isinstance(_PREVIEW_AREA_X, (int, float)): _PREVIEW_AREA_X = GAME_BOARD_WIDTH + 10
        if not isinstance(_PREVIEW_AREA_Y, (int, float)): _PREVIEW_AREA_Y = 50
        if not isinstance(_NEXT_LABEL_X, (int, float)): _NEXT_LABEL_X = _PREVIEW_AREA_X + _PREVIEW_AREA_WIDTH // 2
        if not isinstance(_NEXT_LABEL_Y, (int, float)): _NEXT_LABEL_Y = _PREVIEW_AREA_Y -15

        _SCORE_TEXT_X = globals().get('SCORE_TEXT_X', SCREEN_WIDTH - SIDE_PANEL_WIDTH // 2)
        _SCORE_TEXT_Y = globals().get('SCORE_TEXT_Y', 30)
        if not isinstance(_SCORE_TEXT_X, (int, float)): _SCORE_TEXT_X = SCREEN_WIDTH - SIDE_PANEL_WIDTH // 2
        if not isinstance(_SCORE_TEXT_Y, (int, float)): _SCORE_TEXT_Y = 30

        score_surface = score_font.render(f"Score: {score}", True, SCORE_FONT_COLOR)
        score_display_rect = score_surface.get_rect(center=(_SCORE_TEXT_X, _SCORE_TEXT_Y))
        game_surface.blit(score_surface, score_display_rect)

        # Display current Level
        _LEVEL_TEXT_X = globals().get('LEVEL_TEXT_X', SCREEN_WIDTH - SIDE_PANEL_WIDTH // 2) # Default if missing
        _LEVEL_TEXT_Y = globals().get('LEVEL_TEXT_Y', _SCORE_TEXT_Y + 30) # Default below score
        if not isinstance(_LEVEL_TEXT_X, (int, float)): _LEVEL_TEXT_X = SCREEN_WIDTH - SIDE_PANEL_WIDTH // 2
        if not isinstance(_LEVEL_TEXT_Y, (int, float)): _LEVEL_TEXT_Y = _SCORE_TEXT_Y + 30

        level_text_surface = level_font.render(f"{LEVEL_LABEL_TEXT} {current_level}", True, LEVEL_TEXT_COLOR)
        level_rect = level_text_surface.get_rect(center=(_LEVEL_TEXT_X, _LEVEL_TEXT_Y))
        game_surface.blit(level_text_surface, level_rect)


        preview_bg_rect = pygame.Rect(_PREVIEW_AREA_X, _PREVIEW_AREA_Y, _PREVIEW_AREA_WIDTH, _PREVIEW_AREA_HEIGHT)
        pygame.draw.rect(game_surface, _PREVIEW_AREA_COLOR, preview_bg_rect)
        pygame.draw.rect(game_surface, _PREVIEW_BORDER_COLOR, preview_bg_rect, 2)

        next_label_surface = label_font.render(_NEXT_LABEL_TEXT, True, LABEL_FONT_COLOR)
        label_rect = next_label_surface.get_rect(center=(_NEXT_LABEL_X, _NEXT_LABEL_Y))
        game_surface.blit(next_label_surface, label_rect)

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
                next_tetromino.draw_at(game_surface, draw_x, draw_y, preview_block_size)

        render_offset_x = 0
        render_offset_y = 0
        if screen_shake_timer > 0:
            render_offset_x = random.randint(-screen_shake_intensity, screen_shake_intensity)
            render_offset_y = random.randint(-screen_shake_intensity, screen_shake_intensity)
            screen_shake_timer -= 1
            if screen_shake_timer == 0:
                screen_shake_intensity = 0

        screen.blit(game_surface, (render_offset_x, render_offset_y))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
