# Screen dimensions
SCREEN_HEIGHT = 600 # Base height
SCREEN_WIDTH = SCREEN_HEIGHT # Square window

# Grid dimensions
GRID_WIDTH = 10     # Number of columns in the game grid
GRID_HEIGHT = 20    # Number of rows in the game grid
BLOCK_SIZE = SCREEN_HEIGHT // GRID_HEIGHT # Size of a single block, ensures board fits height
GAME_BOARD_WIDTH = GRID_WIDTH * BLOCK_SIZE # Pixel width of the game board

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRID_COLOR = (128, 128, 128) # Light gray for the grid lines

# Tetromino Colors (defined in game_elements.py, but can be referenced here if needed)
# Example: CYAN = (0, 255, 255)

# Game speed (Original simple speed settings - will be replaced by dynamic leveling)
# INITIAL_FALL_SPEED = 0.5  # Time in seconds for a block to fall one step
# SPEED_INCREMENT_FACTOR = 0.05 # Factor by which speed increases with score/level
# MIN_FALL_SPEED = 0.1 # Minimum fall speed (fastest)

# Font settings
SCORE_FONT_SIZE = 28 # Adjusted size
SCORE_FONT_COLOR = (255, 255, 255) # White
GAME_OVER_FONT_SIZE = 40 # Adjusted size
GAME_OVER_FONT_COLOR = (255, 0, 0) # Red
FONT_NAME = None # None will use pygame's default font
LABEL_FONT_SIZE = 22 # Adjusted size
LABEL_FONT_COLOR = WHITE
NEXT_LABEL_TEXT = "Next:"
PAUSE_FONT_SIZE = 40 # Adjusted size

# Side Panel (for score and preview)
SIDE_PANEL_WIDTH = SCREEN_WIDTH - GAME_BOARD_WIDTH
SIDE_PANEL_PADDING = 20 # Padding within the side panel

# Score Display Position (within side panel)
SCORE_TEXT_X = GAME_BOARD_WIDTH + SIDE_PANEL_WIDTH // 2
SCORE_TEXT_Y = SIDE_PANEL_PADDING + SCORE_FONT_SIZE // 2 # Positioned at the top of side panel

# Preview Area settings (within side panel, below score)
PREVIEW_AREA_WIDTH = SIDE_PANEL_WIDTH - (2 * SIDE_PANEL_PADDING) # Width of preview area, with padding
PREVIEW_AREA_HEIGHT = PREVIEW_AREA_WIDTH * 0.8 # Attempt to make it somewhat proportional, can be adjusted
PREVIEW_AREA_X = GAME_BOARD_WIDTH + SIDE_PANEL_PADDING
PREVIEW_AREA_Y = SCORE_TEXT_Y + SCORE_FONT_SIZE // 2 + SIDE_PANEL_PADDING * 1.5 # Below score text with padding
PREVIEW_AREA_COLOR = (20, 20, 20) # Dark gray background for preview
PREVIEW_BORDER_COLOR = GRID_COLOR

# Next Block Label Position (above preview area)
NEXT_LABEL_X = PREVIEW_AREA_X + PREVIEW_AREA_WIDTH // 2
NEXT_LABEL_Y = PREVIEW_AREA_Y - LABEL_FONT_SIZE // 2 - 5 # 5px padding above preview box

# ==============================================================================
# GAME SOUND ASSETS
# ==============================================================================
# Replace the placeholder filenames below with the actual paths to your
# sound effect and music files.
#
# The game is currently configured to expect .mp3 files for all audio.
# Ensure your chosen audio files are in .mp3 format.
#
# If ENABLE_SOUND is True and files are not found, the game will print
# a warning to the console but will run without sound for that specific effect.
# ==============================================================================
ENABLE_SOUND = True # Master switch for all sounds and music

# Placeholder Sound Effect Filenames (replace with your .mp3 files)
ROTATE_SOUND_FILE = 'rotate_tech.mp3'
MOVE_SOUND_FILE = 'move_tech.mp3' # For block horizontal and soft drop movement
LAND_SOUND_FILE = 'land_tech.mp3' # When a block locks into place
LINE_CLEAR_SOUND_FILE = 'line_clear_tech.mp3' # For 1, 2, or 3 lines cleared
TETRIS_CLEAR_SOUND_FILE = 'tetris_clear_futuristic.mp3' # For 4 lines cleared (a Tetris)
GAME_OVER_SOUND_FILE = 'game_over_tech.mp3' # When the game ends

# Placeholder Background Music Filename (replace with your .mp3 file)
BACKGROUND_MUSIC_FILE = 'relaxing-guitar-loop-v5-245859.mp3'
# Placeholder for user's chosen background music: 'relaxing-guitar-loop-v5-245859.mp3'
# User needs to provide this file in .mp3 format.

# Visual Effects Settings
LINE_FLASH_DURATION = 15  # Frames (e.g., 0.25s at 60FPS, 0.5s at 30FPS)
LINE_FLASH_INTERVAL = 5   # Frames for each color state in flash
LINE_FLASH_COLOR = (255, 255, 255) # White, used for flashing effect

