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

# Game speed
INITIAL_FALL_SPEED = 0.5  # Time in seconds for a block to fall one step
SPEED_INCREMENT_FACTOR = 0.05 # Factor by which speed increases with score/level
MIN_FALL_SPEED = 0.1 # Minimum fall speed (fastest)

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
# Replace the placeholder filenames below (e.g., 'rotate_tech.wav')
# with the actual paths to your sound effect and music files.
#
# Supported formats generally include .wav for sound effects
# and .ogg or .mp3 for background music.
#
# If ENABLE_SOUND is True and files are not found, the game will print
# a warning to the console but will run without sound for that specific effect.
# ==============================================================================
ENABLE_SOUND = True # Master switch for all sounds and music

# Placeholder Sound Effect Filenames (replace with your files)
ROTATE_SOUND_FILE = 'rotate_tech.wav'
MOVE_SOUND_FILE = 'move_tech.wav' # For block horizontal and soft drop movement
LAND_SOUND_FILE = 'land_tech.wav' # When a block locks into place
LINE_CLEAR_SOUND_FILE = 'line_clear_tech.wav' # For 1, 2, or 3 lines cleared
TETRIS_CLEAR_SOUND_FILE = 'tetris_clear_futuristic.wav' # For 4 lines cleared (a Tetris)
GAME_OVER_SOUND_FILE = 'game_over_tech.wav' # When the game ends

# Placeholder Background Music Filename (replace with your file)
BACKGROUND_MUSIC_FILE = 'music_futuristic_loop.ogg' # .ogg is good for looping music
