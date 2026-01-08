import pygame
from settings import *

# Helper function for color manipulation
def adjust_color_brightness(color_tuple, factor):
    """Adjusts the brightness of an RGB color tuple by a factor."""
    r, g, b = color_tuple
    # Ensure colors stay within the 0-255 range
    new_r = min(255, int(r * factor))
    new_g = min(255, int(g * factor))
    new_b = min(255, int(b * factor))
    return (new_r, new_g, new_b)

class Board:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.block_size = SCREEN_HEIGHT // GRID_HEIGHT # BLOCK_SIZE from settings could be used too
        self.color_grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        # For line clear animation
        self.lines_to_clear_animation = []
        self.line_clear_animation_timer = 0
        self.last_lines_cleared_count = 0

        # For lock feedback effect
        self.just_locked_blocks = [] # List of (grid_col, grid_row, original_color_tuple)
        self.lock_feedback_timer = 0


    def is_valid_position(self, tetromino, offset_x=0, offset_y=0):
        """Checks if the tetromino's position (with optional offset) is valid."""
        for r_idx, row in enumerate(tetromino.shape):
            for c_idx, cell in enumerate(row):
                if cell:
                    board_x = tetromino.x + c_idx + offset_x
                    board_y = tetromino.y + r_idx + offset_y
                    # Check bounds
                    if not (0 <= board_x < GRID_WIDTH and 0 <= board_y < GRID_HEIGHT):
                        return False
                    # Check collision with existing blocks
                    if self.grid[board_y][board_x] != 0:
                        return False
        return True

    def add_tetromino(self, tetromino):
        """Adds a landed tetromino to the board's grid and initiates lock feedback."""
        self.just_locked_blocks = [] # Clear previous, or ensure it's cleared by timer
        for r_idx, row in enumerate(tetromino.shape):
            for c_idx, cell in enumerate(row):
                if cell:
                    grid_r, grid_c = tetromino.y + r_idx, tetromino.x + c_idx
                    if 0 <= grid_r < GRID_HEIGHT and 0 <= grid_c < GRID_WIDTH: # Ensure within bounds
                        self.grid[grid_r][grid_c] = 1
                        self.color_grid[grid_r][grid_c] = tetromino.color
                        self.just_locked_blocks.append((grid_c, grid_r, tetromino.color))

        if self.just_locked_blocks: # Only start feedback if blocks were actually added
            self.lock_feedback_timer = LOCK_FEEDBACK_DURATION


    def clear_lines(self):
        """Identifies completed lines and initiates the flashing animation."""
        if self.line_clear_animation_timer > 0: # Already animating
            return 0

        lines_to_clear_indices = []
        for r in range(GRID_HEIGHT -1, -1, -1): # Iterate from bottom up
            if all(self.grid[r]): # If line is full
                lines_to_clear_indices.append(r)

        if not lines_to_clear_indices:
            return 0 # No lines to clear

        self.lines_to_clear_animation = []
        for r_idx in lines_to_clear_indices:
            original_color_row = list(self.color_grid[r_idx])
            self.lines_to_clear_animation.append({'index': r_idx, 'colors': original_color_row})

        self.line_clear_animation_timer = LINE_FLASH_DURATION
        self.last_lines_cleared_count = len(lines_to_clear_indices) # Store how many lines are being cleared
        return self.last_lines_cleared_count

    def _perform_actual_line_clear(self):
        """
        Actually removes lines and shifts rows down. Called after animation.
        Returns data for particle generation: list of (world_x, world_y, color) tuples.
        """
        if not self.lines_to_clear_animation:
            return []

        num_cleared_this_cycle = len(self.lines_to_clear_animation)

        # Prepare particle data (world coordinates of each cleared block)
        particle_creation_data = []
        for anim_data in self.lines_to_clear_animation:
            row_idx = anim_data['index']
            original_colors = anim_data['colors']
            for x_grid_idx in range(GRID_WIDTH):
                block_color = original_colors[x_grid_idx]
                if block_color != BLACK: # Only create particles for actual blocks
                    world_x = x_grid_idx * self.block_size
                    world_y = row_idx * self.block_size
                    particle_creation_data.append((world_x, world_y, block_color))

        # Build new grid by skipping cleared lines
        new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(num_cleared_this_cycle)]
        new_color_grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(num_cleared_this_cycle)]

        current_grid_rows = []
        current_color_grid_rows = []

        cleared_indices_set = {anim_data['index'] for anim_data in self.lines_to_clear_animation}

        for r in range(GRID_HEIGHT -1, -1, -1):
            if r not in cleared_indices_set:
                current_grid_rows.insert(0, list(self.grid[r]))
                current_color_grid_rows.insert(0, list(self.color_grid[r]))

        new_grid.extend(current_grid_rows)
        new_color_grid.extend(current_color_grid_rows)

        self.grid = new_grid
        self.color_grid = new_color_grid

        self.lines_to_clear_animation = []
        return particle_creation_data


    def update_animations(self):
        """
        Updates line clearing animation.
        Returns: (clearing_just_finished_flag, list_of_particle_details, num_lines_cleared_this_cycle)
        particle_details is a list of (world_x, world_y, color) tuples.
        """
        particle_details_for_creation = []
        clearing_just_finished = False
        num_lines_actually_cleared = 0

        # Line Clear Animation Update
        if self.line_clear_animation_timer > 0:
            self.line_clear_animation_timer -= 1
            if self.line_clear_animation_timer == 0:
                num_lines_actually_cleared = self.last_lines_cleared_count
                particle_details_for_creation = self._perform_actual_line_clear()
                clearing_just_finished = True

        # Lock Feedback Animation Update
        if self.lock_feedback_timer > 0:
            self.lock_feedback_timer -= 1
            if self.lock_feedback_timer == 0:
                self.just_locked_blocks = [] # Clear the list once effect is done

        return clearing_just_finished, particle_details_for_creation, num_lines_actually_cleared


    def draw(self, screen):
        # Draw normally landed blocks first
        for y_idx in range(GRID_HEIGHT):
            for x_idx in range(GRID_WIDTH):
                rect = pygame.Rect(x_idx * self.block_size, y_idx * self.block_size, self.block_size, self.block_size)
                if self.grid[y_idx][x_idx] == 1:
                    base_color = self.color_grid[y_idx][x_idx]
                    is_locked_feedback_block = False

                    # Check if this block is part of the lock feedback effect
                    if self.lock_feedback_timer > 0:
                        for locked_gx, locked_gy, locked_original_color in self.just_locked_blocks:
                            if locked_gx == x_idx and locked_gy == y_idx:
                                is_locked_feedback_block = True
                                if LOCK_FEEDBACK_FLASH_COLOR:
                                    base_color = LOCK_FEEDBACK_FLASH_COLOR
                                else:
                                    base_color = adjust_color_brightness(locked_original_color, LOCK_FEEDBACK_BRIGHTNESS_MULTIPLIER)
                                break # Found the block, no need to check further in this list

                    # If part of a flashing line and animation is active, this overrides lock feedback for drawing
                    is_in_flashing_line = False
                    if self.line_clear_animation_timer > 0:
                        for anim_data in self.lines_to_clear_animation:
                            if y_idx == anim_data['index']:
                                is_in_flashing_line = True
                                # Determine flash color
                                flash_on = (self.line_clear_animation_timer % (LINE_FLASH_INTERVAL * 2)) < LINE_FLASH_INTERVAL
                                original_block_color_in_flash = anim_data['colors'][x_idx]
                                if original_block_color_in_flash != BLACK:
                                     base_color = LINE_FLASH_COLOR if flash_on else original_block_color_in_flash
                                else: # Should not happen if logic is correct (cleared lines are full)
                                     base_color = BLACK # Or some error color
                                break

                    if base_color != BLACK : # Draw if it's not an empty (possibly flashed to black) part of a line
                        _draw_beveled_block(screen, rect.x, rect.y, self.block_size, base_color)

                pygame.draw.rect(screen, GRID_COLOR, rect, 1) # Draw grid line (over block or empty cell)

        # The lock feedback drawing as an overlay is removed as it's integrated above.
        # The flashing line drawing is also integrated above.