# Particle System Settings
PARTICLE_COUNT_PER_BLOCK = 3  # Base number of particles per cleared block
PARTICLE_LIFESPAN = 30        # Frames a particle will last
PARTICLE_SIZE = 3             # Pixel size of particles (radius for circles, or side for squares)
PARTICLE_VELOCITY_RANGE_X = (-1.5, 1.5) # Min/max horizontal velocity
PARTICLE_VELOCITY_RANGE_Y = (-2.5, -0.5) # Min/max initial vertical velocity (negative is up)

# Tetris Clear Specific Particle Enhancements
TETRIS_PARTICLE_COUNT_MULTIPLIER = 3  # Multiplier for particle count on a Tetris
TETRIS_PARTICLE_LIFESPAN_MULTIPLIER = 1.5 # Multiplier for lifespan on a Tetris
TETRIS_PARTICLE_SIZE_MULTIPLIER = 1.2   # Multiplier for size on a Tetris
TETRIS_PARTICLE_COLOR_OVERRIDE = None   # Example: (255, 215, 0) for gold, None to use block colors

# Lock Feedback Effect Settings
LOCK_FEEDBACK_DURATION = 6  # Frames (e.g., 0.1s at 60FPS or 0.2s at 30FPS)
# Option 1: Brightness multiplier
LOCK_FEEDBACK_BRIGHTNESS_MULTIPLIER = 1.5
# Option 2: Fixed flash color (if multiplier is not preferred, set multiplier to 1.0 or None)
LOCK_FEEDBACK_FLASH_COLOR = None # Example: (220, 220, 220)
# If LOCK_FEEDBACK_FLASH_COLOR is set, it will be used. Otherwise, brightness multiplier.

# Ghost Piece Settings
GHOST_PIECE_ALPHA = 100  # Transparency (0-255, lower is more transparent)
GHOST_PIECE_OUTLINE_THICKNESS = 1 # 0 or None to fill, >0 for outline only

# Screen Shake Effect Settings
SCREEN_SHAKE_DURATION_HARD_DROP = 5   # Frames
SCREEN_SHAKE_INTENSITY_HARD_DROP = 3  # Pixels (max offset)
SCREEN_SHAKE_DURATION_TETRIS = 8      # Frames
SCREEN_SHAKE_INTENSITY_TETRIS = 5     # Pixels

# Floating Score Text Settings
FLOATING_SCORE_LIFESPAN = 45  # Frames (e.g., 0.75s @ 60FPS)
FLOATING_SCORE_SPEED_Y = -1   # Pixels per frame (negative for upward)
FLOATING_SCORE_FONT_SIZE = 20
FLOATING_SCORE_COLOR = (255, 255, 100) # Light yellow
# FLOATING_SCORE_FADE_RATE is not needed as alpha is calculated from lifespan

# Block Bevel Effect Settings
BLOCK_BEVEL_OFFSET = 2  # Pixels, thickness of the bevel edges
BLOCK_HIGHLIGHT_BRIGHTNESS_FACTOR = 1.4 # Multiplier for lighter shade
BLOCK_SHADOW_DARKNESS_FACTOR = 0.6    # Multiplier for darker shade

# --- Level System Settings ---
MAX_LEVEL = 15  # Maximum reachable level

# Points progression
BASE_POINTS_FOR_NEXT_LEVEL_INCREMENT = 500 # Points needed to get from L1 to L2 (this is the delta, not cumulative)
ADDITIONAL_POINTS_INCREMENT_STEP = 250   # Each subsequent level will require 'delta' more points than the last 'delta',
                                         # where 'delta' increases by this step.
                                         # L1->L2 needs +BASE_POINTS_FOR_NEXT_LEVEL_INCREMENT
                                         # L2->L3 needs +(BASE_POINTS_FOR_NEXT_LEVEL_INCREMENT + 1*ADDITIONAL_POINTS_INCREMENT_STEP)
                                         # L3->L4 needs +(BASE_POINTS_FOR_NEXT_LEVEL_INCREMENT + 2*ADDITIONAL_POINTS_INCREMENT_STEP)
                                         # Cumulative points will be calculated based on these deltas.

# Fall Speed progression
INITIAL_FALL_SPEED_SECONDS = 0.8      # Initial time between downward movements (in seconds) for Level 1
FALL_SPEED_MULTIPLIER_PER_LEVEL = 0.95 # Speed_for_level_L = Speed_for_level_L-1 * multiplier
MIN_FALL_SPEED_SECONDS = 0.05         # Fastest allowed fall speed (seconds per step)

# Level Display UI
LEVEL_FONT_SIZE = 24
LEVEL_TEXT_COLOR = (200, 200, 255)  # A light blue/purple
LEVEL_LABEL_TEXT = "Level:"
# Position for Level display (ensure SCORE_TEXT_Y and SCORE_FONT_SIZE are defined above)
LEVEL_TEXT_X = GAME_BOARD_WIDTH + SIDE_PANEL_WIDTH // 2 # Centered in side panel
LEVEL_TEXT_Y = SCORE_TEXT_Y + SCORE_FONT_SIZE + 30      # Below score, with some padding