def _draw_beveled_block(surface, x, y, size, base_color):
    """Helper function to draw a single beveled block."""
    if size <= BLOCK_BEVEL_OFFSET * 2: # Bevel would be too large or invert
        pygame.draw.rect(surface, base_color, (x, y, size, size))
        return

    highlight_color = adjust_color_brightness(base_color, BLOCK_HIGHLIGHT_BRIGHTNESS_FACTOR)
    shadow_color = adjust_color_brightness(base_color, BLOCK_SHADOW_DARKNESS_FACTOR)
    offset = BLOCK_BEVEL_OFFSET

    # Draw the four outer bevel edges as filled rectangles
    # Top highlight
    pygame.draw.rect(surface, highlight_color, (x, y, size, offset))
    # Left highlight
    pygame.draw.rect(surface, highlight_color, (x, y + offset, offset, size - offset)) # Adjusted to not overlap top-left corner fully
    # Bottom shadow
    pygame.draw.rect(surface, shadow_color, (x + offset, y + size - offset, size - offset, offset)) # Adjusted
    # Right shadow
    pygame.draw.rect(surface, shadow_color, (x + size - offset, y, offset, size - offset)) # Adjusted

    # Draw the central, main color part of the block
    inner_size = size - (2 * offset)
    pygame.draw.rect(surface, base_color, (x + offset, y + offset, inner_size, inner_size))


class Tetromino:
    SHAPES = {
        "I": [[1, 1, 1, 1]],
        "J": [[1, 0, 0], [1, 1, 1]],
        "L": [[0, 0, 1], [1, 1, 1]],
        "O": [[1, 1], [1, 1]],
        "S": [[0, 1, 1], [1, 1, 0]],
        "T": [[0, 1, 0], [1, 1, 1]],
        "Z": [[1, 1, 0], [0, 1, 1]]
    }
    COLORS = {
        "I": (0, 255, 255),  # Cyan
        "J": (0, 0, 255),    # Blue
        "L": (255, 165, 0),  # Orange
        "O": (255, 255, 0),  # Yellow
        "S": (0, 255, 0),    # Green
        "T": (128, 0, 128),  # Purple
        "Z": (255, 0, 0)     # Red
    }

    def __init__(self, shape_name, board): # Added board reference
        self.shape_name = shape_name
        self.shape = self.SHAPES[shape_name]
        self.color = self.COLORS[shape_name]
        # Position: col (x), row (y)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.board = board # Store a reference to the board for collision checks

    def rotate(self):
        """Rotates the tetromino 90 degrees clockwise."""
        # Transpose the shape matrix
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]

        # Check if the rotated shape is valid before applying
        # This is a basic check; more complex wall kick logic might be needed
        original_shape = self.shape
        self.shape = rotated_shape
        if not self.board.is_valid_position(self):
            # If not valid, try to nudge left/right
            if self.board.is_valid_position(self, offset_x=-1):
                self.x -= 1
            elif self.board.is_valid_position(self, offset_x=1):
                self.x += 1
            elif self.board.is_valid_position(self, offset_x=-2): # For I piece
                self.x -=2
            elif self.board.is_valid_position(self, offset_x=2): # For I piece
                self.x += 2
            else: # If still not valid, revert rotation
                self.shape = original_shape
        # Ensure x is within bounds after rotation and nudge
        if self.x < 0:
            self.x = 0
        elif self.x + len(self.shape[0]) > GRID_WIDTH:
            self.x = GRID_WIDTH - len(self.shape[0])


    def draw(self, surface, current_block_size): # Renamed screen to surface, block_size to current_block_size
        """Draws the tetromino on the screen with bevel effect."""
        # self.board.block_size should be equivalent to current_block_size passed from tetris.py
        for r_idx, row in enumerate(self.shape):
            for c_idx, cell in enumerate(row):
                if cell:
                    draw_x = (self.x + c_idx) * current_block_size
                    draw_y = (self.y + r_idx) * current_block_size
                    _draw_beveled_block(surface, draw_x, draw_y, current_block_size, self.color)


    def draw_at(self, surface, x_pixel_offset, y_pixel_offset, current_block_size): # Renamed for clarity
        """Draws the tetromino at a specific pixel offset with bevel, used for preview."""
        for r_idx, row in enumerate(self.shape):
            for c_idx, cell in enumerate(row):
                if cell:
                    draw_x = x_pixel_offset + c_idx * current_block_size
                    draw_y = y_pixel_offset + r_idx * current_block_size
                    _draw_beveled_block(surface, draw_x, draw_y, current_block_size, self.color)
